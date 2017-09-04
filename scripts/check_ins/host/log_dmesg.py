#!/usr/bin/python

import os, sys, tempfile
from common_zabbix import deco_head, logger, shell, TmpFile

base_dir = os.path.split(os.path.realpath(__file__))[0]
var_dir = r'%s/var' % base_dir
logfile = r'%s/logs/%s.log' % (base_dir, os.path.basename(__file__).split('.')[0])
cache_file = r'%s/var/%s.tmp' % (base_dir, os.path.basename(__file__).split('.')[0])



def dmesg():
    cmd=r'dmesg |grep error|wc -l'
    cpu_str = shell(cmd, 'r')
    print cpu_str

dmesg()
