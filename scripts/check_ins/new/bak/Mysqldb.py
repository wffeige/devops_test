#!/usr/bin/env python
import os
import MySQLdb

class MySQL(object):
    def __init__(self, config):
        self.config = config
        try:
            self.cnn = MySQLdb.connect(**self.config)
            self.cursor = self.cnn.cursor()
        except Exception, e:
            raise Exception("MySQL connect error, check my_config.")
    
    def result_lst(self, sql):
        try:
            self.cursor.execute(sql)
            rs = self.cursor.fetchall()
        except Exception, e:
            print e
            return 0
        return rs

    def commit(self, sql) :
        try:
            self.cursor.execute(sql)
            self.cnn.commit()
        except Exception, e:
            return 0
        return 1

    def __del__(self):
        try:
            self.cursor.close()
            self.cnn.close()
        except:
            pass
