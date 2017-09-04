#!/usr/bin/env python
#-*- coding:utf-8 -*-

# FileName    :restore_beta_from_online.py
# Author      :wang fei
# Date        :2016-12-28
# Description :每周一从线上备份恢复beta库数据，并且建立一个备份，用于之后的还原。
# Excute      :restore_beta_from_online.py

import os, sys
from MT import *

base_dir = os.path.split(os.path.realpath(__file__))[0]
script = os.path.basename(__file__)
today = get_today()
logpath = r'%s/logs/%s' % (base_dir, script)
logfile = r'%s/%s.log' % (logpath, today)
my_config = get_rds_info_dict('beta')

def main():
    ###logging
    if os.path.isdir(logpath):
        pass
    else:
        os.mkdir(logpath)
    logging = logger(logfile)
    logging.info('123')

if __name__ == "__main__":
    main()
