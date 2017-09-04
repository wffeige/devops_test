# -*- coding: utf-8 -*-
#!/usr/bin/python
import smtplib
from email.mime.text import MIMEText


mailto_list = ['wffeige@126.com']
mail_host = "smtp.163.com"
mail_user = "wffeige3@163.com"
mail_pass = "wf813776"
content="1231231231312313123123"

def send_mail(to_list,content, sub):

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


def send():
    send_mail(mailto_list,content,"慢查询")


send()

