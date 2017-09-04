# encoding:utf-8
#!/usr/bin/python
#Auther:test
#Time:2017-08-26
#Function:输入时间间隔，查询某个服务的错误日志总量,每个节点都会执行
#Example: python every_test.py 'nova' '2017-08-26' '00:00:00' '23:59:59'


import os
import sys
import time
import socket
import threading
import subprocess
import ansible.runner
from time import ctime,sleep

machine_lst=['172.16.1.134','172.16.1.135','172.16.1.136','172.16.1.138']


# controller_log = {'neutron':'/var/log/neutron/server.log','nova':'/var/log/nova/nova-scheduler.log','keystone':'/var/log/keystone/keystone.log','cinder':'/var/log/cinder/scheduler.log'}
controller_log = {'neutron':'/var/log/nova/nova-scheduler.log'}

# =ERROR REPORT==== 28-Aug-2017::11:10:29 ===
# This is a test
rabbitmq_log = '/var/log/rabbitmq/rabbit@{hostname}.log'.format(hostname=socket.gethostname())

compute_log = []

time_log = time.strftime('%H:%M:%S:',time.localtime(time.time()))
cmd = "echo '' >>{}"


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
    results = ansible.runner.Runner(pattern=pattern, forks=fork,module_name=module, module_args=args).run()

    for (hostname, result) in results['contacted'].items():
        try:
            if not 'failed' in result:
                print "{} execute is ok!".format(hostname)
        except Exception, e:
            print e
            sys.exit(1)

#2017-08-26 00:00:00.249 23789 DEBUG keystone.middleware.core
# 2017-08-26 17:37:28.064 3321 DEBUG nova.servicegroup.drivers.db [-] Report
#2017-08-26 03:22:08.558 7721 ERROR neutron.wsgi [-] 172.16.1.136 - - [26/Aug/2017 03:22:08] "OPTIONS / HTTP/1.0" 200 263 0.000478

def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - long(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp

def generate_log(host,num):


    for log  in  controller_log.values():
        for i in range(num):
            # row_time = time.strftime('%H:%M:%S', time.localtime(time.time()))

            row_info = "{row_time} 23789 ERROR nova.metadata.wsgi.server [-] This is a test".format(row_time=get_time_stamp())
            cmd = 'echo  "{row_info}"   >> {log}'.format(row_info=row_info,log=log)
            # command(host,"command",cmd,1)
            shell(cmd)
            print cmd


def main():
    generate_log('172.16.1.136',10)


if __name__ == '__main__':
    main()