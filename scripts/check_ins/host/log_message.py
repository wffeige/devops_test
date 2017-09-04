#!/usr/bin/python
'''
python log_message.py --opt=1
'''

import time,re,os,commands
import subprocess
from  common_zabbix import *

base_dir = os.path.split(os.path.realpath(__file__))[0]
var_dir = r'%s/var' % base_dir
logfile = r'%s/logs/%s.log' % (base_dir, os.path.basename(__file__).split('.')[0])
cache_file = r'%s/var/%s.tmp' % (base_dir, os.path.basename(__file__).split('.')[0])

@deco_head(logfile)
def message(opt,discovery,logging):
    if re.match("[0-9]",opt):
        try:
            range_time=int(opt)*60*60*24
            pass_time=time.time()-range_time
            a=time.ctime(pass_time)
            a=a.split(' ')
            if a[2] == '':
                a.remove('')
                sed1="%s  %s"%(a[1],a[2])
            else:
                sed1="%s %s"%(a[1],a[2])
        except Exception as e:
            logging.error("mseeage log no this day")
            print e
        try:

            result=commands.getoutput("cat /var/log/messages*|sed -rn '/%s/,$p'|grep -v ^$|grep -v ^#|grep ERROR"%sed1)   
            result1=result.split('\n')

            count=0
            for i in result1:
                if i != '':
                    count+=1
                    print i
            print count     

        except Exception as e:
            logging.error(e)    
                
message()
