#coding:utf-8

import os
import ConfigParser
import subprocess
import logging




'''

    可以写个修饰器 或者公共函数 判断log var config 目录是否存在

'''

base_dir = os.path.split(os.path.realpath(__file__))[0]
configure_file = '%s/config/MySQLConfigure' % base_dir




def get_info_dict(opt):
    '''
    从configure_file中读取MySQL的连接配置文件，返回dict
    '''
    cf = ConfigParser.ConfigParser()
    cf.read(configure_file)
    kvs = cf.items(opt)
    if kvs:
        return dict(kvs)
    else:
        return 0



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


'''
判断路径是否存在 不存在就新建
'''
def mkdirs(f_path):
    if os.path.exists(f_path):
        pass
    else:
        os.makedirs(f_path)






# 字节bytes转化kb\m\g
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)







'''
判断路径的大小
'''
def getPathSize(path):
    sumsize = 0
    try:
        filename = os.walk(path)
        for root, dirs, files in filename:
            for fle in files:
                size = os.path.getsize(path + fle)
                sumsize += size
        return formatSize(sumsize)
    except Exception as err:
        print(err)




from os.path import join, getsize
def getdirsize(dir):

    size = 0L
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    return formatSize(size)


'''
判断文件的大小
'''
def getFileSize(file):
    try:
        size = os.path.getsize(file)
        return formatSize(size)
    except Exception as err:
        print(err)


class TmpFile:
    def __init__(self, tmpfile):
        self.tmpfile = tmpfile

    def recode_info(self, info):
        """
        """
        in_put = open(self.tmpfile, 'w')
        in_put.writelines(info)
        in_put.close()

    def get_content(self):
        """
        """
        try:
            out_put = open(self.tmpfile)
            content = out_put.readline()
            out_put.close()
        except:
            return {}
        return dict(eval(content))






import smtplib
from email.mime.text import MIMEText


def send_mail(to_list,content, sub):
    mail_user = "wffeige3@163.com"
    mail_pass = "wf813776"
    mail_host = "smtp.163.com"



    me = "autopost"+ "<" + mail_user + ">"
    msg = MIMEText(content, _subtype='html', _charset='utf8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)

    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False






























