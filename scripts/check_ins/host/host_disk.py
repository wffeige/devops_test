#!/usr/bin/env python
# -*- coding:utf8 -*-
'''
discovery
    --opt=discovery

get the %util of disk
    --opt=util --descovery=$1

get the %iops of disk
    --opt=util --descovery=$1

get the %throughput of disk
    --opt=throughput --descovery=$1
'''
import os, sys, tempfile
from common_zabbix import deco_head, logger, shell, TmpFile

base_dir = os.path.split(os.path.realpath(__file__))[0]
logfile = r'%s/logs/%s.log' % (base_dir, os.path.basename(__file__).split('.')[0])
cache_file = r'%s/var/%s.tmp' % (base_dir, os.path.basename(__file__).split('.')[0])


def discovery_info():
    '''
    discovery the active disk, output with json format
    '''
    print "{";
    print '''\t"data":['''
    cmd = r"iostat -x 1 2|grep -Ev 'avg-cpu:|Device:|Linux|^$'|grep -v ^' '|awk '{print $1}'|sort|uniq"
    cmdout = shell(cmd, 'r')
    lineslist = cmdout.strip().split('\n')
    aset = set()
    linenum = 0
    for line in lineslist:
        if line.strip() == '': continue
        aset.add(line.strip())
    listlen = len(aset)    
    for line in aset:
        linenum += 1
        if linenum != listlen:
            print '''\t\t{"{#DISK}": "%s"},''' % line
        else:
            print '''\t\t{"{#DISK}": "%s"}''' % line
    print '''\t]\n}'''


def iostat_dict(ifname):
    '''
    use command 'iostat -x 1 2', get info
    '''
    cmd = r'iostat -xmd 1 2 '
    #cmd=r"iostat -x 1 2"
    disk_str = shell(cmd, 'r')
    disk_lst = []
    for line in disk_str.split('\n'):
        if line == '':
            disk_lst = []
        else:
            disk_lst.append(line)
    try:
        title_lst = disk_lst[0].split()[1:]
        values_lst = [i.split() for i in disk_lst if ifname in i.split()][0][1:]
        iostat_dict = dict(zip(title_lst, values_lst))
    except:
        return
    #print iostat_dict
    #print type(iostat_dict)
    return iostat_dict

def max_diskusage():
    cmd=r"df -Th|tail -n +2|awk '{print $6}'"
    zfs_str = shell(cmd, 'r')
    zfs_str=zfs_str.replace('%','')
    zfs_str=zfs_str.split('\n')
    try:
        li=[]
        for i in zfs_str:
            li.append(i)
        return max(li)
    except Exception as e:
        pass



def diskuse():
    cmd=r'df -Th|grep -E "Filesystem|zfs"|tr -s " " ","'
    zfs_str = shell(cmd, 'r')
    keylist, valuelist = [], []
    try:
        count=0
        for line in zfs_str.split('\n'):
            line=line.split(',')
            count += 1
            if count<2:
                keylist=line
            else:
                valuelist=line
        disk_dict = dict(zip(keylist, valuelist))
    except Exception as e:
        logging.error(e)
    return disk_dict




@deco_head(logfile)
def main(opt, discovery, logging):
    if opt == 'discovery':
        discovery_info()
    else:
        cache = TmpFile(cache_file)
        if opt == 'util':
            disk_info_dict = iostat_dict(discovery)
            if isinstance(disk_info_dict, dict):
                print float(disk_info_dict['%util'])
            else:
                logging.error("Network get error, check 'sar -n DEV 1 2' pls.")
                disk_info_dict = ''
                print 0.0
            ###cache
            #print disk_info_dict
            #print type(disk_info_dict)
            cache.recode_info(str(disk_info_dict.items()))
        else:
            disk_info_dict = cache.get_content()
            #print disk_info_dict
            
            if opt == 'rtps':
                print float(disk_info_dict.setdefault('r/s', 0))
            elif opt == 'wtps':
                print float(disk_info_dict.setdefault('w/s', 0))
            elif opt == 'rmps':
                print float(disk_info_dict.setdefault('rMB/s', 0))
            elif opt == 'wmps':
                print float(disk_info_dict.setdefault('wMB/s', 0))
            elif opt == 'await':
                print float(disk_info_dict.setdefault('await', 0))
            elif opt == 'svctm':
                print float(disk_info_dict.setdefault('svctm', 0))
            elif opt == 'throughput':
                print float(disk_info_dict['rMB/s'])+float(disk_info_dict['wMB/s'])
            elif opt == 'iops1':
                print float(disk_info_dict['r/s'])+float(disk_info_dict['w/s'])
            elif opt == 'max_usage':
                maxuse=max_diskusage()
                maxuse=int(maxuse)
                print maxuse

            else:
                print 0.0

if __name__ == '__main__':
    main()

