#!/usr/bin/env python
'''
get MySQL hit_rate  --opt=hit 
mysql status --opt=mysql status
slave status --opt=slave status
deadlocks  --opt=deadlock
dbsize  --opt=dbsize

'''

import time, sys, os, MySQLdb, subprocess
from common_zabbix import deco_head, logger, shell, TmpFile

base_dir = os.path.split(os.path.realpath(__file__))[0]
logfile = r'%s/logs/%s.log' % (base_dir, os.path.basename(__file__).split('.')[0])
cache_file = r'%s/var/%s.tmp' % (base_dir, os.path.basename(__file__).split('.')[0])
logging = logger(logfile)


try :
    conn=MySQLdb.connect('127.0.0.1','wangfei','rootroot')
    cursor=conn.cursor()
except Exception as e :
    logging.error('mysql connect error\n.%s'%e)

def resultAll(sql):
    conn=MySQLdb.connect('127.0.0.1','wangfei','rootroot')
    cursor=conn.cursor()
    cursor.execute(sql)
    rs = cursor.fetchall()
    return rs

def result_dict(sql):
    conn=MySQLdb.connect('127.0.0.1','wangfei','rootroot')
    cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    rs = cursor.fetchone()
    return rs
    
def getdata():
    dict_info={}
    sql1 = "show global status where Variable_name in ('Innodb_buffer_pool_reads','Innodb_buffer_pool_read_requests');"
    result1 = resultAll(sql1)
    result1 = dict(result1)
    read = (float (result1['Innodb_buffer_pool_reads']))
    request = (float (result1['Innodb_buffer_pool_read_requests']))  
    hit = (1- read/request)
    dict_info['hit']=hit

    sql2 = "select sum(data_length/1024/1024+index_length/1024/1024) as data from information_schema.tables;"
    result2 = result_dict(sql2)
    a='%f'%result2['data']
    dict_info['dbsize']=float(a)


    sql3 = 'show databases;'
    result3 = resultAll(sql3)
    if result3:
        mysql_status=1
    else:
        mysql_status=0
    dict_info['mysql_status']=mysql_status
    sql4 = 'show slave status;'
    result4 = result_dict(sql4)
    print result4
			
    #sql5 = "show global status where Variable_name in('Innodb_deadlocks','Innodb_x_lock_os_waits','Innodb_s_lock_os_waits','Table_locks_waited')"
    #result5 = resultAll(sql5)
    #for i in result5:
    #    dict_info[i[0]]=int(i[1])
    #return dict_info

@deco_head(logfile)
def main(opt,discovery  ,logging):
    dict_info=getdata()
    print dict_info
    if opt == 'deadlock':
        print dict_info['Innodb_deadlocks']
    elif opt == 'mysql_status':
        print dict_info['mysql_status']
    elif opt == 'dbsize':
        print dict_info['dbsize']
    else:
        pass
    
main()
