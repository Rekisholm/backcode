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
    # command_list = [
                    # "wget -O /root/install-sysdig https://cloud.tsinghua.edu.cn/f/def380d8b37241688032/?dl=1",
                    # "wget -O /root/sysdig_1107_match.sh https://cloud.tsinghua.edu.cn/f/b3113004d63f49a4a79e/?dl=1",
                    # "wget -O /root/middle_process.py https://cloud.tsinghua.edu.cn/f/1588a2c0d7124608ac32/?dl=1",
                    # "wget -O /root/mv_and_delete.py https://cloud.tsinghua.edu.cn/f/22421653210f48558d31/?dl=1",
                    # ]
    # for command in command_list:
    #     stdin, stdout, stderr = client.exec_command(command)
    #     time.sleep(3)
    #     err = stderr.read().decode()
    #     if err:
    #         print(f"Error: {err}")

    #     # 读取命令结果
    #     for line in stdout:
    #         print(line.strip('\n'))

    # 这里的目的 是找到进程号，然后kill
    kill_proc(client, "sysdig")
    kill_proc(client, "middle_process.py")
    kill_proc(client, "mv_and_delete.py")

    
    print("+" * 20 + " end " + hostname + "+ " * 20)
    print('\n')

    # 关闭连接
    client.close()


hostname = ['10.7.253.123', '10.7.253.124', '10.7.253.125', '10.7.253.126', '10.7.253.127',
            '10.7.253.128', '10.7.253.129', '10.7.253.130', '10.7.253.131', '10.7.253.132']
            # '10.7.253.108', '10.7.253.109', '10.7.253.110','10.7.253.111','10.7.253.112','10.7.253.113']
hostname = ['10.2.0.186', '10.2.0.187', '10.2.0.188','10.2.0.189','10.2.0.190']
port = 22
username = 'root'
password = 'thusw0rd'

for host in hostname:
    run_order(host, port, username, password)

