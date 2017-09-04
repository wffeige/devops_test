#!/usr/bin/env python
'''
backup  processlist,  innodb status, global status (per minute)
'''

import time, sys, os, MySQLdb, subprocess
from common_zabbix import deco_head, logger, shell, TmpFile

base_dir = os.path.split(os.path.realpath(__file__))[0]
logfile = r'%s/logs/%s.log' % (base_dir, os.path.basename(__file__).split('.')[0])
cache_file = r'%s/var/%s.tmp' % (base_dir, os.path.basename(__file__).split('.')[0])
logging = logger(logfile)



## backup "show processlist;", "show engine status;"  "show global status;"

path_innodb='%s/logs/innodb_status/'%base_dir
path_global='%s/logs/global_status/'%base_dir
path_proc='%s/logs/processlist/'%base_dir

timestamp=time.strftime("%Y-%m-%d_%H:%M")
day=time.strftime("%Y-%m-%d")
name_proc='processlist_'+timestamp
name_innodb='innodb_status_'+timestamp
name_global='global_status_'+timestamp


def backup():
  
### check backfile path  
    if not os.path.isdir(path_proc):
        os.makedirs(path_proc)
    
    if not os.path.isdir(path_innodb):
        os.makedirs(path_innodb)

    if not os.path.isdir(path_global):
        os.makedirs(path_global)


    try:
### backup  processlist 
        file1=open('%s.txt'%(path_proc+name_proc),'w')
        pro_result=os.popen('/opt/mysql_3306/bin/mysql -uroot -prootroot   --socket=/data/mysql_3306/mysql.sock -e "show processlist;"').readlines()
        for i in pro_result:
            file1.write(i)
        file1.close()

### backup innodb_status
        file2=open('%s.txt'%(path_innodb+name_innodb),'w')
        innodb_result=os.popen('/opt/mysql_3306/bin/mysql -uroot -prootroot  --socket=/data/mysql_3306/mysql.sock -e "show engine innodb status\G"').readlines()
        for k in innodb_result:
            file2.write(k)
        file2.close()

### backup global_status
        file3=open('%s.txt'%(path_global+name_global),'w')
        gstatus_result=os.popen('/opt/mysql_3306/bin/mysql -uroot -prootroot        --socket=/data/mysql_3306/mysql.sock -e "show global status;"').readlines()
        for m in gstatus_result:
            file3.write(m)
        file3.close()
    except Exception as e:
        logging.error("create backfile error! %s"%e)
    print 1

### make dir perday && backup file to dir
def day_dir():
    while True:
        if os.path.exists('%s'%path_proc+day):
            os.popen('find %s   -maxdepth 1  -type f -name "*%s*" -exec mv {} %s \;'%(path_proc,day,path_proc+day))
            break
        else:
            os.popen('mkdir %s'%path_proc+day)

    while True:
        if os.path.exists('%s'%path_innodb+day):
            os.popen('find %s -maxdepth 1  -type f -name "*%s*" -exec mv {} %s \;'%(path_innodb,day,path_innodb+day))
            break 
        else:
            os.popen('mkdir %s'%path_innodb+day)

    while True:
        if os.path.exists('%s'%path_global+day):
            os.popen('find %s -maxdepth 1  -type f -name "*%s*" -exec mv {} %s \;'%(path_global,day,path_global+day))
            break
        else:
            os.popen('mkdir %s'%path_global+day)


if __name__ == '__main__':
    
    backup()
    day_dir()
