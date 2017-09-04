# coding:utf-8
# !/usr/bin/python
# Auther:wangfei
# Function:自动发现当前路径下所有的.log文件，然后遍历符合要求的日志文件进行处理
# Date:2017-08-25
# Usage: python walker.py '2017-08-09' '2017-08-10'

'''
为了满足测试需求，遍历所有的日志文件，过滤信息，然后统一追加到同一文件，将日志的行数进行校验
测试命令： awk  '/start_key/,/stop_key/{print}' logfile >>result.txt
'''

import os
import re
import sys
import socket
import subprocess
base_dir = os.path.split(os.path.realpath(__file__))[0]


openstack_dic = {"keystone":"/var/log/keystone","ceph":"/var/log/ceph","glance":"/var/log/glance","cinder":"/var/log/cinder","nova":"/var/log/nova","neutron":"/var/log/neutron","libvirt":"/var/log/libvirt"}

try:
    month = 'Aug'
    service = sys.argv[1]
    date = sys.argv[2]
    day = date.split('-')[2]
    time_start = sys.argv[3]
    time_stop = sys.argv[4]

    if service not in openstack_dic.keys():
        print "{} is not in query range.".format(service)
        sys.exit()
except IndexError as e:
    print "当前脚本仅支持测试当天数据!\nUsage: python script.py [service]  [date]  [start_time]  [stop_time] \nExample: python script.py 'nova' '2017-08-22' '00:00:00'  '00:01:00'"
    sys.exit()






def find_all_logfile(path):
    file_lst = []
    # for per_dir in log_lst:
    #     print per_dir
    for file in os.walk(path):
        file_lst1 = map(lambda x: file[0] + '/' + x, file[-1])
        file_lst.extend(file_lst1)

    logfile_lst = []
    for i in file_lst:
        # if re.match(r'.*.log$', i) or re.match(r'.*.log-[0-9]{8}',i):
        if re.match(r'.*.log$', i):

            logfile_lst.append(i)

    if '/var/log/nova/nova-manage.log' in logfile_lst:
        logfile_lst.remove('/var/log/nova/nova-manage.log')
    elif '/var/log/keystone/keystone-tokenflush.log' in logfile_lst:
        logfile_lst.remove('/var/log/keystone/keystone-tokenflush.log')

    # for i in logfile_lst:
    #     print i

    return logfile_lst


def shell(cmd, type='s'):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        p_status = p.wait()
        if type == 's':
            return p_status
        elif type == 'r':
            return output.strip()
    except Exception, e:
        return 0

def exec_src(script_name):
    try:
        cmd = '/bin/bash {script}'.format(script=script_name)
        status = shell(cmd, 's')
        print status
    except Exception as e:
        print e



def generate_script(service_lst):

    dir_path = openstack_dic[service]
    dir_var_path = "{base_dir}/var/".format(base_dir=base_dir)

    result_txt = '{}{}_result.txt'.format(dir_var_path,service)
    scripts = '{}{}_query.sh'.format(dir_var_path,service)

    if not os.path.exists(dir_var_path):
        os.makedirs(dir_var_path)

    file_lst = find_all_logfile("{}".format(dir_path))


    with open(scripts,'w') as e:
        e.write('> {result_txt}\n'.format(result_txt=result_txt))
        for i in file_lst:
            line = "awk -F \" \" '{if ($1==\"%s\" &&   $2>=\"%s\" && $2<=\"%s\"   && $4 ==\"ERROR\" ) print $0}' %s >>%s" % (date, time_start, time_stop, i,result_txt )
            e.write(line+'\n')
    # exec(scripts)

    cmd = '/bin/bash {script}'.format(script=scripts)
    shell(cmd,'r')
    cmd = 'cat {result_txt}|wc -l'.format(result_txt=result_txt)
    num = shell(cmd, 'r')
    print "The {} log has {} rows".format(service,num)










def main():


    generate_script(service)





if __name__ == "__main__":
    main()



