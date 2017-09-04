#!/usr/bin/env python
'''
get MySQL TPS, QPS, hit_rate, server status, slave status, deadlock status, dbsize (per minute)

backup  processlist,  innodb status, global status (per minute)
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

### get QPS TPS
    try:    
        diff = 2
        mystat1={}
        mystat2={}
        mystat3={}
        sql1 = "show global status where Variable_name in ('Com_commit','Com_delete','Com_insert','Com_rollback','Com_select','Com_update','Questions');"
        cursor.execute(sql1)
        results1 = cursor.fetchall()    
        mystat1 = dict(results1)

        time.sleep(diff)

        cursor.execute(sql1)
        results2 = cursor.fetchall()
        mystat2 = dict(results2)

        Com_diff = (int(mystat2['Com_commit'])   - int(mystat1['Com_commit']) ) / diff
        rol_diff = (int(mystat2['Com_rollback']) - int(mystat1['Com_rollback']))/ diff
        del_diff = (int(mystat2['Com_delete'])   - int(mystat1['Com_delete']) ) / diff
        ins_diff = (int(mystat2['Com_insert'])   - int(mystat1['Com_insert']) ) / diff
        sel_diff = (int(mystat2['Com_select'])   - int(mystat1['Com_select']) ) / diff
        upd_diff = (int(mystat2['Com_update'])   - int(mystat1['Com_update']) ) / diff
        que_diff = (int(mystat2['Questions'])    - int(mystat1['Questions']) )  / diff
        QPS = del_diff + ins_diff + upd_diff + sel_diff
        TPS = Com_diff + rol_diff

    except Exception as e:
        logging.error("sql1 excute error! \n%s"%e)
        sys.exit(1)


### get hit_rate
   
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


### get mysql alive status
    try:    
        sql4 = 'show databases;'
        if cursor.execute(sql4):
            alive_status=1
    except Exception as e:
            alive_status=0
            logging.error('sql4 error!\n%s'%e)



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



### get timestamp(hour and minute)
    time_data=time.strftime("%H%M")

#    print "QPS is:          \t%s"%QPS 
#    print "TPS is:          \t%s"%TPS
#    print "hit_rate is:     \t%.2f%%"% (hit*100)   
#    print "all db size is:  \t%s"%dbsize
#    print "mysql status is: \t%s"%alive_status
#    print "slave status is: \t%s"%slave_status
#    print "deadlock status is:\t%s"%dead_lock_status


    try:
        if os.path.exists('%s/var'%base_dir):
            file1=open('%s/var/mysql_status_new.txt'%base_dir,'w')
            file1.write('%s\n'%QPS)     
            file1.write('%s\n'%TPS)     
            #file1.write('%.2f%%\n'%(hit*100))     
            file1.write('%s\n'%hit)     
            file1.write('%s\n'%dbsize)     
            file1.write('%s\n'%alive_status)     
            file1.write('%s\n'%slave_status)     
            file1.write('%s\n'%dead_lock_status)
            file1.write('%s\n'%time_data)
            file1.close()   
        else:
            os.popen('mkdir %s/var'%base_dir)
    except Exception as e:
        logging.error("update %s/var/mysql_status_new.txt error! \n%s"%(base_dir,e))
        sys.exit(1)

    print 1

if __name__ == '__main__':
    getdata()
