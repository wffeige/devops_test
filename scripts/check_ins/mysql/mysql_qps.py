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


def get_status():
    sql = "show global status where Variable_name in ('Com_select','Com_insert','Com_delete','Com_update','Uptime','Com_rollback','Com_commit')"
    conn=MySQLdb.connect('127.0.0.1','root','rootroot')
    cursor=conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    lines=cursor.fetchall()
    keylist=[]
    valuelist=[]
    dict_now={}
    for i in lines:
        valuelist.append(i['Value'])
        keylist.append(i['Variable_name'])

    dict_now=dict(zip(keylist,valuelist))
    #print dict_now
    return dict_now




@deco_head(logfile)
def main(opt,discovery  ,logging):
    try:
        cache = TmpFile(cache_file)
        dict_past = cache.get_content()
        dict_now=get_status()
        cache.recode_info(str(dict_now.items()))
    except Exception as e :
        logging.warning(e)


    try:    
        time_interval = int(dict_now['Uptime'])-int(dict_past['Uptime'])
        if time_interval == 0:
            time_interval=1
            logging.info("time_interval is 0")
        select_diff=(int(dict_now['Com_select'])-int(dict_past['Com_select']))/time_interval
        insert_diff=(int(dict_now['Com_insert'])-int(dict_past['Com_insert']))/time_interval
        update_diff=(int(dict_now['Com_update'])-int(dict_past['Com_update']))/time_interval
        delete_diff=(int(dict_now['Com_delete'])-int(dict_past['Com_delete']))/time_interval
        commit_diff=(int(dict_now['Com_commit'])-int(dict_past['Com_commit']))/time_interval
        rollback_diff=(int(dict_now['Com_rollback'])-int(dict_past['Com_rollback']))/time_interval
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
