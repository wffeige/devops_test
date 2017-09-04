# coding:utf-8
# !/usr/bin/python
# Auther:wangfei
# Function:自动发现当前路径下所有的.log文件，然后遍历符合要求的日志文件进行处理
# Date:2017-08-24
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
result_con_rel = '{base_dir}/var/result_con_rel.txt'.format(base_dir=base_dir)
result_con_err = '{base_dir}/var/result_con_err.txt'.format(base_dir=base_dir)
sort_res_txt = '{base_dir}/var/sort_result.txt'.format(base_dir=base_dir)
script_err = '{base_dir}/var/error_log_collect.sh'.format(base_dir=base_dir)
script_rel = '{base_dir}/var/relation_log_collect.sh'.format(base_dir=base_dir)

#控制节点需要查询的日志目录
controller_openstack_lst =['/var/log/keystone', '/var/log/ceph', '/var/log/glance', '/var/log/cinder', '/var/log/nova', '/var/log/neutron','/var/log/libvirt/qemu']
controller_other_lst = ['/var/log/messages', '/var/log/keepalived.log', '/var/log/haproxy.log']
controller_httpd_lst = ['/var/log/httpd/access_log', '/var/log/httpd/every_test']
rabbitmq_log = '/var/log/rabbitmq/rabbit@{hostname}.log'.format(hostname=socket.gethostname())
openstack_dict = {"keystone":"/var/log/keystone","ceph":"/var/log/ceph","glance":"/var/log/glance","cinder":"/var/log/cinder","nova":"/var/log/nova","neutron":"/var/log/neutron","libvirt":"/var/log/libvirt"}


#计算节点需要查询的日志目录
#目前计算节点的目录已经被控制节点的目录涵盖，
# compute_openstack_lst = ['/var/log/ceph','/var/log/neutron','/var/log/libvirt/qemu','/var/log/cinder','/var/log/nova']
# compute_other_lst =['/var/log/messages']
# result_com_rel = '{base_dir}/var/result_com_rel.txt'.format(base_dir=base_dir)
# result_com_err = '{base_dir}/var/result_com_err.txt'.format(base_dir=base_dir)



try:
    month = 'Aug'
    date = sys.argv[1]
    day = date.split('-')[2]
    time_start = sys.argv[2]
    time_stop = sys.argv[3]
except IndexError as e:
    print "当前脚本仅支持测试当天数据!\nUsage: python script.py  [date] [start_time]  [stop_time] \nExample: python script.py '2017-08-22' '00:00:00'  '00:01:00'"
    sys.exit()


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


def find_all_logfile(log_lst):
    file_lst = []
    for per_dir in log_lst:
        print per_dir
        for file in os.walk(per_dir):
            file_lst1 = map(lambda x: file[0] + '/' + x, file[-1])
            file_lst.extend(file_lst1)

    logfile_lst = []
    for i in file_lst:
        if re.match(r'.*.log$', i):
            logfile_lst.append(i)

    if '/var/log/nova/nova-manage.log' in logfile_lst:
        logfile_lst.remove('/var/log/nova/nova-manage.log')
    elif '/var/log/keystone/keystone-tokenflush.log' in logfile_lst:
        logfile_lst.remove('/var/log/keystone/keystone-tokenflush.log')

    for i in logfile_lst:
        print i
    return logfile_lst


