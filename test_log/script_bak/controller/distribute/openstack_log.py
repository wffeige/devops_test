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
import commands
import subprocess

base_dir = os.path.split(os.path.realpath(__file__))[0]
result_txt = '{base_dir}/var/result.txt'.format(base_dir=base_dir)
sort_res_txt = '{base_dir}/var/sort_result.txt'.format(base_dir=base_dir)
script = '{base_dir}/var/error_collect.sh'.format(base_dir=base_dir)
openstack_lst = ['/var/log/keystone', '/var/log/ceph', '/var/log/glance', '/var/log/cinder', '/var/log/nova','/var/log/nova/tmp', '/var/log/neutron']
logfile_lst1 = ['/var/log/messages', '/var/log/keepalived.log','/var/log/haproxy.log']
logfile_lst2 = ['/var/log/httpd/access_log','/var/log/httpd/every_test']
rabbitmq_log='/var/log/rabbitmq/rabbit@{hostname}.log'.format(hostname=socket.gethostname())

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
        return 0

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

    testlog_lst.remove('/var/log/nova/nova-manage.log')
    testlog_lst.remove('/var/log/keystone/keystone-tokenflush.log')
    # print "查询的日志列表:"
    # for i in testlog_lst:
    #     print i
    return testlog_lst

def generate_script():
    #输出openstack服务日志查询脚本
    file_lst = find_all_logfile()
    with open(script,'w') as e:
        e.write('> {result_txt}\n'.format(result_txt=result_txt))
        for i in file_lst:
            line="awk -F \" \" '{if ($1==\"%s\" &&   $2>=\"%s\" && $2<=\"%s\"  && $4 ==\"ERROR\") print $0}' %s >>%s"%(date,time_start,time_stop,i,result_txt)
            e.write(line+'\n')

def message_src():
    # 写lst1脚本
    with open(script,'a') as e :
        for logfile in logfile_lst1:
            line = "awk -F \" \" '{if ($1==\"%s\" && $2==\"%s\" &&$3>=\"%s\" && $3<=\"%s\") print $0}' %s >>%s"%(month,day,time_start,time_stop,logfile,result_txt)
            e.write(line+'\n')

def httpd_src():
    # 写http脚本22/Aug/2017:21:48:38

    times1 = "{}:{}".format(time_start.split(':')[0], time_start.split(':')[1])
    times2 = "{}:{}".format(time_stop.split(':')[0], time_stop.split(':')[1])

    with open(script, 'a') as e:
        for i in logfile_lst2:
            # line1 = "cat {log}| grep ERROR|egrep '{date}/{month}/2017:{times1}' >>{result_txt}".format(log=i, date=day, month=month, times1=times1, times2=times2,result_txt=result_txt)
            # line2 = "cat {log}| grep ERROR|egrep '{date}/{month}/2017:{times2}' >>{result_txt}".format(log=i, date=day, month=month, times1=times1, times2=times2,result_txt=result_txt)

            line2 = "cat {log}|grep '{day}-{month}-2017'|grep ERROR  >>{result_txt}".format(log=i,result_txt=result_txt,day=day,month=month)

            e.write(line2 + '\n')

def rabbitmq_src():
    # 写rabbitmq脚本    22-Aug-2017::18:48:39

    times1 = "{}:{}".format(time_start.split(':')[0],time_start.split(':')[1])
    times2 ="{}:{}".format(time_stop.split(':')[0], time_stop.split(':')[1])

    with open(script,'a') as e:
        # line1 = "cat {rabbitmq_log}| egrep 'ERROR'|egrep '{date}-{month}-2017::{times1}' >>{result_txt}".format(rabbitmq_log=rabbitmq_log,date=day,month=month,times1=times1,times2=times2,result_txt=result_txt)
        # line2 = "cat {rabbitmq_log}|egrep 'ERROR'| egrep '{date}-{month}-2017::{times2}' >>{result_txt}".format(rabbitmq_log=rabbitmq_log,date=day,month=month,times1=times1,times2=times2,result_txt=result_txt)
        line1 = "cat {log}|grep '{day}-{month}-2017'|grep ERROR  >>{result_txt}".format(log=rabbitmq_log, result_txt=result_txt,day=day, month=month)

        e.write(line1 + '\n')
        e.write('cat {result_txt} |sort -t " " -k2 > {sort_res_txt}'.format(result_txt=result_txt, sort_res_txt=sort_res_txt))

            
def main():
    generate_script()
    # httpd_src()
    # message_src()
    rabbitmq_src()

    try:
        cmd = '/bin/bash {script}'.format(script=script)
        status = shell(cmd,'s')
        print status
    except Exception as e:
        print e


if __name__ == "__main__":
    main()
