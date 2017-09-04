#!/usr/bin/env python
# -*- coding:utf8 -*-
'''
get the MEM used
    --opt=used

swap默认是关闭的，所以没有监控

'''
import os, sys, tempfile
from common_zabbix import deco_head, logger, shell, TmpFile

base_dir = os.path.split(os.path.realpath(__file__))[0]
logfile = r'%s/logs/%s.log' % (base_dir, os.path.basename(__file__).split('.')[0])
cache_file = r'%s/var/%s.tmp' % (base_dir, os.path.basename(__file__).split('.')[0])

def mem_num():
    '''
    use command 'free -m|grep 'buffers/cache'|awk '{print $NF}''
    '''
    cmd = r"free -m|grep 'buffers/cache'|awk '{print $NF}'"
    mem_str = shell(cmd, 'r')
    return int(mem_str)
    
@deco_head(logfile)
def main(opt,discovery_value, logging):
    if opt == 'free':
        print mem_num()
    else:
        print 0

if __name__ == '__main__':
    main()
