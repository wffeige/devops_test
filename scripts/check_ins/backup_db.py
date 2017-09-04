#!/usr/bin/env python
#-*- coding:utf-8 -*-

# TODO(wffeig@126.com)

# TODO(Zeke) 目前先用mysqldump 进行备份  后期备份大的话 考虑mysqldumper进行多线程备份



from public import get_info_dict
from public import shell
from public import logger
from public import mkdirs
from public import getFileSize,getPathSize,getdirsize

import datetime
import sys
import os
from MySQL_cnn import MySQL


now_time = datetime.datetime.now()
dir_time = now_time.strftime("%Y-%m-%d")
#dir_time ='2017-05-10'






base_dir = os.path.split(os.path.realpath(__file__))[0]
script = os.path.basename(__file__)
logpath = r'%s/logs/%s' % (base_dir, script)
logfile = r'%s/%s.log' % (logpath, dir_time)
mkdirs(logpath)
logging = logger(logfile)




class BackupDB(object):

    def __init__(self,**kwargs):

        self.conf_name = kwargs['conf_name']      #选择的section
        self.database = kwargs['database']        #选择备份的数据库


        self.host_config = get_info_dict(self.conf_name)
        self.host = self.host_config['host']
        self.user = self.host_config['user']
        self.password = self.host_config['password']
        self.socket = self.host_config['unix_socket']
        self.port = self.host_config['port']



        self.mysql = MySQL(self.host_config)




    '''
    备份文件：备份方式/时间/host
    每次恢复的时候先删除database
    此命令可以用来验证备份的有效性
    '''
    def restore(self):

        sql_drop = "drop database if EXISTS {}".format(self.database)
        sql_create = "create database {}".format(self.database)
        print sql_create



        try:
            res1 =  self.mysql.commit(sql_drop)
            res2 =  self.mysql.commit(sql_create)
            if res1 == 1 and res2 == 1:
                print "db init ok!"
        except Exception as e:
            print e
            print "db init error!"



        back_dir_mysqldump = '/data/db_data_bak/mysqldump/{}/{}'.format(dir_time,self.conf_name)
        back_file='{path}/{database}.sql'.format(path=back_dir_mysqldump,database=self.database)
        cmd="/opt/mysql_3306/bin/mysql  --socket={socket}  --port={port} -h{host}  -u{user} -p{password}  {database} < {back_file}".format(database=self.database,user=self.user, password=self.password, port=self.port, host=self.host,socket=self.socket,back_file=back_file)
        result_cmd = shell(cmd,'s')

        print "cmd status {}".format(result_cmd)
        if result_cmd == 0:
            logging.debug("back {back_file} ok! time is {time}".format(time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),back_file=back_file))



    def dump(self):
        self.mysql = MySQL(get_info_dict('localhost'))

        back_dir_mysqldump = '/data/db_data_bak/mysqldump/{}/{}'.format(dir_time,self.conf_name)

        file_name = "{}/{}.sql".format(back_dir_mysqldump,self.database)
        mkdirs(back_dir_mysqldump)


        try:
            cmd = " /opt/mysql_3306/bin/mysqldump   --set-gtid-purged=off --skip-add-drop-tabl -u{user} -p{password} -h{host} --socket={socket}  --databases {database} >{file_name} ".format(back_dir=back_dir_mysqldump,file_name=file_name,user=self.user,password=self.password,host=self.host,socket=self.socket,database=self.database)
            start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            result_cmd = shell(cmd,'s')
            stop_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

            if result_cmd == 0:

                bak_filesize = getFileSize(file_name)
                record_sql = "insert into opsweb.back_info values(null, '{host}','{db}','{bak_type}','{bak_path}','{start_time}','{stop_time}','{bak_filesize}',null,null )".format(host=self.host,db=self.database,bak_type='dump',bak_path=back_dir_mysqldump,bak_filesize=bak_filesize,start_time=start_time,stop_time=stop_time)
                self.mysql.commit(record_sql)


        except Exception as e:
            print e



    """
    备份binlog的时候 必须指定开始的binlog
    """

    def binlog(self,opt):
        back_dir_binlog = '/data/db_data_bak/binlog/{}/{}/'.format(dir_time,self.conf_name)

        binglog_name=opt

        mkdirs(back_dir_binlog)


        try:
            cmd = "/opt/mysql_3306/bin/mysqlbinlog --read-from-remote-server --raw --host={host} --port={port}     --user={user}  --password={password} --socket={socket}  --to-last-log  {binglog_name} --result-file={back_dir_binlog} ".format(back_dir_binlog=back_dir_binlog, user=self.user, password=self.password, port=self.port, host=self.host,socket=self.socket, binglog_name=binglog_name)
            print cmd
            result = shell(cmd,'s')
        except Exception as e:
            result =1
            print e

        if result == 0:
            # 备份成功，进行record
            pass
        else:
            # 备份失败
            pass



    def xtrabackup(self):
        back_dir_xtrabackup = '/data/db_data_bak/xtrabackup/{}'.format(dir_time)

        mkdirs(back_dir_xtrabackup)
        pass


def main():


    res = {'conf_name':'ali1','database':'all'}
    opt = 'mysql_3306.000018' #备份binlog需要指定开始的binlog

    db = BackupDB(**res)
    #db.binlog(opt)
    #db.restore()

    db.dump()
if __name__ == '__main__':
    main()

