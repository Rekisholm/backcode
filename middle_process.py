import subprocess
import os


shell_script = "/root/sysdig_final.sh" # 采集器脚本地址(sysdig采集器所在地址+名称)
SYSDIG_ORIGIN_PATH = "/dev/shm/logs/sysdig/"  # 日志初始地址(sysdig采集器所在地址)'/root/dhr-testsysdigenv-1101/' #

if not os.path.exists(SYSDIG_ORIGIN_PATH):
    os.makedirs(SYSDIG_ORIGIN_PATH)


def sysdig_process():
    # output_lines_num = {}
    # f_dict = {}
    process = subprocess.Popen(shell_script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while 1:
        for line in process.stdout:  #list:  #
            #process line format and get team's id:
            start_id = line.find('foundation_capture_group_id') + len('foundation_capture_group_id=')
            end_id = start_id + 11
            team_name = line[start_id:end_id]
            team_name = ''.join(team_name.split('-'))
            last_1_id = line.rfind('###')
            # last_2_id = line.rfind('###', 0, last_1_id)
            # container_start_id = line.rfind('###', 0, last_2_id) + 3
            new_line = line[0:last_1_id] + '###' + team_name + '\n'
            # filename = SYSDIG_ORIGIN_PATH + "sysdig_" + line[container_start_id:last_2_id-1] + ".log"
            filename = SYSDIG_ORIGIN_PATH + team_name + ".log"
            print(filename)
            #open many files and directly write a line into one of them:
            with open(file=filename, mode='a') as f:
                f.write(new_line)
                f.flush()
            # if f_dict.get(filename) is None:
            #     f = open(filename, 'a')
            #     f_dict[filename] = f
            #     output_lines_num[filename] = 0
            # f_dict[filename].write(new_line)
            # output_lines_num[filename] += 1

if __name__ == "__main__":
    sysdig_process()
