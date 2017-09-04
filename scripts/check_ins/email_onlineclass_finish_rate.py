#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
每天发送课程完课率和故障率邮件
'''
from __future__ import division
import os, sys
from MyLink import MySQL
from MT import *

my_config = get_rds_info_dict('rep')
#to_list = ['zhanggong@vipkid.com.cn', 'changlili@vipkid.com.cn']
to_list = ['changlili@vipkid.com.cn', 'panglv@vipkid.com.cn', 'zhangyanjing@vipkid.com.cn', 'zhangchao@vipkid.com.cn', 'tom.xie@duobei.com']

def get_finish_rate(result):
    db1_cnt, db2_cnt, total_cnt = 0, 0, 0
    db1_as_cnt, db2_as_cnt, total_as_cnt = 0, 0, 0
    for line in result:
        cnt, ft, supplier = line
        if int(supplier) == 2:
            if ft == 'AS_SCHEDULED':
                db1_as_cnt += int(cnt)
            if ft in ('AS_SCHEDULED', 'STUDENT_IT_PROBLEM', 'TEACHER_IT_PROBLEM', 'SYSTEM_PROBLEM'):
                db1_cnt += int(cnt)
        if int(supplier) == 4:
            if ft == 'AS_SCHEDULED':
                db2_as_cnt += int(cnt)
            if ft in ('AS_SCHEDULED', 'STUDENT_IT_PROBLEM', 'TEACHER_IT_PROBLEM', 'SYSTEM_PROBLEM'):
                db2_cnt += int(cnt)
        if int(supplier) in (2, 4):
            if ft == 'AS_SCHEDULED':
                total_as_cnt += int(cnt)
            if ft in ('AS_SCHEDULED', 'STUDENT_IT_PROBLEM', 'TEACHER_IT_PROBLEM', 'SYSTEM_PROBLEM'):
                total_cnt += int(cnt)
    return [[db1_cnt, db2_cnt, total_cnt] ,[db1_as_cnt, db2_as_cnt, total_as_cnt]]


def get_problem_rate(result):
    problem_cnt, total_cnt = 0, 0
    for line in result:
        cnt, ft, supplier = line
        if ft in ('TEACHER_IT_PROBLEM', 'SYSTEM_PROBLEM'):
            problem_cnt += int(cnt)
        if ft in ('AS_SCHEDULED', 'STUDENT_IT_PROBLEM', 'TEACHER_IT_PROBLEM', 'SYSTEM_PROBLEM'):
            total_cnt += int(cnt)
    return '%.4f' % float(problem_cnt/total_cnt)

def main():
    content_td = ''
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    yes_time_str = yes_time.strftime('%Y-%m-%d')
    yes_month_str = yes_time.strftime('%Y-%m')
    sql = "select count_num,finish_type,supplier_code from time_oc_finish_type where scheduled_date = '%s'" % yes_time_str
    sql_month = "select count_num,finish_type,supplier_code from time_oc_finish_type where scheduled_date like '%s%%'" % yes_month_str
    mysql = MySQL(my_config)
    result = mysql.result_lst(sql)
    result_month = mysql.result_lst(sql_month)
    if result:
        finish_rate = get_finish_rate(result)
        db1_cnt, db2_cnt, total_cnt = finish_rate[0]
        db1_as_cnt, db2_as_cnt, total_as_cnt = finish_rate[1]
        db1_finish_rate = '%.4f' % float(db1_as_cnt/db1_cnt)
        db1_finish_rate_percent = (float(db1_finish_rate) * 100)
        db2_finish_rate = '%.4f' % float(db2_as_cnt/db2_cnt)
        db2_finish_rate_percent = (float(db2_finish_rate) * 100)
        total_finish_rate = '%.4f' % float(total_as_cnt/total_cnt)
        total_finish_rate_percent = (float(total_finish_rate) * 100)
        ###
        problem_rate = get_problem_rate(result)
        problem_rate_percent = (float(problem_rate) * 100)
        problem_rate_month = get_problem_rate(result_month)
        problem_rate_month_percent = (float(problem_rate_month) * 100)
        content = '''
        A集合是as_scheduled状态课程数量；<br>B集合是as_scheduled,system_problem,student_problem,teacher_problem状态课程数量；<br>C集合是teacher_problem,system_problem状态课程数量(problem类)<br>;
        <br>
        <table border="1" cellpadding="5">
        <thead>
        <tr>
        <th>线路</th>
        <th>A集合</th>
        <th>B集合</th>
        <th>完课率(A集合/B集合)</th>
        </tr>
        </thead>
        <tr>
        <td style='text-align:center'>多贝1</td>
        <td style='text-align:center'>%s</td>
        <td style='text-align:center'>%s</td>
        <td style='text-align:center'>%s%%</td>
        </tr>
        <tr>
        <td style='text-align:center'>多贝2</td>
        <td style='text-align:center'>%s</td>
        <td style='text-align:center'>%s</td>
        <td style='text-align:center'>%s%%</td>
        </tr>
        <tr>
        <td style='text-align:center'>总计</td>
        <td style='text-align:center'>%s</td>
        <td style='text-align:center'>%s</td>
        <td style='text-align:center'>%s%%</td>
        </tr>
        </table>
        <hr>
        <b>故障率昨天(C集合/B集合): %s%%<br>
            故障率当月(C集合/B集合) %s%%<br>
        </b>
''' % (db1_as_cnt, db1_cnt, db1_finish_rate_percent, db2_as_cnt, db2_cnt, db2_finish_rate_percent, total_as_cnt, total_cnt, total_finish_rate_percent, problem_rate_percent, problem_rate_month_percent)
        Mail.send_mail(to_list, '%s online_class finish rate' % yes_time_str, content)
    else:
        pass
        

if __name__ == "__main__":
    main()
