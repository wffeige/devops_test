#!/usr/bin/env python

'''
get QPS                 
    --opt=QPS

get TPS                 
    --opt=TPS

get hit                 
    --opt=hit

get dead_lock_status    
    --opt=deadlock

get slave_status        
    --opt=slave_status

get dbsize              
    --opt=dbsize

get alive_status        
    --opt=alive_status

get data_status      (judje the mysql info is new or old)   
    --opt=data_status
'''

import time, sys, os,syslog,subprocess,os, sys, getopt, subprocess, json
from common_zabbix import deco_head, logger, shell

base_dir = os.path.split(os.path.realpath(__file__))[0]
logfile = r'%s/logs/%s.log' % (base_dir, os.path.basename(__file__).split('.')[0])
cache_file = r'%s/var/%s.tmp' % (base_dir, os.path.basename(__file__).split('.')[0])
#logging = logger(logfile)

@deco_head(logfile)
def main(opt,logging):
    try:
        state='Null'
        if os.path.exists('%s/var/mysql_status_new.txt'%base_dir):

            file1=open('%s/var/mysql_status_new.txt'%base_dir,'r')
            a=file1.readlines()    
            a=str(a)
            a=a.replace('\\n','')
            a=a.replace('[','')
            a=a.replace(']','')
            a=a.replace("'","")
            a=a.split(',')
            valuelist=a
            keylist=['QPS','TPS','hit','dbsize','alive_status','slave_status','dead_lock_status','time_data']
            info=dict(zip(keylist,valuelist))
            file1.close()
        else:
            info={'hit': ' 85.61%', 'dead_lock_status': ' 0', 'alive_status': ' 0', 'TPS': ' 0','slave_status': ' 0', 'dbsize': ' 0.56', 'QPS': '0'}
            logging.error("can't connect mysql")
    except Exception as e:
        logging.info(e)


    time_current=time.strftime("%H%M")
    time_current=int(time_current)
    time_data=int(info['time_data'])

    try :
        if opt == 'QPS':
            print float(info['QPS'])
        elif opt == 'TPS':
            print float(info['TPS'])
        elif opt == 'hit':
            print float(info['hit'])
        elif opt == 'deadlock':
            print info['dead_lock_status']
        elif opt == 'slave_status':
            print info['slave_status']
        elif opt == 'dbsize':
            print float(info['dbsize'])
        elif opt == 'alive_status':
            print info['alive_status']
        elif opt == 'data_status':
            if time_data == time_current or time_data == time_current - 1:
                state='new'
            else:
                state='old'
                logging.error("mysql data is old!")
            print state
        else:
            print 0.0
    except Exception as e:
        logging.info(e)
### judje mysql server data is new
if __name__ == '__main__':
    main()
