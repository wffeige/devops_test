#!/usr/bin/env python
#-*- coding:utf-8 -*-

# FileName    :restore_beta_from_online.py
# Author      :wang fei
# Date        :2016-12-28
# Description :每周一从线上备份恢复beta库数据，并且建立一个备份，用于之后的还原。
# Excute      :restore_beta_from_online.py

import os, sys,re
# from MyLink import MySQL
from public import *
from MySQL_cnn import MySQL

host_config = get_info_dict('ali1')



def check():
    # print host_config

    mysql = MySQL(host_config)


    sql='drop database wangfei_hehe'
    res = mysql.commit(sql)
    print res
    
def main():
    check()



if __name__ == "__main__":
    main()
