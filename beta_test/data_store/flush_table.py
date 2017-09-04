#!/usr/bin/env python
#-*- coding:utf-8 -*-

# TODO(wffeig@126.com)

from public import get_info_dict
from public import shell
from public import logger
from public import mkdirs

import datetime
import sys
import os
from MySQL_cnn import MySQL


now_time = datetime.datetime.now()
dir_time = now_time.strftime("%Y-%m-%d")

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
        self.socket = self.host_config['socket']
        self.port = self.host_config['port']

        self.mysql = MySQL(self.host_config)


    def restore(self):

        sql = """insert into openstack_log.t5(hostname,module,service,log_level,operation,log_message) values ('172.16.1.136','nova','nova-api','info','create vm','{"name":"123"}'); """

        try:
            res1 =  self.mysql.commit(sql)
            if res1 == 1 :
                print "commit  ok!"
        except Exception as e:
            print e
            print "db init error!"



def main():

    res = {'conf_name':'localhost','database':'openstack_log'}

    db = BackupDB(**res)
    db.restore()

if __name__ == '__main__':
    main()



