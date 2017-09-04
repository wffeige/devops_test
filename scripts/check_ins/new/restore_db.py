#!/usr/bin/env python
#-*- coding:utf-8 -*-

# FileName    :restore_beta_from_online.py
# Author      :wang fei
# Date        :2016-12-28
# Description :每周一从线上备份恢复beta库数据，并且建立一个备份，用于之后的还原。
# Excute      :restore_beta_from_online.py

import os, sys,re
from MyLink import MySQL
from MT import *

base_dir = os.path.split(os.path.realpath(__file__))[0]
script = os.path.basename(__file__)
today = get_today()
logpath = r'%s/logs/%s' % (base_dir, script)
logfile = r'%s/%s.log' % (logpath, today)
logging = logger(logfile)
beta_master_config = get_rds_info_dict('beta')
beta_slave_config = get_rds_info_dict('beta_slave')

nfs_path = r'/nfs_data/mysql_backup/rds_3306/dump/%s' % today
check_beta_master_server_id = 22222

def check():
    ###check nfs back path
    pass
    mysql = MySQL(beta_master_config)
    mysql_slave = MySQL(beta_slave_config)

    slave = mysql_slave.result_dict('show slave status;')
    s_id = mysql.result_dict('show global variables  like "server_id";')
    port = mysql.result_dict('show global variables  like "port";')
    s_id = s_id['Value']    
    port = port['Value']
    
    print s_id
    print port
    print slave['Slave_IO_Running']
    print slave['Slave_SQL_Running']
    

    if os.path.exists(nfs_path):
        #logging.info("%s is exist."%nfs_path)
        pass
    else:
        logging.info("%s is not exist!"%nfs_path) 
        return 0
        
    if int(s_id) == check_beta_master_server_id and int(port) == 3306: 
        pass
        #logging.info("beta env!")
    else:
        logging.info("not beta env")
        return 0

    if slave['Slave_IO_Running'] == 'No' and slave['Slave_SQL_Running'] == 'No':
        pass
    else:
        logging.info("no slave")
        return 0




    #print data
    #print define

def ge_scr():
    
    data = []
    define = []
    li=os.listdir(nfs_path)
    for i in li:
        if i.find("table_data.vipkid") == 0:
            data.append(i)
        elif i.find("table_define.vipkid") == 0:
            define.append(i)
    print data    


    
    
def main():
    ###logging
    if os.path.isdir(logpath):
        pass
    else:
        os.mkdir(logpath)
    ###check
    #check()
    #ge_scr
    ge_scr()


if __name__ == "__main__":
    main()
