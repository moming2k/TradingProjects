#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: util
# Author: Mark Wang
# Date: 24/7/2016

import urllib2
import json
import traceback
import time
import smtplib
from email import MIMEMultipart
from email import MIMEText


def send_email_through_gmail(subject, msg_body, to_addr='wangyouan@gmail.com'):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('wangyouan@gmail.com', 'battleraper')

    msg = MIMEMultipart.MIMEMultipart()
    msg['From'] = 'wangyouan@gmail.com'
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText.MIMEText(msg_body, 'plain'))
    text = msg.as_string()
    server.sendmail('wangyouan@gmail.com', to_addr, text)
    server.close()


def is_geocode_in_target_country(coordinate, country_code='usa'):
    """ Check given coordinate is in the U.S. or not """
    try:
        api_url = 'http://www.datasciencetoolkit.org/coordinates2politics'
        api_body = json.dumps(coordinate)
        response_string = urllib2.urlopen(api_url, api_body).read()
        query_result = json.loads(response_string, encoding='utf8')

        if 'error' in query_result:
            print coordinate
            print query_result['error']
            response_string = urllib2.urlopen(api_url, api_body).read()
            query_result = json.loads(response_string, encoding='utf8')
            if 'error' in query_result:
                raise Exception(query_result['error'])

    except Exception:
        traceback.print_exc()
        print coordinate
        time.sleep(30)
        api_url = 'http://www.datasciencetoolkit.org/coordinates2politics'
        api_body = json.dumps(coordinate)
        response_string = urllib2.urlopen(api_url, api_body).read()
        query_result = json.loads(response_string, encoding='utf8')
        if 'error' in query_result:
            print coordinate
            print query_result['error']
            response_string = urllib2.urlopen(api_url, api_body).read()
            query_result = json.loads(response_string, encoding='utf8')
            if 'error' in query_result:
                raise Exception(query_result['error'])

    query_result = query_result[0]
    if query_result['politics']:
        for info in query_result['politics']:
            if info['friendly_type'] == 'country':
                return info['code'] == country_code
    return False