import os
import smtplib                           #发送邮件模块
from email.mime.text import MIMEText    #定义邮件内容
from email.header import Header         #定义邮件标题
from email.mime.multipart import MIMEMultipart  #用于传送附件
from test_run.run import *


def send_mail(latest_report):
    f = open(latest_report, 'rb')
    mail_content = f.read()
    f.close()

    # 发送邮箱服务器
    # smtpserver='smtp.163.com'
    smtpserver = 'smtp.exmail.qq.com'

    # 发送邮箱用户名密码
    # user='leilei3356@163.com'
    # password='leilei123456'
    user = 'leil@excetop.com'
    password = 'Yj72bTdyBrEkzYZs'

    # 发送和接收邮箱
    sender = 'leil@excetop.com'
    receives = ['leil@excetop.com']
    # receives = ['1591505373@qq.com', 'leilei3356@163.com']

    # 发送邮件主题和内容
    subject = '接口测试报告'

    # 构造附件内容
    send_file = open(latest_report, 'rb').read()
    att = MIMEText(send_file, 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment;filename="test_report.html"'

    # 构建发送与接收信息
    msgRoot = MIMEMultipart()
    msgRoot.attach(MIMEText(mail_content, 'html', 'utf-8'))
    msgRoot['subject'] = Header(subject, 'utf-8')
    msgRoot['From'] = sender
    msgRoot['To'] = ','.join(receives)
    msgRoot.attach(att)

    smtp = smtplib.SMTP_SSL(smtpserver, 465)

    # HELO 向服务器标识用户身份
    smtp.helo(smtpserver)
    # 服务器返回结果确认
    smtp.ehlo(smtpserver)
    # 登录邮箱服务器用户名和密码
    smtp.login(user, password)

    print("Start send Email...")
    smtp.sendmail(sender, receives, msgRoot.as_string())
    smtp.quit()
    print("Send Email end!")

def latest_report(report_dir):
    lists = os.listdir(report_dir)
    # 按时间顺序对该目录文件夹下面的文件进行排序
    lists.sort(key=lambda fn: os.path.getatime(report_dir + '\\' + fn))
    print(("new report is :" + lists[-1]))

    file = os.path.join(report_dir, lists[-1])
    print(file)
    return file


if __name__ == '__main__':
    run_case()
    # h获取最新测试报告
    latest_report = latest_report(report_dir)
    # 发送邮件报告
    send_mail(latest_report)
