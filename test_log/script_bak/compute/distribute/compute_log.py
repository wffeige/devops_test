#coding:utf-8
#!/usr/bin/python
#Auther:wangfei
#Function:自动发现当前路径下所有的.log文件，然后遍历符合要求的日志文件进行处理
#Date:2017-08-10
#Usage: python walker.py '2017-08-09' '2017-08-10'

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
result_txt = '{base_dir}/var/result.txt'.format(base_dir=base_dir)
sort_res_txt = '{base_dir}/var/sort_result.txt'.format(base_dir=base_dir)
script = '{base_dir}/var/compute_collect.sh'.format(base_dir=base_dir)
openstack_lst = ['/var/log/keystone','/var/log/ceph','/var/log/libvirt/qemu/','/var/log/cinder','/var/log/nova','/var/log/neutron']
logfile_lst1 = ['/var/log/messages']

try:
    month = 'Aug'
    date = sys.argv[1]
    day = date.split('-')[2]
    time_start = sys.argv[2]
    time_stop = sys.argv[3]
except IndexError as e:
    print "当前脚本仅支持测试当天数据!\nUsage: python script.py  [date] [start_time]  [stop_time] \nExample: python script.py '2017-08-22' '00:00:00'  '00:01:00'"
    sys.exit()


def shell(cmd, type = 's'):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        p_status = p.wait()
        if type == 's':
            return p_status
        elif type == 'r':
            return output.strip()
    except Exception, e:
        return 


def find_all_logfile():

    file_lst = [] 
    for per_dir in openstack_lst:
        for file in os.walk(per_dir):
            file_lst1 = map(lambda x:per_dir+'/'+x, file[-1])	
            file_lst.extend(file_lst1)

    testlog_lst = []
    for i in file_lst:
        if re.match(r'.*.log$',i):
            testlog_lst.append(i)

    return testlog_lst


def generate_script():
    #输出openstack服务日志查询脚本
    file_lst = find_all_logfile()
    with open(script,'w') as e:
        e.write('> {result_txt}\n'.format(result_txt=result_txt))
        for i in file_lst:
            line="awk -F \" \" '{if ($1==\"%s\" &&   $2>=\"%s\" && $2<=\"%s\" &&$4==\"ERROR\") print $0}' %s >>%s"%(date,time_start,time_stop,i,result_txt)
            e.write(line+'\n')
        e.write('cat {result_txt} |sort -t " " -k2 > {sort_res_txt}'.format(result_txt=result_txt, sort_res_txt=sort_res_txt))




def main():
    generate_script()

    try:
        cmd = '/bin/bash {script}'.format(script=script)
        status = shell(cmd,'s')
        print status
    except Exception as e:
        print e

if __name__ == "__main__":
    main()
