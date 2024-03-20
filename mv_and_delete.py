from datetime import datetime
import shutil
import signal
import os
from threading import Timer
import socket
import psutil
import json

# list = ["2023-11-01 09:11:48.175250680###apache2###13###>###read###<4t>192.0.2.2:52450->192.0.2.5:80###8000###<NA>###<NA>###192.0.2.2:52450->192.0.2.5:80###9###/usr/sbin/apache2###<NA>###192.0.2.5###192.0.2.2###80###52450###511c592b839e###service52301ba394f348b4910d2509a416db24.1.ipmpus42fs5aajzxui00ugxvd###APACHE_PID_FILE=/var/run/apache2/apache2.pid LDFLAGS=-Wl,-O1 -Wl,--hash-style=both HOSTNAME=511c592b839e APACHE_RUN_USER=www-data PHP_INI_DIR=/usr/local/etc/php PHP_ASC_URL=https://secure.php.net/get/php-5.6.28.tar.xz.asc/from/this/mirror CPPFLAGS=-fstack-protector-strong -fpic -fpie -O2 PHP_MD5=1e01c66b2e67ab3b56a6180ee560fe4c PHPIZE_DEPS=autoconf 		file 		g++ 		gcc 		libc-dev 		make 		pkg-config 		re2c capture_group_name=2 PHP_URL=https://secure.php.net/get/php-5.6.28.tar.xz/from/this/mirror APACHE_ENVVARS=/etc/apache2/envvars APACHE_LOG_DIR=/var/log/apache2 PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin GPG_KEYS=0BD78B5F97500D450838F95DFE857D9A90D90EC1 6E4F6AB321FDC07F2C332E3AC2BF0BC433CFC8B3 SUPERVISOR_GROUP_NAME=apache2 PWD=/var/www LANG=C APACHE_RUN_GROUP=www-data SUPERVISOR_ENABLED=1 SHLVL=0 PHP_SHA256=07187ba2870f89cef334cd2ad6cb801aeec5eaf283da0293a9a6be75d6786d11 CFLAGS=-fstack-protector-strong -fpic -fpie -O2 APACHE_CONFDIR=/etc/apache2 SUPERVISOR_PROCESS_NAME=apache2 SUPERVISOR_SERVER_URL=unix:///var/run/supervisor.sock PHP_EXTRA_BUILD_DEPS=apache2-dev APACHE_LOCK_DIR=/var/lock/apache2 APACHE_RUN_DIR=/var/run/apache2 PHP_VERSION=5.6.28 PHP_EXTRA_CONFIGURE_ARGS=--with-apxs2",
# "2023-11-01 09:11:48.175260606###apache2###13###<###read###553###GET / HTTP/1.1..Host: service523-f86608ef18-1.thudart.cn..User-Agent: Mozilla/5.###<NA>###<NA>###192.0.2.2:52450->192.0.2.5:80###9###/usr/sbin/apache2###553###192.0.2.5###192.0.2.2###80###52450###511c592b839e###service52301ba394f348b4910d2509a416db24.1.ipmpus42fs5aajzxui00ugxvd###APACHE_PID_FILE=/var/run/apache2/apache2.pid LDFLAGS=-Wl,-O1 -Wl,--hash-style=both HOSTNAME=511c592b839e APACHE_RUN_USER=www-data PHP_INI_DIR=/usr/local/etc/php PHP_ASC_URL=https://secure.php.net/get/php-5.6.28.tar.xz.asc/from/this/mirror CPPFLAGS=-fstack-protector-strong -fpic -fpie -O2 PHP_MD5=1e01c66b2e67ab3b56a6180ee560fe4c PHPIZE_DEPS=autoconf 		file 		g++ 		gcc 		libc-dev 		make 		pkg-config 		re2c capture_group_name=2 PHP_URL=https://secure.php.net/get/php-5.6.28.tar.xz/from/this/mirror APACHE_ENVVARS=/etc/apache2/envvars APACHE_LOG_DIR=/var/log/apache2 PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin GPG_KEYS=0BD78B5F97500D450838F95DFE857D9A90D90EC1 6E4F6AB321FDC07F2C332E3AC2BF0BC433CFC8B3 SUPERVISOR_GROUP_NAME=apache2 PWD=/var/www LANG=C APACHE_RUN_GROUP=www-data SUPERVISOR_ENABLED=1 SHLVL=0 PHP_SHA256=07187ba2870f89cef334cd2ad6cb801aeec5eaf283da0293a9a6be75d6786d11 CFLAGS=-fstack-protector-strong -fpic -fpie -O2 APACHE_CONFDIR=/etc/apache2 SUPERVISOR_PROCESS_NAME=apache2 SUPERVISOR_SERVER_URL=unix:///var/run/supervisor.sock PHP_EXTRA_BUILD_DEPS=apache2-dev APACHE_LOCK_DIR=/var/lock/apache2 APACHE_RUN_DIR=/var/run/apache2 PHP_VERSION=5.6.28 PHP_EXTRA_CONFIGURE_ARGS=--with-apxs2",
# "2023-11-01 09:11:48.175421180###apache2###13###>###open###/var/www/.htaccess###O_RDONLY|O_CLOEXEC###0###<NA>###<NA>###9###/usr/sbin/apache2###<NA>###<NA>###<NA>###<NA>###<NA>###511c592b839e###service52301ba394f348b4910d2509a416db24.1.ipmpus42fs5aajzxui00ugxvd###APACHE_PID_FILE=/var/run/apache2/apache2.pid LDFLAGS=-Wl,-O1 -Wl,--hash-style=both HOSTNAME=511c592b839e APACHE_RUN_USER=www-data PHP_INI_DIR=/usr/local/etc/php PHP_ASC_URL=https://secure.php.net/get/php-5.6.28.tar.xz.asc/from/this/mirror CPPFLAGS=-fstack-protector-strong -fpic -fpie -O2 PHP_MD5=1e01c66b2e67ab3b56a6180ee560fe4c PHPIZE_DEPS=autoconf 		file 		g++ 		gcc 		libc-dev 		make 		pkg-config 		re2c capture_group_name=2 PHP_URL=https://secure.php.net/get/php-5.6.28.tar.xz/from/this/mirror APACHE_ENVVARS=/etc/apache2/envvars APACHE_LOG_DIR=/var/log/apache2 PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin GPG_KEYS=0BD78B5F97500D450838F95DFE857D9A90D90EC1 6E4F6AB321FDC07F2C332E3AC2BF0BC433CFC8B3 SUPERVISOR_GROUP_NAME=apache2 PWD=/var/www LANG=C APACHE_RUN_GROUP=www-data SUPERVISOR_ENABLED=1 SHLVL=0 PHP_SHA256=07187ba2870f89cef334cd2ad6cb801aeec5eaf283da0293a9a6be75d6786d11 CFLAGS=-fstack-protector-strong -fpic -fpie -O2 APACHE_CONFDIR=/etc/apache2 SUPERVISOR_PROCESS_NAME=apache2 SUPERVISOR_SERVER_URL=unix:///var/run/supervisor.sock PHP_EXTRA_BUILD_DEPS=apache2-dev APACHE_LOCK_DIR=/var/lock/apache2 APACHE_RUN_DIR=/var/run/apache2 PHP_VERSION=5.6.28 PHP_EXTRA_CONFIGURE_ARGS=--with-apxs2",
# "2023-11-01 09:11:48.175433551###apache2###13###<###open###ENOENT###/var/www/.htaccess###O_RDONLY|O_CLOEXEC###0###/var/www/.htaccess###9###/usr/sbin/apache2###-2###<NA>###<NA>###<NA>###<NA>###511c592b839e###service52301ba394f348b4910d2509a416db24.1.ipmpus42fs5aajzxui00ugxvd###APACHE_PID_FILE=/var/run/apache2/apache2.pid LDFLAGS=-Wl,-O1 -Wl,--hash-style=both HOSTNAME=511c592b839e APACHE_RUN_USER=www-data PHP_INI_DIR=/usr/local/etc/php PHP_ASC_URL=https://secure.php.net/get/php-5.6.28.tar.xz.asc/from/this/mirror CPPFLAGS=-fstack-protector-strong -fpic -fpie -O2 PHP_MD5=1e01c66b2e67ab3b56a6180ee560fe4c PHPIZE_DEPS=autoconf 		file 		g++ 		gcc 		libc-dev 		make 		pkg-config 		re2c capture_group_name=2 PHP_URL=https://secure.php.net/get/php-5.6.28.tar.xz/from/this/mirror APACHE_ENVVARS=/etc/apache2/envvars APACHE_LOG_DIR=/var/log/apache2 PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin GPG_KEYS=0BD78B5F97500D450838F95DFE857D9A90D90EC1 6E4F6AB321FDC07F2C332E3AC2BF0BC433CFC8B3 SUPERVISOR_GROUP_NAME=apache2 PWD=/var/www LANG=C APACHE_RUN_GROUP=www-data SUPERVISOR_ENABLED=1 SHLVL=0 PHP_SHA256=07187ba2870f89cef334cd2ad6cb801aeec5eaf283da0293a9a6be75d6786d11 CFLAGS=-fstack-protector-strong -fpic -fpie -O2 APACHE_CONFDIR=/etc/apache2 SUPERVISOR_PROCESS_NAME=apache2 SUPERVISOR_SERVER_URL=unix:///var/run/supervisor.sock PHP_EXTRA_BUILD_DEPS=apache2-dev APACHE_LOCK_DIR=/var/lock/apache2 APACHE_RUN_DIR=/var/run/apache2 PHP_VERSION=5.6.28 PHP_EXTRA_CONFIGURE_ARGS=--with-apxs2"]


