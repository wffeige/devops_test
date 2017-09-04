#coding:utf-8

#!/usr/bin/env python
'''
mysql connection
    
'''
import os
import MySQLdb
class MySQL(object):
    def __init__(self, config):
        self.config = config

        user = self.config['user']
        passwd = self.config['password']
        host = self.config['host']
        # unix_socket = self.config['unix_socket']


        try:
            # self.db = MySQLdb.connect(user=user,passwd=passwd,host=host,unix_socket=unix_socket)
            self.db = MySQLdb.connect(user=user,passwd=passwd,host=host)

            # self.db = MySQLdb.connect(**self.config)
            self.cursor = self.db.cursor()


        except Exception, e:
            raise Exception("MySQL connect error, check my_config.")



    def result_list(self,sql):

        try:
            cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql)
            data = cursor.fetchall()
            li = []
            for i in data:
                li.append(i)
        except  Exception as e:
            print e
            return 0
        return  li





    def result_str(self,sql):

        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
        except Exception, e:
            print e
            return 0
        return  data






    def commit(self,sql):

        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception, e:
            print e
            return 0
        return 1




    def __del__(self):
        try:
            self.cursor.close()
            self.db.close()
        except:
            pass


