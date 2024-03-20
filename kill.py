import time
import paramiko

count = 0
record = []


def check_alive(client, script):
    command = "ps aux | grep {}".format(script)
    stdin, stdout, stderr = client.exec_command(command)

    # 读取命令结果
    for line in stdout:
        line = line.strip('\n')
        if script == "capture.py" and "capture.py -b" in line:
            line = line.split(' ')
            for item in line:
                if item.isdigit():
                    return item

        elif script == "tshark" and "tshark -l" in line:
            line = line.split(' ')
            for item in line:
                if item.isdigit():
                    return item

        elif script == "script.py" and "script.py" in line and "tshark" not in line and "grep" not in line:
            line = line.split(' ')
            for item in line:
                if item.isdigit():
                    return item

    return False


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

    print(" + " * 20 + " begin check " + hostname + " + " * 20)


    model = 'a'

    if model == 'm':
        quit()
    else:
        command_list = ["ps aux | grep capture.py", "ps aux |grep tshark", "ps aux | grep script.py"]
        for index, command in enumerate(command_list):
            print(command)
            stdin, stdout, stderr = client.exec_command(command)
            # 读取命令结果
            for line in stdout:
                line = line.strip('\n')
                if index == 0 and "capture.py -b" in line:
                    print(line)
                    line = line.split(' ')
                    for item in line:
                        if item.isdigit():
                            stdin, stdout, stderr = client.exec_command("kill -9 " + str(item))
                            break
                elif index == 1 and "tshark -i" in line:
                    print(line)
                    line = line.split(' ')
                    for item in line:
                        if item.isdigit():
                            stdin, stdout, stderr = client.exec_command("kill -9 " + str(item))
                            break
                elif index == 2 and "script.py" in line:
                    print(line)
                    line = line.split(' ')
                    for item in line:
                        if item.isdigit():
                            stdin, stdout, stderr = client.exec_command("kill -9 " + str(item))
                            break



        stdin, stdout, stderr = client.exec_command("ps aux|grep python3")
        print('\n')
        # 读取命令结果
        for line in stdout:
            line = line.strip('\n')
            if "capture.py" in line or "script.py" in line:
                print(line)

        stdin, stdout, stderr = client.exec_command("ps aux|grep tshark")
        print('\n')
        # 读取命令结果
        for line in stdout:
            line = line.strip('\n')
            if "tshark -l" in line:
                print(line)

        c_pid = check_alive(client, "capture.py")
        t_pid = check_alive(client, "tshark")
        s_pid = check_alive(client, "script.py")


        if(c_pid  == False and t_pid == False and s_pid == False):
            record.append(hostname)



    print(" + " * 20 + " end check" + hostname + " + " * 20)
    print('\n')

    # 关闭连接
    client.close()

    time.sleep(1)


# SSH服务器的设置

hostname = ['10.7.253.123', '10.7.253.124', '10.7.253.125', '10.7.253.126', '10.7.253.127','10.7.253.128', '10.7.253.129', '10.7.253.130', '10.7.253.131', '10.7.253.132', '10.7.253.108', '10.7.253.109', '10.7.253.110', '10.7.253.111', '10.7.253.112', '10.7.253.113']
# hostname = ["47.98.203.48"]
port = 22
username = 'root'
password = 'Aa@13579'

while True:

    for host in hostname:
        run_order(host, port, username, password)

    if count == len(hostname):
        summary = "During this patrol, all equipment was running well."

        # 设置框的宽度，根据需要调整
        width = len(summary) + 4

        # 打印顶部的边框
        print("+" + "-" * width + "+")

        # 打印内容，左右各留有空格
        print("|  " + summary + "  |")

        # 打印底部的边框
        print("+" + "-" * width + "+")
    else:
        content = "During this patrol, the equipment with operating problems is as follows: "

        # 为了使框看起来更整洁，根据内容长度设置框的宽度
        # 这里我们给内容两边各加了一个空格，所以宽度要加2
        width = len(content) + 2

        # 打印框的顶部
        print("+" + "-" * width + "+")

        # 打印内容，左右各有一个空格
        print("|" + content.center(width) + "|")
        for r in record:
            print("|" + r.center(width) + "|")
        # 打印框的底部
        print("+" + "-" * width + "+")
    count = 0
    time.sleep(5)
    flag = input("Do you want to continue ending?(yes/no)")
    if flag == "no":
        quit()
    else:
        pass
