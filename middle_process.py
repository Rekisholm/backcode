import subprocess
import os

# list = ["2023-11-01 09:11:48.175250680###apache2###13###>###read###<4t>192.0.2.2:52450->192.0.2.5:80###8000###<NA>###<NA>###192.0.2.2:52450->192.0.2.5:80###9###/usr/sbin/apache2###<NA>###192.0.2.5###192.0.2.2###80###52450###511c592b839e###service52301ba394f348b4910d2509a416db24.1.ipmpus42fs5aajzxui00ugxvd###APACHE_PID_FILE=/var/run/apache2/apache2.pid LDFLAGS=-Wl,-O1 -Wl,--hash-style=both HOSTNAME=511c592b839e APACHE_RUN_USER=www-data PHP_INI_DIR=/usr/local/etc/php PHP_ASC_URL=https://secure.php.net/get/php-5.6.28.tar.xz.asc/from/this/mirror CPPFLAGS=-fstack-protector-strong -fpic -fpie -O2 PHP_MD5=1e01c66b2e67ab3b56a6180ee560fe4c PHPIZE_DEPS=autoconf 		file 		g++ 		gcc 		libc-dev 		make 		pkg-config 		re2c foundation_capture_group_id=6fd9fc11-60dd-4b2a-aa55-46929a0dc67a PHP_URL=https://secure.php.net/get/php-5.6.28.tar.xz/from/this/mirror APACHE_ENVVARS=/etc/apache2/envvars APACHE_LOG_DIR=/var/log/apache2 PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin GPG_KEYS=0BD78B5F97500D450838F95DFE857D9A90D90EC1 6E4F6AB321FDC07F2C332E3AC2BF0BC433CFC8B3 SUPERVISOR_GROUP_NAME=apache2 PWD=/var/www LANG=C APACHE_RUN_GROUP=www-data SUPERVISOR_ENABLED=1 SHLVL=0 PHP_SHA256=07187ba2870f89cef334cd2ad6cb801aeec5eaf283da0293a9a6be75d6786d11 CFLAGS=-fstack-protector-strong -fpic -fpie -O2 APACHE_CONFDIR=/etc/apache2 SUPERVISOR_PROCESS_NAME=apache2 SUPERVISOR_SERVER_URL=unix:///var/run/supervisor.sock PHP_EXTRA_BUILD_DEPS=apache2-dev APACHE_LOCK_DIR=/var/lock/apache2 APACHE_RUN_DIR=/var/run/apache2 PHP_VERSION=5.6.28 PHP_EXTRA_CONFIGURE_ARGS=--with-apxs2"]
# "2023-11-01 09:11:48.175260606###apache2###13###<###read###553###GET / HTTP/1.1..Host: service523-f86608ef18-1.thudart.cn..User-Agent: Mozilla/5.###<NA>###<NA>###192.0.2.2:52450->192.0.2.5:80###9###/usr/sbin/apache2###553###192.0.2.5###192.0.2.2###80###52450###511c592b839e###service52301ba394f348b4910d2509a416db24.1.ipmpus42fs5aajzxui00ugxvd###APACHE_PID_FILE=/var/run/apache2/apache2.pid LDFLAGS=-Wl,-O1 -Wl,--hash-style=both HOSTNAME=511c592b839e APACHE_RUN_USER=www-data PHP_INI_DIR=/usr/local/etc/php PHP_ASC_URL=https://secure.php.net/get/php-5.6.28.tar.xz.asc/from/this/mirror CPPFLAGS=-fstack-protector-strong -fpic -fpie -O2 PHP_MD5=1e01c66b2e67ab3b56a6180ee560fe4c PHPIZE_DEPS=autoconf 		file 		g++ 		gcc 		libc-dev 		make 		pkg-config 		re2c capture_group_name=2 PHP_URL=https://secure.php.net/get/php-5.6.28.tar.xz/from/this/mirror APACHE_ENVVARS=/etc/apache2/envvars APACHE_LOG_DIR=/var/log/apache2 PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin GPG_KEYS=0BD78B5F97500D450838F95DFE857D9A90D90EC1 6E4F6AB321FDC07F2C332E3AC2BF0BC433CFC8B3 SUPERVISOR_GROUP_NAME=apache2 PWD=/var/www LANG=C APACHE_RUN_GROUP=www-data SUPERVISOR_ENABLED=1 SHLVL=0 PHP_SHA256=07187ba2870f89cef334cd2ad6cb801aeec5eaf283da0293a9a6be75d6786d11 CFLAGS=-fstack-protector-strong -fpic -fpie -O2 APACHE_CONFDIR=/etc/apache2 SUPERVISOR_PROCESS_NAME=apache2 SUPERVISOR_SERVER_URL=unix:///var/run/supervisor.sock PHP_EXTRA_BUILD_DEPS=apache2-dev APACHE_LOCK_DIR=/var/lock/apache2 APACHE_RUN_DIR=/var/run/apache2 PHP_VERSION=5.6.28 PHP_EXTRA_CONFIGURE_ARGS=--with-apxs2",
# "2023-11-01 09:11:48.175421180###apache2###13###>###open###/var/www/.htaccess###O_RDONLY|O_CLOEXEC###0###<NA>###<NA>###9###/usr/sbin/apache2###<NA>###<NA>###<NA>###<NA>###<NA>###511c592b839e###service52301ba394f348b4910d2509a416db24.1.ipmpus42fs5aajzxui00ugxvd###APACHE_PID_FILE=/var/run/apache2/apache2.pid LDFLAGS=-Wl,-O1 -Wl,--hash-style=both HOSTNAME=511c592b839e APACHE_RUN_USER=www-data PHP_INI_DIR=/usr/local/etc/php PHP_ASC_URL=https://secure.php.net/get/php-5.6.28.tar.xz.asc/from/this/mirror CPPFLAGS=-fstack-protector-strong -fpic -fpie -O2 PHP_MD5=1e01c66b2e67ab3b56a6180ee560fe4c PHPIZE_DEPS=autoconf 		file 		g++ 		gcc 		libc-dev 		make 		pkg-config 		re2c capture_group_name=2 PHP_URL=https://secure.php.net/get/php-5.6.28.tar.xz/from/this/mirror APACHE_ENVVARS=/etc/apache2/envvars APACHE_LOG_DIR=/var/log/apache2 PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin GPG_KEYS=0BD78B5F97500D450838F95DFE857D9A90D90EC1 6E4F6AB321FDC07F2C332E3AC2BF0BC433CFC8B3 SUPERVISOR_GROUP_NAME=apache2 PWD=/var/www LANG=C APACHE_RUN_GROUP=www-data SUPERVISOR_ENABLED=1 SHLVL=0 PHP_SHA256=07187ba2870f89cef334cd2ad6cb801aeec5eaf283da0293a9a6be75d6786d11 CFLAGS=-fstack-protector-strong -fpic -fpie -O2 APACHE_CONFDIR=/etc/apache2 SUPERVISOR_PROCESS_NAME=apache2 SUPERVISOR_SERVER_URL=unix:///var/run/supervisor.sock PHP_EXTRA_BUILD_DEPS=apache2-dev APACHE_LOCK_DIR=/var/lock/apache2 APACHE_RUN_DIR=/var/run/apache2 PHP_VERSION=5.6.28 PHP_EXTRA_CONFIGURE_ARGS=--with-apxs2",
# "2023-11-01 09:11:48.175433551###apache2###13###<###open###ENOENT###/var/www/.htaccess###O_RDONLY|O_CLOEXEC###0###/var/www/.htaccess###9###/usr/sbin/apache2###-2###<NA>###<NA>###<NA>###<NA>###511c592b839e###service52301ba394f348b4910d2509a416db24.1.ipmpus42fs5aajzxui00ugxvd###APACHE_PID_FILE=/var/run/apache2/apache2.pid LDFLAGS=-Wl,-O1 -Wl,--hash-style=both HOSTNAME=511c592b839e APACHE_RUN_USER=www-data PHP_INI_DIR=/usr/local/etc/php PHP_ASC_URL=https://secure.php.net/get/php-5.6.28.tar.xz.asc/from/this/mirror CPPFLAGS=-fstack-protector-strong -fpic -fpie -O2 PHP_MD5=1e01c66b2e67ab3b56a6180ee560fe4c PHPIZE_DEPS=autoconf 		file 		g++ 		gcc 		libc-dev 		make 		pkg-config 		re2c capture_group_name=2 PHP_URL=https://secure.php.net/get/php-5.6.28.tar.xz/from/this/mirror APACHE_ENVVARS=/etc/apache2/envvars APACHE_LOG_DIR=/var/log/apache2 PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin GPG_KEYS=0BD78B5F97500D450838F95DFE857D9A90D90EC1 6E4F6AB321FDC07F2C332E3AC2BF0BC433CFC8B3 SUPERVISOR_GROUP_NAME=apache2 PWD=/var/www LANG=C APACHE_RUN_GROUP=www-data SUPERVISOR_ENABLED=1 SHLVL=0 PHP_SHA256=07187ba2870f89cef334cd2ad6cb801aeec5eaf283da0293a9a6be75d6786d11 CFLAGS=-fstack-protector-strong -fpic -fpie -O2 APACHE_CONFDIR=/etc/apache2 SUPERVISOR_PROCESS_NAME=apache2 SUPERVISOR_SERVER_URL=unix:///var/run/supervisor.sock PHP_EXTRA_BUILD_DEPS=apache2-dev APACHE_LOCK_DIR=/var/lock/apache2 APACHE_RUN_DIR=/var/run/apache2 PHP_VERSION=5.6.28 PHP_EXTRA_CONFIGURE_ARGS=--with-apxs2"]

shell_script = "/root/sysdig_1107_match.sh" # 采集器脚本地址(sysdig采集器所在地址+名称)
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
