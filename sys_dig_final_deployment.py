import time
import paramiko

def kill_proc(client:paramiko.SSHClient, proc_name:str):
    command_list = ["ps aux | grep " + proc_name]
    for index, command in enumerate(command_list):
        print(command)
        stdin, stdout, stderr = client.exec_command(command)

        # 读取命令结果
        for line in stdout:
            line = line.strip('\n')
            if index == 0 and proc_name in line:
                print(line)
                line = line.split(' ')
                for item in line:
                    if item.isdigit():
                        print("need kill pid is:", item)
                        stdin, stdout, stderr = client.exec_command("kill -9 " + str(item))
                        break


def check_success(client:paramiko.SSHClient, proc_name:str):
    stdin, stdout, stderr = client.exec_command("ps aux | grep sysdig")

    print('\n')
    # 读取命令结果
    for line in stdout:
        line = line.strip('\n')
        print(line)
    


# SSH服务器的设置
def run_order(hostname, port, username, password):
    hostname = hostname
    port = port
    username = username
    password = password

    # 创建SSH客户端实例
    client = paramiko.SSHClient()

    # 自动添加服务器的主机名和新的主机密钥
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 连接到服务器
    client.connect(hostname, port, username, password)
    print("+"*20 + " begin " + hostname + " +"*20)
    # 运行命令 更新代码从清华网盘
    client.exec_command("mkdir /root/sysfinal_files")
    command_list = [
                    "wget -O /root/sysfinal_files/sysdig_final.sh https://cloud.tsinghua.edu.cn/f/6281e2c0bafb432e8dbb/?dl=1",
                    "wget -O /root/sysfinal_files/middle_process.py https://cloud.tsinghua.edu.cn/f/4e5b30941f6b4d46849c/?dl=1",
                    "wget -O /root/sysfinal_files/mv_and_delete.py https://cloud.tsinghua.edu.cn/f/10fe81d1944749359109/?dl=1",
                    ]
    for command in command_list:
        stdin, stdout, stderr = client.exec_command(command)
        time.sleep(3)
        err = stderr.read().decode()
        if err:
            print(f"Error: {err}")

        # 读取命令结果
        for line in stdout:
            print(line.strip('\n'))

    # 这里的目的 是找到进程号，然后kill
    kill_proc(client, "sysdig")
    kill_proc(client, "middle_process.py")
    kill_proc(client, "mv_and_delete.py")
    time.sleep(3)
    # 这里是重新部署
    # client.exec_command("chmod +x install-sysdig")
    # client.exec_command("./install-sysdig -y")
    # client.exec_command("apt-get install python3-pip -y")
    # client.exec_command("pip3 install psutil")
    # client.exec_command("rm -r /root/logs")
    # client.exec_command("rm -r /root/ready")
    # client.exec_command("rm -r /root/sysready")
    # client.exec_command("rm -r /root/sys_status")
    # client.exec_command("rm -r /root/sys_alert")
    # client.exec_command("mkdir /dev/shm/logs")
    # client.exec_command("mkdir /dev/shm/logs/ready")
    # client.exec_command("mkdir /dev/shm/logs/ready/sysready")
    stdin, stdout, stderr = client.exec_command("chmod +x /root/sysfinal_files/sysdig_final.sh")
    stdin, stdout, stderr = client.exec_command("nohup python3 /root/sysfinal_files/middle_process.py >/dev/null 2>&1 &")
    stdin, stdout, stderr = client.exec_command("nohup python3 /root/sysfinal_files/mv_and_delete.py >/dev/null 2>&1 &")
    time.sleep(2)

    # 这里检查是否部署成功，查看运行状态
    check_success(client, "sysdig")
    check_success(client, "middle_process")
    check_success(client, "mv_and_delete")
    print("+" * 20 + " end " + hostname + "+ " * 20)
    print('\n')

    # 关闭连接
    client.close()


#hostname = ['10.7.253.123', '10.7.253.124', '10.7.253.125', '10.7.253.126', '10.7.253.127',
#           '10.7.253.128', '10.7.253.129', '10.7.253.130', '10.7.253.131', '10.7.253.132']
hostname = ['10.2.0.186', '10.2.0.187', '10.2.0.188','10.2.0.189','10.2.0.190']
port = 22
username = 'root'
password = 'thusw0rd'

for host in hostname:
    run_order(host, port, username, password)
