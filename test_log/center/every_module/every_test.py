# encoding:utf-8
#!/usr/bin/python
#Auther:test
#Time:2017-08-26
#Function:输入时间间隔，查询某个服务的错误日志总量,每个节点都会执行
#Example: python every_test.py 'nova' '2017-08-26' '00:00:00' '23:59:59'


import sys
import threading
import subprocess
import ansible.runner
import os
from time import ctime,sleep


try:
    module = sys.argv[1]
    date = sys.argv[2]
    time_start = sys.argv[3]
    time_stop = sys.argv[4]
except Exception as e:
    # print e
    print "缺少参数!\nUsage: python every_test.py [module] [date] [start_time]  [stop_time] \nExample: python every_test.py 'nova' '2017-08-22' '00:00:00'  '23:59:59'"
    sys.exit(1)

def shell(cmd, type='s'):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        p_status = p.wait()
        if type == 's':
            return p_status
        elif type == 'r':
            print  p.stdout.readline()
            return p.stdout.readline()

            # return output.strip()
    except Exception, e:
        return 0



def command(pattern, module, args, fork):
    results = ansible.runner.Runner(pattern=pattern, forks=fork,module_name=module, module_args=args,).run()

    for (hostname, result) in results['contacted'].items():
        try:
            if not 'failed' in result:
                print "{} execute is ok!".format(hostname)
        except Exception, e:
            print e
            sys.exit(1)


def execute():
    # command(pattern, module, args, fork)

    threads = []
    t1 = threading.Thread(target=command, args=('172.16.1.134', 'command', 'python /root/devops/scripts/log_analyze/every_test/query_error_log.py {module} {date} {start_time} {stop_time}'.format(date=date,start_time=time_start,stop_time=time_stop,module=module), 1))
    threads.append(t1)

    t2 = threading.Thread(target=command, args=('172.16.1.135', 'command', 'python /root/devops/scripts/log_analyze/every_test/query_error_log.py  {module} {date} {start_time} {stop_time}'.format(date=date,start_time=time_start,stop_time=time_stop,module=module), 1))
    threads.append(t2)

    t4 = threading.Thread(target=command, args=('172.16.1.136', 'command', 'python /root/devops/scripts/log_analyze/every_test/query_error_log.py  {module} {date} {start_time} {stop_time}'.format(date=date,start_time=time_start,stop_time=time_stop,module=module), 1))
    threads.append(t4)

    t3 = threading.Thread(target=command, args=('172.16.1.138', 'command', 'python /root/devops/scripts/log_analyze/every_test/query_error_log.py  {module} {date} {start_time} {stop_time}'.format(date=date,start_time=time_start,stop_time=time_stop,module=module), 1))
    threads.append(t3)

    for t in threads:
        t.setDaemon(True)
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()
    # print "Exiting Main Thread"




def collect():

    cmd1 = "scp 172.16.1.134:/root/devops/scripts/log_analyze/every_test/var/{}_result.txt /root/devops/scripts/center/every_module/var/134_{}.txt".format(module,module)
    cmd2 = "scp 172.16.1.135:/root/devops/scripts/log_analyze/every_test/var/{}_result.txt /root/devops/scripts/center/every_module/var/135_{}.txt".format(module, module)
    cmd3 = "scp 172.16.1.136:/root/devops/scripts/log_analyze/every_test/var/{}_result.txt /root/devops/scripts/center/every_module/var/136_{}.txt".format(module, module)
    cmd4 = "scp 172.16.1.138:/root/devops/scripts/log_analyze/every_test/var/{}_result.txt /root/devops/scripts/center/every_module/var/138_{}.txt".format(module, module)

    shell(cmd1)
    shell(cmd2)
    shell(cmd3)
    shell(cmd4)


if __name__ == "__main__":
    execute()
    collect()

