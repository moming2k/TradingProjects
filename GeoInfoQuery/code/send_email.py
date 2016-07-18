#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: send_email
# Author: Mark Wang
# Date: 18/7/2016

import smtplib
from email import MIMEMultipart
from email import MIMEText


def send_email_through_126(subject, msg_body, to_addr='wangyouan@gmail.com'):
    server = smtplib.SMTP('smtp.126.com', 25)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('wyatc@126.com', '1212az1212AZ')

    msg = MIMEMultipart.MIMEMultipart()
    msg['From'] = 'wyatc@126.com'
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText.MIMEText(msg_body, 'plain'))
    text = msg.as_string()
    server.sendmail('wyatc@126.com', to_addr, text)
    server.close()


if __name__ == "__main__":
    send_email_through_126('Project Finished', 'Your test is successfully completed', to_addr='markwang@connect.hku.hk')
