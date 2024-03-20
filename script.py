# coding:utf8
# author:Mars
import os.path
from datetime import datetime
import sys
import json


req_res = {}
traffic_size = {}
size_threshold = 500*1024
time_interval = 60
ip = ''


def write_log(path, content):
    with open(path, 'a') as f:
        f.write(content+'\n')


def write_traffic(path, traffic_cont):
    try:
        traffic_size = os.path.getsize(path)
        if traffic_size // 500 > 200:
            with open(path, 'r') as f:
                lines = f.readlines()

            if len(lines) > 200:
                lines = lines[100:]

            lines.append(traffic_cont+'\n')

            with open(path, 'w') as f:
                f.writelines(lines)
        else:
            with open(path, 'a') as f:
                f.write(traffic_cont + '\n')

    except Exception as e:
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write(traffic_cont + '\n')
        else:
            write_log("/dev/shm/logs/ready/net_alert/alert.log", datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"An unexpected error occurred: {e}" + ip)


def link_check(http_host, ip_src, ip_dst):
    # 有http_host 情况一：已经添加了， 还有可能未添加
    if http_host and "-gen" in http_host[0]:
        req_res[tuple(ip_src) + tuple(ip_dst)] = http_host[0].split('-')[1]
        return http_host[0].split('-')[1]
    elif http_host and "-gen" not in http_host[0]:
        return None
    return req_res.get(tuple(ip_dst + ip_src))


def control_size(http_host, time, line_len):
    time = float(time)
    if traffic_size.get(http_host) is None:
        traffic_size[http_host] = [[time, line_len]]
        return True
    else:
        time_size = traffic_size.get(http_host)
        time_size_len = len(time_size)
        size = line_len
        for index, item in enumerate(time_size[::-1]):
            if time - item[0] < time_interval:
                index = time_size_len - 1 - index
                size += item[1]
            else:
                index = time_size_len - 1 - index
                break
        time_size = time_size[index:]

        if size > size_threshold:
            # write a log
            # path
            content = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "The collection system lost a traffic packet from " + http_host + ip
            write_log("/dev/shm/logs/ready/net_alert/alert.log", content)
            return False
        else:
            time_size.append([time, line_len])
            traffic_size[http_host] = time_size
            return True


def process_traffic():
    # 读取本机IP
    with open('ip.json', 'r') as f:
        line = f.readline()
    ip = json.loads(line).get('native_IP')
    ip = " - IP - " + ip

    # 从标准输入读取数据
    for line in sys.stdin:
        # 在这里处理每行数据
        try:
            traffic_dic = json.loads(line)
            if traffic_dic.get("index"):
                pass
            else:
                http_host = traffic_dic.get("layers").get("http_host")
                ip_src = traffic_dic.get("layers").get("ip_src")
                ip_dst = traffic_dic.get("layers").get("ip_dst")
                res = link_check(http_host, ip_src, ip_dst)
                if res is None:
                    pass
                else:
                    state = control_size(res, traffic_dic.get("layers").get("frame_time_epoch")[0], len(line))
                    if state:
                        # /dev/shm/logs/ready/netready
                        path = "/dev/shm/logs/ready/netready/" + res + "_traffic" + ".jsonl"
                        # parse and write into res[1].jsonl
                        if traffic_dic.get("layers").get("tcp_payload") == None:
                            pass
                        else:
                            content = traffic_dic.get("layers").get("tcp_payload")[0]
                            content = bytes.fromhex(content).decode("utf-8", "ignore")
                            traffic_dic.get("layers")["tcp_payload"][0] = content
                            traffic_dic.get("layers")["http_host"] = [res]
                            line = json.dumps(traffic_dic)
                        write_traffic(path, line)
        except json.JSONDecodeError as e:
            content = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S") + " " + "JSON parsing error " + line + str(e) + ip
            write_log("/dev/shm/logs/ready/net_alert/alert.log", content)
        sys.stdout.flush()


if __name__ == "__main__":
    process_traffic()