MAX_LINE_LIMIT = 10485760 #10兆字节 #100000000 # 最大限制字节数
SYSDIG_FINAL_PATH = "/dev/shm/logs/ready/sysready/" # 转发路径"/root/data/"  #
SYSDIG_ORIGIN_PATH = "/dev/shm/logs/sysdig/"  # 日志初始地址(sysdig采集器所在地址)"/root/dhr-testsysdigenv-1101/" #
ALRET_FILE = "/dev/shm/logs/ready/sys_alert/sysdig_alert.log"  # 告警日志地址
RESOURCE_FILE = "/dev/shm/logs/ready/sys_status/sysdig_resource.log"  # 状态日志地址
TIME_CIRCLE = 60.0 #转发/告警/资源监测频率

def move_delete_files():
    if not os.path.exists(SYSDIG_ORIGIN_PATH):  
        os.makedirs(SYSDIG_ORIGIN_PATH)

    filelist = os.listdir(SYSDIG_ORIGIN_PATH)      #列出该目录下的所有文件,listdir返回的文件列表是不包含路径的
    for filename in filelist:
        f_size = os.path.getsize(SYSDIG_ORIGIN_PATH + filename)
        if len(filename) != 14 or '###' in filename:
            os.remove(SYSDIG_ORIGIN_PATH + filename)
        elif f_size > MAX_LINE_LIMIT:
            os.remove(SYSDIG_ORIGIN_PATH + filename)
            generate_exceed_alert(f_size, filename)
        else:
            if os.path.exists(SYSDIG_FINAL_PATH + filename):  
                os.remove(SYSDIG_FINAL_PATH + filename)
            src = os.path.join(SYSDIG_ORIGIN_PATH, filename)
            dst = os.path.join(SYSDIG_FINAL_PATH, filename)
            shutil.move(src, dst)


