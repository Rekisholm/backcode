# coding:utf8
# author:Mars
from datetime import datetime
import subprocess
import time
import argparse
import os
import psutil
import logging
import json
import decimal


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        if "net_alert" in path:
            print("创建了/dev/shm/logs/ready/net_alert,用于存放流量告警日志")
        elif "net_status" in path:
            print("创建了/dev/shm/logs/ready/net_status,用于存放tshark状态日志")
        else:
            print("创建了/dev/shm/logs/ready/netready,用于存放流量日志")


def check_process(process_name):
    try:
        # 使用shell运行命令并获取输出
        process = subprocess.Popen(f"ps aux | grep {process_name}", stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()

        # 检查输出中是否有除grep命令外的tshark进程
        for line in output.decode().split('\n'):
            if process_name in line and 'grep' not in line:
                return True
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def clean_status():
    path = "/dev/shm/logs/ready/net_status/tshark_performance.log"
    log_size = os.path.getsize(path)
    if log_size // 100 > 300:
        with open(path, 'r') as f:
            lines = f.readlines()

        if len(lines) > 300:
            lines = lines[300:]

        with open(path, 'w') as f:
            f.writelines(lines)


def write_log(path, content):
    try:
        log_size = os.path.getsize(path)
        if log_size // 60 > 300:
            with open(path, 'r') as f:
                lines = f.readlines()

            if len(lines) > 300:
                lines = lines[300:]

            lines.append(content + '\n')

            with open(path, 'w') as f:
                f.writelines(lines)
        else:
            with open(path, 'a') as f:
                f.write(content + '\n')
    except Exception as e:
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write(content + '\n')
        else:
            print(e)


def get_dir_size(dir_path):
    file_list = os.listdir(dir_path)
    total_size = 0
    for file in file_list:
        if ".jsonl" in file:
            file_path = dir_path + '/' + file
            total_size += os.path.getsize(file_path)
    total_size = "{:.3f}".format(total_size / 2 ** 20)
    return total_size


def get_tshark_pid():
    tshark_pids = []
    process = subprocess.Popen(f"ps aux | grep tshark", stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    # 检查输出中是否有除grep命令外的tshark进程
    for line in output.decode().split('\n'):
        if "tshark -l" in line:
            line = line.split(" ")
            for item in line:
                if item.isdigit():
                    tshark_pids.append(item)
                    break
    if len(tshark_pids) == 0:
        return False
    return tshark_pids


def top_tshark():
    process = subprocess.Popen(f"top -b -n 1 | grep tshark", stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    # 检查输出中是否有除grep命令外的tshark进程
    for line in output.decode().split('\n'):
        if "tshark" in line:
            line = line.split(' ')
            for item in line:
                if '.' in item:
                    item = decimal.Decimal(item)
                    if isinstance(item, decimal.Decimal):
                        return item


def tshark_restart(command, tshark_pids):
    # kill tshark
    for tpid in tshark_pids:
        process = subprocess.Popen(f"kill -9 {tpid}", stdout=subprocess.PIPE, shell=True)
    # restart
    tshark_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    tshark_pid = tshark_process.pid
    return tshark_pid


def get_traffic(bridge, options, yes, m_ip):
    command = 'dumpcap -i {} -w - 2>/dev/null | tshark -l -t u -T ek -e frame.time_epoch -e frame.protocols -e http.host -e eth.src -e eth.dst -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e tcp.payload -e tcp.len {} -Y "http {}" -r - | python3 script.py'.format(
        bridge, options, yes)
    tshark_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    logging.basicConfig(filename='/dev/shm/logs/ready/net_status/tshark_performance.log', level=logging.INFO,
                        format='%(asctime)s - %(message)s')

    while True:
        tshark_pids = get_tshark_pid()
        tshark_cpu_usage = 0
        tshark_memory_usage = 0.0
        for tshark_pid in tshark_pids:
            tshark_pid = int(tshark_pid)
            # 获取tshark进程的内存使用情况
            tshark_memory_usage += psutil.Process(tshark_pid).memory_info().rss/2**20# 转换为MB
        tshark_memory_usage = "{:.3f} MB".format(tshark_memory_usage)

        # 获取磁盘使用情况/dev/shm/logs/ready/netready/
        disk_usage = get_dir_size("/dev/shm/logs/ready/netready")

        # 获取tshark进程的CPU占用率
        tshark_cpu_usage += top_tshark()

        # 记录性能数据到日志
        logging.info(
            f"CPU Usage: {tshark_cpu_usage}% - Memory Usage: {tshark_memory_usage}  - Disk Usage: {disk_usage} MB - IP: {m_ip}")

        if not check_process("tshark"):
            write_log('/dev/shm/logs/ready/net_alert/alert.log',
                      datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ' + 'The tshark has dead.' + ' - IP - ' + m_ip)
            tshark_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


        for interval in range(10):
            tshark_pids = get_tshark_pid()
            # 计算tshark占用内存
            memory_size = 0
            if tshark_pids == False:
                tshark_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                write_log('/dev/shm/logs/ready/net_alert/alert.log', datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S") + ' ' + 'Tshark has restarted.' + ' - IP - ' + m_ip)
                break
            for tpid in tshark_pids:
                process = subprocess.Popen(f"cat /proc/{tpid}/status | grep VmRSS", stdout=subprocess.PIPE, shell=True)
                output, error = process.communicate()
                for item in output.decode().split('\n')[0].split(' '):
                    if item.isdigit():
                        memory_size += int(item)
                        break
            memory_size /= 2**20
            if memory_size > 0.5:
                occupy = "{:.3f} GB".format(memory_size)
                tshark_pid = tshark_restart(command, tshark_pids)
                write_log('/dev/shm/logs/ready/net_alert/alert.log', datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S") + ' ' + f'Tshark takes up too much memory, {occupy}.' + ' - IP - ' + m_ip)
            time.sleep(3)
        clean_status()


def main():
    parser = argparse.ArgumentParser(description='A capture traffic Python script')
    # 添加 -e 和 -b 和 -y 参数
    parser.add_argument('-y', '--yes', type=str, action='append', help='Specify Display Filter')
    parser.add_argument('-e', '--option', type=str, action='append', help='Specify an option argument')
    parser.add_argument('-b', '--bridge', type=str, help='Specify a bridge argument')
    parser.add_argument('-s', '--source_ip', type=str, help='This machine source ip')

    args = parser.parse_args()

    options = ''
    if args.option:
        options = ['', ]
        options.extend(args.option)
        options = ' -e '.join(options)

    yes = ''
    if args.yes:
        yes = ['', ]
        yes.extend(args.yes)
        yes = ' or '.join(yes)

    bridge = ''
    if args.bridge:
        bridge = args.bridge

    if args.source_ip:
        m_ip = args.source_ip
        ip_dic = {"native_IP": m_ip}
        with open('ip.json', 'w') as f:
            f.write(json.dumps(ip_dic))
    else:
        print("Please input native ip like 'python3 capture.py -b lo -s 10.0.0.1'.")
        quit()

    if not bridge:
        print("Please input bridge name like 'python3 capture.py -b lo'.")
        quit()

    mkdir("/dev/shm/logs/ready/net_alert")
    mkdir("/dev/shm/logs/ready/net_status")
    mkdir("/dev/shm/logs/ready/netready")

    get_traffic(bridge, options, yes, m_ip)


if __name__ == '__main__':
    main()
