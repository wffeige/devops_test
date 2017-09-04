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
logging = logger(logfile)

def resultOne(sql):
    try:
        conn=MySQLdb.connect('127.0.0.1','wangfei','rootroot')
        cursor=conn.cursor()
        cursor.execute(sql)
        rs = cursor.fetchone()
        return rs
    except Exception as err:
        logging.waring(err)


def get_status():
    resSelect = resultOne("show global status like 'Com_select'")
    resInsert = resultOne("show global status like 'Com_insert'")
    resDelete = resultOne("show global status like 'Com_delete'")
    resUpdate = resultOne("show global status like 'Com_update'")
    resTime = resultOne("show global status like 'Uptime'")
    resRolback = resultOne("show global status like 'Com_rollback'")
    resCommit = resultOne("show global status like 'Com_commit'")
    key=[]
    value=[]
    dict_qps={}
    for i in (resSelect,resInsert,resDelete,resUpdate,resTime, resRolback,resCommit):
        key.append(i[0])
        value.append(i[1])
    dict_qps=dict(zip(key,value))
    return dict_qps

@deco_head(logfile)
def main(opt,discovery  ,logging):
    try:
        cache = TmpFile(cache_file)
        dict_qps_past = cache.get_content()
        dict_qps_now=get_status()
        cache.recode_info(str(dict_qps_now.items()))
    except Exception as e :
        logging.warning(e)


    try:    
        time_interval = int(dict_qps_now['Uptime'])-int(dict_qps_past['Uptime'])
        if time_interval == 0:
            time_interval=1
            logging.info("time_interval is 0")
        select_diff=(int(dict_qps_now['Com_select'])-int(dict_qps_past['Com_select']))/time_interval
        insert_diff=(int(dict_qps_now['Com_insert'])-int(dict_qps_past['Com_insert']))/time_interval
        update_diff=(int(dict_qps_now['Com_update'])-int(dict_qps_past['Com_update']))/time_interval
        delete_diff=(int(dict_qps_now['Com_delete'])-int(dict_qps_past['Com_delete']))/time_interval
        commit_diff=(int(dict_qps_now['Com_commit'])-int(dict_qps_past['Com_commit']))/time_interval
        rollback_diff=(int(dict_qps_now['Com_rollback'])-int(dict_qps_past['Com_rollback']))/time_interval
    except KeyError as e :
        logging.warning(e)
    
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
    elif opt == 'commit':
        print commit_diff
    elif opt == 'rollback':
        print rollback_diff
    else :
        print -1

if __name__ == '__main__':
    main()
