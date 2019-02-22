# -*- coding: utf-8 -*-
'''
@File  : sendEmail.py
@Date  : 2019/1/15/015 17:32
'''
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from common.parseConfig import ParseConfig
from config.config import RECEIVERS
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


pc = ParseConfig()
email_info = pc.get_info("email")


class SendEmail(object):
    def __init__(self):
        self.stmp = smtplib.SMTP(email_info["server"])
        self.msg = None

    def set_msg(self, text,part_path):
        message = MIMEMultipart()
        message.attach(MIMEText(text, 'plain', 'utf-8'))
        message['From'] = Header(email_info["msgfrom"], 'utf-8')  # 发送者
        subject = email_info["subject"]
        message['Subject'] = Header(subject, 'utf-8')

        with open(part_path,"rb") as f:
            part=MIMEApplication(f.read())
            part.add_header('Content-Disposition', 'attachment', filename="测试报告.xls")
            message.attach(part)
            f.close()
        self.msg = message

    def send_email(self, sender, recivers):
        self.stmp.login(email_info["user"], email_info["pwd"])
        self.stmp.sendmail(sender, recivers, self.msg.as_string())


def send_email_for_all(msg,part_path):
    """
    群发信息
    :param msg: 正文
    :param part_path:附件地址
    :return:
    """
    receivers = RECEIVERS
    sender = 'ning.tonggang@qianka.com'
    se = SendEmail()
    message="Dear all,\n  {},详情见附件：".format(msg)
    se.set_msg(message,part_path)
    se.send_email(sender, receivers)