def get_ipaddress():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

IP_ADDR = get_ipaddress()

def generate_exceed_alert(f_size:int, filename:str):
    now = datetime.now()
    dt = now.strftime("%Y-%m-%d, %H:%M:%S")
    ip = IP_ADDR
    info = { 'datetime': str(dt), 'ip': str(ip), 'team_name': filename.split('.')[0], 'file_size': str(f_size), 'msg':''}
    # info = "{ datetime:" + str(dt) + ", ip:" + str(ip) + ", team_name:" + filename.split('.')[0] + ", file_size:" + str(f_size) + " }\n"
    with open(file=ALRET_FILE, mode='a') as f:
        json.dump(info, f)
        f.write('\n')


def getdirsize(dir):
   size = 0
   for _, _, files in os.walk(dir):
      size += sum([os.path.getsize(dir + name) for name in files])
   return size


def generate_sysdigdown_alert():
    now = datetime.now()
    dt = now.strftime("%Y-%m-%d, %H:%M:%S")
    ip = IP_ADDR
    info = { 'datetime': str(dt), 'ip': str(ip), 'team_name': '', 'file_size': '', 'msg':'sysdig has downed.'}
    # info = "{ datetime:" + str(dt) + ", ip:" + str(ip) + ", sysdig has downed."  + " }\n"
    with open(file=ALRET_FILE, mode='a') as f:
        json.dump(info, f)
        f.write('\n')


def monite_sysdig_resource_utilization():
    # a = os.popen('ps -ef | grep sysdig')
    # output = a.readlines()
    # sysdig_pid = int(str.split(output[0])[1])
    # print("sysdig_pid", sysdig_pid)
    sysdig_pid = get_pid('sysdig')
    try:
        process = psutil.Process(sysdig_pid)
        # 获取CPU占用情况
        cpu_percent = process.cpu_percent()
        # 获取内存占用情况
        memory_percent = process.memory_percent()
        # 获取磁盘占用情况
        disk_usage = getdirsize(SYSDIG_FINAL_PATH)  #psutil.disk_usage(SYSDIG_FINAL_PATH)
    
        # a = os.popen('ps -ef | grep middle_process')
        # output = a.readlines()
        # mid_pid = int(str.split(output[0])[1])
        # os.kill(mid_pid)
        # os.system('python3 ' + MID_PROC_ADDR)
    
        now = datetime.now()
        dt = now.strftime("%Y-%m-%d, %H:%M:%S")
        ip = IP_ADDR
        info  = { 'datetime': str(dt), 'ip': str(ip), 'cpu_percent': str(cpu_percent), 'memory_percent': str(memory_percent), 'disk_usage': str(disk_usage)}
        # info = "{ datetime:" + str(dt) + ", ip:" + str(ip) + ", cpu_percentage:" + str(cpu_percent) + ", memory_percent:" + str(memory_percent) + " disk_usage:" + str(disk_usage) + " }\n"
        with open(file=RESOURCE_FILE, mode='a') as f:
            json.dump(info, f)
            f.write('\n')
    except Exception:
        generate_sysdigdown_alert()


def get_pid(name):
    pids = psutil.process_iter()
    for pid in pids:
        if name in pid.name():
            return pid.pid
    return -1


def func():
    monite_sysdig_resource_utilization()
    move_delete_files()

class RepeatingTimer(Timer): 
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)

t = RepeatingTimer(TIME_CIRCLE, func)
t.start()
