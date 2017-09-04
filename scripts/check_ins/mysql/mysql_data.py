#!/usr/bin/env python
'''
get MySQL hit_rate, server status, slave status, deadlock status, dbsize (per minute)
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


def getdata():
### get hit_rate
    dict_info={}
    try: 
        sql2="show global status where Variable_name in ('Innodb_buffer_pool_reads','Innodb_buffer_pool_read_requests');"       
        cursor.execute(sql2)
        result3 = cursor.fetchall()
        mystat3 = dict(result3)
        read = (float (mystat3['Innodb_buffer_pool_reads']))
        request = (float (mystat3['Innodb_buffer_pool_read_requests']))  
        hit = (1- read/request)
        #print "%.2f%%"% (hit*100)   

    except Exception as e:
        logging.error("sql2 excute error! \n%s"%e)

    dict_info['hit']=hit

### get db_size
    try:
        sql3="select sum(data_length/1024/1024+index_length/1024/1024) as data from information_schema.tables;"
        cursor.execute(sql3)
        i=cursor.fetchall()
        i=str(i)
        i=i.replace("(","")
        i=i.replace(")","")
        i=i.replace(",","")
        i=i.replace("'","")
        i=i.replace("Decimal","")
        dbsize=i
    except  Exception as e:
        logging.error("sql3 execute error! \n%s"%e)
    dict_info['dbsize']=dbsize

### get mysql alive status
    try:    
        sql4 = 'show databases;'
        if cursor.execute(sql4):
            alive_status=1
    except Exception as e:
            alive_status=0
            logging.error('sql4 error!\n%s'%e)
    dict_info['mqstatus'] =alive_status   


### get slave status        
    try:
        cur1 = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        sql5 = 'show slave status;'
        cur1.execute(sql5)
        result5 = cur1.fetchall()
        result5 = str(result5)
        if "'Slave_IO_Running': 'Yes'" in result5:
            slave_status = 1
        else:
            slave_status = 0
            logging.error("\n slave status error! \n")    
    except Exception as e:
        logging.error('sql5 error!\n%s'%e)
    dict_info['slave_status']=alive_status

    #sql7='show global status like "%Slave_running%"'
        




### get  deadlock 
    try:
        sql6="select t.trx_id  waiting_trx_id,   t.trx_mysql_thread_id   waiting_thread_id,t.trx_query   waiting_query,l.*,p.*  from information_schema.PROCESSLIST  p,information_schema.INNODB_LOCK_WAITS l ,information_schema.INNODB_TRX t    where t.trx_id = l.requesting_trx_id   and  p.ID= t.trx_mysql_thread_id;"
        if  cursor.execute(sql6):
            dead_lock_status=1
            cmdout=''
            cmd='/opt/mariadb10/bin/mysql --socket=/data/mysql_3306/mysql.sock -e"select t.trx_id waiting_trx_id,   t.trx_mysql_thread_id   waiting_thread_id,t.trx_query waiting_query,l.*,p.*  from information_schema.PROCESSLIST  p,information_schema.INNODB_LOCK_WAITS l ,information_schema.INNODB_TRX t    where t.trx_id = l.requesting_trx_id   and  p.ID= t.trx_mysql_thread_id\G"'
            subp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            cmdout = subp.communicate()[0][:-1]
            file_d=open('%s/logs/deadlock_info.txt'%base_dir,'w')
            file_d.write(cmdout)
            file_d.cloes()
        
            logging.error("generate deadlock! time is %s"%(time.strftime("%Y-%m-%d_%H:%M")))
        else:
            dead_lock_status=0
    
    except Exception as e:
        logging.error(e)

    dict_info['dead_lock_status'] = dead_lock_status

### get timestamp(hour and minute)
    time_data=time.strftime("%H%M")
    dict_info['time_id']=time_data
    print dict_info
    cache = TmpFile(cache_file)

    dict_past=cache.get_content()
    print "past time is %s "%dict_past['time_id']

    if dict_past['time_id'] == dict_info['time_id']:
        logging.warning("Time interval less than a minute ")

    cache.recode_info(str(dict_info.items()))
    
if __name__ == '__main__':
    getdata()
