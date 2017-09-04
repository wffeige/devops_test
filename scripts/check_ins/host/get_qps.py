#!/usr/bin/env python
"""
python get_qps.py --opt=sel
python get_qps.py --opt=del
python get_qps.py --opt=ins
python get_qps.py --opt=upd
"""

import MySQLdb,os
from common_zabbix import deco_head, logger, shell, TmpFile
base_dir = os.path.split(os.path.realpath(__file__))[0]
logfile = r'%s/logs/%s.log' % (base_dir, os.path.basename(__file__).split('.')[0])
cache_file = r'%s/var/%s.tmp' % (base_dir, os.path.basename(__file__).split('.')[0])


def resultOne(sql):
    try:
        conn=MySQLdb.connect('127.0.0.1','wangfei','rootroot')
        cursor=conn.cursor()
        cursor.execute(sql)
        rs = cursor.fetchone()
        return rs
    except Exception as err:
        print err


def get_status():
    resSelect = resultOne("show global status like 'Com_select'")
    resInsert = resultOne("show global status like 'Com_insert'")
    resDelete = resultOne("show global status like 'Com_delete'")
    resUpdate = resultOne("show global status like 'Com_update'")
    resCommit = resultOne("show global status like 'Com_commit'")
    resRollback = resultOne("show global status like 'Com_rollback'")
    resQuestions = resultOne("show global status like 'Questions'")

    resTime = resultOne("show global status like 'Uptime'")
    conn.close()
    key=[]
    value=[]
    dict_qps={}
    for i in (resSelect,resInsert,resDelete,resUpdate,resTime,resCommit,resRollback,resQuestions):
        key.append(i[0])
        value.append(i[1])
    dict_qps=dict(zip(key,value))
    print dict_qps
    return dict_qps

@deco_head(logfile)
def main(opt,discovery  ,logging):
    cache = TmpFile(cache_file)
    dict_qps_past = cache.get_content()
    dict_qps_now=get_status()
    cache.recode_info(str(dict_qps_now.items()))
    

    time_interval = int(dict_qps_now['Uptime'])-int(dict_qps_past['Uptime'])
    if time_interval == 0:
        time_interval=1
    select_diff=(int(dict_qps_now['Com_select'])-int(dict_qps_past['Com_select']))/time_interval
    insert_diff=(int(dict_qps_now['Com_insert'])-int(dict_qps_past['Com_insert']))/time_interval
    update_diff=(int(dict_qps_now['Com_update'])-int(dict_qps_past['Com_update']))/time_interval
    delete_diff=(int(dict_qps_now['Com_delete'])-int(dict_qps_past['Com_delete']))/time_interval
    
    if opt == 'sel':
        print select_diff
    elif opt == 'del':
        print delete_diff
    elif opt == 'ins':
        print insert_diff
    elif opt == 'upd':
        print update_diff
    elif opt == 'time':
        print time_interval
    else :
        print -1

if __name__ == '__main__':
    main()
