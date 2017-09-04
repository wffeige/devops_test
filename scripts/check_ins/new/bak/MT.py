#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os, sys, logging, ConfigParser, subprocess, smtplib, datetime
from email.mime.text import MIMEText

base_dir = os.path.split(os.path.realpath(__file__))[0]
configure_file = '%s/MyConfigure' % base_dir

class Mail(object):
    mail_user = "zhanggong@vipkid.com.cn"
    mail_pass = "Vipkid-800"
    mail_host = "smtp.exmail.qq.com"    

    @classmethod    
    def send_mail(cls, to_list, sub, content):
        me = "CP"+ "<" + cls.mail_user + ">"
        msg = MIMEText(content, _subtype='html', _charset='utf8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            s = smtplib.SMTP()
            s.connect(cls.mail_host)
            s.login(cls.mail_user, cls.mail_pass)
            s.sendmail(me, to_list, msg.as_string())
            s.close()
            return True
        except Exception, e:
            print str(e)
            return False

def shell(cmd, type = 's'):
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        if type == 's':
            return p_status
        elif type == 'r':
            return output.strip()
    except:
        return -1

def logger(logfile):
    format = '%(asctime)s [%(filename)s][%(levelname)s] %(message)s'
    logging.basicConfig(level = logging.DEBUG, filename = logfile, filemode = 'a', format = format)
    logger = logging.getLogger()
    return logger

def get_rds_info_dict(opt):
    '''
    从configure_file中读取MySQL的连接配置文件，返回dict
    '''
    cf = ConfigParser.ConfigParser()
    cf.read(configure_file)
    kvs = cf.items(opt)
    if kvs:
        return dict(kvs)
    else:
        return

def get_today():
    now_time = datetime.datetime.now()
    return now_time.strftime('%y%m%d')
