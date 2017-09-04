#!/usr/bin/env python
#-*- coding:utf-8 -*-

# FileName    :restore_beta_from_online.py
# Author      :wang fei
# Date        :2016-12-28
# Description :每周一从线上备份恢复beta库数据，并且建立一个备份，用于之后的还原。
# Excute      :restore_beta_from_online.py

import os, sys
from Mysqldb import MySQL
from MT import *

base_dir = os.path.split(os.path.realpath(__file__))[0]
script = os.path.basename(__file__)
today = get_today()
logpath = r'%s/logs/%s' % (base_dir, script)
logfile = r'%s/%s.log' % (logpath, today)
logging = logger(logfile)
beta_master_config = get_rds_info_dict('local')
#beta_slave_config = get_rds_info_dict('beta_slave')

nfs_path = r'/nfs_data/mysql_backup/rds_3306/dump/%s' % today
check_beta_master_server_id = 22222

def check():
    ###check nfs back path
    pass
    mysql = MySQL(beta_master_config)
    mysql_slave = MySQL(beta_master_config)
    print mysql.result_lst('show slave status')



    pass
    mysql = MySQL(beta_master_config)
    mysql_slave = MySQL(beta_slave_config)
    print mysql.result_lst('show master status')

    s_id = mysql.result_lst('show global variables  like "server_id";')
    s_id = dict(s_id)
    s_id = re.findall("\d+",str(s_id.values()))
    s_id = int(s_id[0])
    print s_id

    port = mysql.result_lst('show global variables  like "port";')
    port = dict(port)
    port = re.findall("\d+",str(port.values()))
    port = int(port[0])
    print port


    if os.path.exists(nfs_path):
        #logging.info("%s is exist."%nfs_path)
        pass
    else:
        logging.info("%s is not exist!"%nfs_path)
    if s_id == check_beta_master_server_id and port == 3306:
        #logging.info("beta env!")
        pass
    else:
        logging.info("not beta env")


    ###slave
    p = mysql_slave.result_dict('show slave status;')
    print p
    s_id = mysql_slave.result_lst('show global variables  like "server_id";')
    s_id = dict(s_id)
    s_id = re.findall("\d+",str(s_id.values()))
    s_id = int(s_id[0])

    

def main():
    ###logging
    if os.path.isdir(logpath):
        pass
    else:
        os.mkdir(logpath)
    ###check
    check()

if __name__ == "__main__":
    main()
