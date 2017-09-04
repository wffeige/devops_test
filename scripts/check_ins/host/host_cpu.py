#!/usr/bin/env python
# -*- coding:utf8 -*-
'''
get the CPU used (per second)
    --opt=used

get the CPU nice (per second)
    --opt=nice

get the CPU system (per second)
    --opt=system

get the CPU iowait (per second)
    --opt=iowait

get the CPU steal (per second)
    --opt=steal

get the CPU user (per second)
    --opt=user

'''

import os, sys, re
from common_zabbix import deco_head, logger, shell, TmpFile

base_dir = os.path.split(os.path.realpath(__file__))[0]
cache_file = r'%s/var/%s.tmp' % (base_dir, os.path.basename(__file__).split('.')[0])
logfile = r'%s/logs/%s.log' % (base_dir, os.path.basename(__file__).split('.')[0])

def cpu_dict():
    '''
    use command 'iostat -x 1 2', get the last value (avg value)
    '''
    second = 2
    #cmd = r'iostat -x 1 %s' %second
    cmd = r'iostat -x 1 2'
    cpu_str = shell(cmd, 'r')
    keylist, valuelist = [], []
    count = 0
    try:
        for line in cpu_str.split('\n'):
            if line.strip() == '': continue
            if "avg-cpu:" in line:
                count += 1
                if count != second: continue
                keylist = line.strip().split()
            elif len(keylist) != 0:
                valuelist = line.strip().split() 
                break
        cpu_dict = dict(zip(keylist[1:], valuelist))
    except:
        return 0.0
    return cpu_dict

def max_cpu():
    '''
    use command 'mpstat -P ALL 1 2', get second value 
    '''
    second = 2
    count = 0
    second_cpu_lst = []
    cmd = r'mpstat -P ALL 1 2'
    max_cpu_str = shell(cmd, 'r')
    for line in max_cpu_str.split('\n'):
        if line.strip() == '':
            count += 1
        if count == 2:
            if line and re.match(r'[0-9]', line.split()[-1]):
                second_cpu_lst.append(line.split()[-1])
        second_cpu_float = [float(i) for i in second_cpu_lst]
    second_cpu_float.sort()
    return 100 - second_cpu_float[0]


def cpu_load():
	cmd =r"uptime|awk -F 'load average:' '{print $2}'|awk -F ',' '{print $1}'"
	#cmd =r'iostat -xm 1 2'
	load_str = shell(cmd, 'r')
	#print load_str
	return float(load_str)






@deco_head(logfile)
def main(opt, discovery, logging):
    cache = TmpFile(cache_file)
    if opt == 'used':
        cpu_info_dict = cpu_dict()
        if isinstance(cpu_info_dict, dict):
            print 100 - float(cpu_info_dict['%idle'])
        else:
            logging.error("CPU get error, check 'iostat -x 1 2' pls.")
            cpu_info_dict = ''
            print 0.0
        ###cache
        cache.recode_info(str(cpu_info_dict.items()))
    elif opt == 'maxcpu':
        print max_cpu()
    else:
        cpu_info_dict = cache.get_content()
        if opt == 'nice':
            print float(cpu_info_dict.setdefault('%nice', 0))
        elif opt == 'system':
            print float(cpu_info_dict.setdefault('%system', 0))
        elif opt == 'iowait':
            print float(cpu_info_dict.setdefault('%iowait', 0))
        elif opt == 'steal':
            print float(cpu_info_dict.setdefault('%steal', 0))
        elif opt == 'user':
            print float(cpu_info_dict.setdefault('%user', 0))
        elif opt == 'load':
            print cpu_load()
        else:
            print 0.0

if __name__ == '__main__':
    main()