class Controller_Node(object):
    def __init__(self):
        self.opestack_logfile_lst = find_all_logfile(controller_openstack_lst)
        self.rel_num = 0
        self.err_num = 0
        with open(script_rel, 'w') as e:
            e.write('> {result_txt}\n'.format(result_txt=result_con_rel))
        with open(script_err, 'w') as e:
            e.write('> {result_txt}\n'.format(result_txt=result_con_err))

    def generate_script_rel(self):
        file_lst = self.opestack_logfile_lst
        self.rel_num += 1
        with open(script_rel, 'a') as e:
            for i in file_lst:
                line = "awk -F \" \" '{if ($1==\"%s\" &&   $2>=\"%s\" && $2<=\"%s\" ) print $0}' %s >>%s" % (
                date, time_start, time_stop, i, result_con_rel)
                e.write(line + '\n')


    def message_src_rel(self):
        self.rel_num += 1
        with open(script_rel, 'a') as e:
            for logfile in controller_other_lst:
                line = "awk -F \" \" '{if ($1==\"%s\" && $2==\"%s\" &&$3>=\"%s\" && $3<=\"%s\") print $0}' %s >>%s" % (month, day, time_start, time_stop, logfile, result_con_rel)
                e.write(line + '\n')


    def httpd_src_rel(self):
        self.rel_num += 1
        times1 = "{}:{}".format(time_start.split(':')[0], time_start.split(':')[1])
        times2 = "{}:{}".format(time_stop.split(':')[0], time_stop.split(':')[1])

        with open(script_rel, 'a') as e:
            for i in controller_httpd_lst:
                line1 = "cat {log}| egrep '{date}/{month}/2017:{times1}' >>{result_txt}".format(log=i, date=day,month=month, times1=times1,times2=times2,result_txt=result_con_rel)
                line2 = "cat {log}| egrep '{date}/{month}/2017:{times2}' >>{result_txt}".format(log=i, date=day,month=month, times1=times1,times2=times2,result_txt=result_con_rel)
                e.write(line1 + '\n' + line2 + '\n')

    def rabbitmq_src_rel(self):
        self.rel_num += 1
        times1 = "{}:{}".format(time_start.split(':')[0], time_start.split(':')[1])
        times2 = "{}:{}".format(time_stop.split(':')[0], time_stop.split(':')[1])

        with open(script_rel, 'a') as e:
            line1 = "cat {rabbitmq_log}| egrep '{date}-{month}-2017::{times1}' >>{result_txt}".format(
                rabbitmq_log=rabbitmq_log, date=day, month=month, times1=times1, times2=times2,
                result_txt=result_con_rel)
            line2 = "cat {rabbitmq_log}| egrep '{date}-{month}-2017::{times2}' >>{result_txt}".format(
                rabbitmq_log=rabbitmq_log, date=day, month=month, times1=times1, times2=times2,
                result_txt=result_con_rel)
            e.write(line1 + '\n' + line2 + '\n')
            e.write('sed -i "s/{} {}/{}/" {} \n'.format(month, day, date, result_con_rel))


    def generate_script_err(self):
        self.err_num += 1
        file_lst = self.opestack_logfile_lst
        with open(script_err, 'w') as e:
            e.write('> {result_txt}\n'.format(result_txt=result_con_err))
            for i in file_lst:
                line = "awk -F \" \" '{if ($1==\"%s\" &&   $2>=\"%s\" && $2<=\"%s\"  && $4 ==\"ERROR\") print $0}' %s >>%s" % (date, time_start, time_stop, i, result_con_err)
                e.write(line + '\n')


    def rabbitmq_src_err(self):
        self.err_num += 1
        times1 = "{}:{}".format(time_start.split(':')[0], time_start.split(':')[1])
        times2 = "{}:{}".format(time_stop.split(':')[0], time_stop.split(':')[1])

        with open(script_err, 'a') as e:
            line1 = "cat {log}|grep '{day}-{month}-2017'|grep ERROR  >>{result_txt}".format(log=rabbitmq_log,result_txt=result_con_err,day=day, month=month)
            e.write(line1 + '\n')

    def __del__(self):
        if self.rel_num > 0:
            with open(script_rel, 'a') as e:
                e.write('cat {result_txt} |sort -t " " -k2 > {sort_res_txt}'.format(result_txt=result_con_rel,
                                                                                    sort_res_txt=sort_res_txt))
            exec_src(script_rel)
        elif self.err_num > 0:
            with open(script_err, 'a') as e:
                e.write('cat {result_txt} |sort -t " " -k2 > {sort_res_txt}'.format(result_txt=result_con_err,
                                                                                    sort_res_txt=sort_res_txt))
            exec_src(script_err)  #执行脚本




# class Coompute_Node(object):
#
#     def __init__(self):
#         self.openstack_logflie_lst  = find_all_logfile(compute_openstack_lst)
#         self.rel_num = 0
#         self.err_num = 0
#
#     def generate_script_rel(self):
#
#         self.rel_num += 1
#         with open(script_rel, 'w') as e:
#             e.write('> {result_txt}\n'.format(result_txt=result_com_rel))
#             for i in self.openstack_logflie_lst:
#                 line = "awk -F \" \" '{if ($1==\"%s\" &&   $2>=\"%s\" && $2<=\"%s\" ) print $0}' %s >>%s" % (date, time_start, time_stop, i, result_com_rel)
#                 e.write(line + '\n')
#             # e.write('cat {result_txt} |sort -t " " -k2 > {sort_res_txt}'.format(result_txt=result_com_rel,
#                                                                                 # sort_res_txt=sort_res_txt))
#
#     def message_src_rel(self):
#         self.rel_num += 1
#         with open(script_rel, 'a') as e:
#             for logfile in compute_other_lst:
#                 line = "awk -F \" \" '{if ($1==\"%s\" && $2==\"%s\" &&$3>=\"%s\" && $3<=\"%s\") print $0}' %s >>%s" % (month, day, time_start, time_stop, logfile, result_com_rel)
#                 e.write(line + '\n')
#
#     def generate_script_err(self):
#         self.err_num += 1
#         with open(script_err, 'w') as e:
#             e.write('> {result_txt}\n'.format(result_txt=result_com_err))
#             for i in self.openstack_logflie_lst:
#                 line = "awk -F \" \" '{if ($1==\"%s\" &&   $2>=\"%s\" && $2<=\"%s\" &&$4==\"ERROR\") print $0}' %s >>%s" % (date, time_start, time_stop, i, result_com_err)
#                 e.write(line + '\n')
#
#
#     def __del__(self):
#         if self.rel_num > 0:
#             with open(script_rel, 'a') as e:
#                 e.write('cat {result_txt} |sort -t " " -k2 > {sort_res_txt}'.format(result_txt=result_com_rel,
#                                                                                     sort_res_txt=sort_res_txt))
#             exec_src(script_rel)
#         elif self.err_num > 0:
#             with open(script_err, 'a') as e:
#                 e.write('cat {result_txt} |sort -t " " -k2 > {sort_res_txt}'.format(result_txt=result_com_err,
#                                                                                     sort_res_txt=sort_res_txt))
#             exec_src(script_err)
