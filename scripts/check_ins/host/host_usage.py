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
    cmd=r'df -Th|grep -E "ext4|zfs"|tr -s " " ","'
    cmdout = shell(cmd, 'r')
    lineslist = cmdout.strip().split('\n')
    linenum = 0
    li=[]
    for i in lineslist:
        i=i.split(',')
        li.append(i[0])
    listlen = len(li)
    for line in li:
        linenum += 1
        if linenum != listlen:
            print '''\t\t{"{#FILESYS}": "%s"},''' % line
        else:
            print '''\t\t{"{#FILESYS}": "%s"}''' % line
    print '''\t]\n}'''

def disk_dict(filesys):
    cmd=r'df -Th|grep -E "Filesystem|%s"|tr -s " " ","'%filesys
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
        if opt == 'usage':
            disk_info_dict = disk_dict(discovery)
            if isinstance(disk_info_dict, dict):
                use=disk_info_dict['Use%']
                use=str(use)
                use=use.replace('%','')
                use=int(use)
                print use
            else:
                print 0.0
            cache.recode_info(str(disk_info_dict.items()))




if __name__ == '__main__':
    main()


