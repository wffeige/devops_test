#coding:utf-8


import os
import sys
from datetime import datetime,timedelta
from public import TmpFile,send_mail
import requests
from requests.auth import HTTPBasicAuth

import sys
reload(sys)
sys.setdefaultencoding('utf8')


base_dir = os.path.split(os.path.realpath(__file__))[0]

cache_file = r'%s/var/request_data.tmp' % (base_dir)
cache = TmpFile(cache_file)

# 存数据
# cache.recode_info(str(data))

# 读数据
# data = cache.get_content()






def request_api():
    '''
    获取实例信息
    '''

    # url = "http://opsweb.vipkid.com.cn/api/v1/assets/?limit=3000"
    url = "http://192.168.2.251/api/v1/assets/?limit=3000"

    user = "wangfei1"
    password = "Wffeige050619!"
    req = requests.get(url,auth=HTTPBasicAuth(user, password))
    res = req.json()
    return res




def check_expired():
    '''
    检查实例的过期时间
    :return:
    '''

    lst=[]

    # 报警阈值
    days=30


    asset_data = request_api()
    for i in asset_data['results']:
        if i['expire_time'] !=None:
            expire_time = i['expire_time'].replace('T', ' ').rstrip('Z')


            if 'aliyun' in i['platform'] :
                expire_time = datetime.strptime(expire_time.split(".")[0], "%Y-%m-%d %H:%M")
            else:
                expire_time = datetime.strptime(expire_time.split(".")[0], "%Y-%m-%d %H:%M:%S")


            time_now = datetime.now()

            #实例剩余时间
            remain_time = expire_time - time_now


            if remain_time.days <= days :
                lst.append({'instance_id':i['instance_id'],'remain_time':remain_time.days,'expire_time':str(expire_time)})
            else:
                pass



    return lst




import time

def check_stop():
    '''
    检查停机情况
    :return:
    '''


    #任务计划刷新接口的时间
    crontab_time=15


    '''

    :检查实例的运行状态:
    '''

    res={}

    asset_data = request_api()
    cache.recode_info(str(asset_data))


    lst_1=[]
    lst_2=[]

    time_now = datetime.now()
    for i in asset_data['results']:

        update_time = i['update_time'].replace('T',' ')
        update_time = datetime.strptime(update_time.split(".")[0], "%Y-%m-%d %H:%M:%S")

        interval_time =  time_now - update_time

        if interval_time >= timedelta(minutes=crontab_time) and interval_time <= timedelta(minutes=crontab_time*2):#刚刚停止的机器
            lst_1.append(i)
        elif interval_time >= timedelta(minutes=crontab_time*2):
            # print "already stop!",i
            lst_2.append(i)


    res['just_stop'] = lst_1    #刚刚停机
    res['already_stop'] = lst_2     #已经停机

    return res



def html_stop(con):
    '''
    停机情况模板
    :param con:
    :return:
    '''
    html_con=''

    for i in con['just_stop']:
        html_con += '实例id:{},  上一次更新时间:{},刚刚停止运行!!! '.format(i['instance_id'],i['update_time'])+'\n'
    return html_con




def html_expire(con):
    '''
    实例过期模板
    :param con:
    :return:
    '''

    html_con=''

    for i in con:
        html_con += '实例id:{},  过期时间:{} ,剩余天数:{}天。'.format(i['instance_id'],i['expire_time'],i['remain_time'])+'\n'
    return html_con




def main():


    content1 = html_stop(check_stop())
    print content1

    # content_send = html_expire(check_expired())


    sub='实例剩余时间'
    mailto=["wffeige@126.com"]

    send_mail(mailto,content1,sub)

if __name__ == '__main__':
    main()
