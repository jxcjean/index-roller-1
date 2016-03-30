import smtplib
from email.mime.text import MIMEText
from email.header import Header
import json
import datetime
import time

def send_email():
    # 系统时间
    unix = time.time()
    system_date_ymdhms_string = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))  # 获取系统时间

    # 解析json文件，获取登录密码
    f = open('email.json')
    content = json.load(f)
    mail_password = str(content.get('password'))
    mail_send_to_address = str(content.get('address'))
    sender = 'Index Roller'
    mail_host = 'smtp.163.com'
    mail_username = 'jxcjean'
    mail_postfix = '163.com'
    me = '<' + mail_username + '@' + mail_postfix + '>'
    msg = MIMEText('Index Roller策略触发，请检查', 'text', 'utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
    msg['Subject'] = Header('Index Roller策略触发，请检查_' + system_date_ymdhms_string, 'utf-8')
    msg['From'] = me
    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_host)
        smtp.login(mail_username, mail_password)
        smtp.sendmail(me, mail_send_to_address, msg.as_string())
        smtp.quit()
        print('发送通知邮件成功')
    except:
        print('发送通知邮件失败')
#send_email()
