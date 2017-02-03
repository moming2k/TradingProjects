#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: http_operation
# @Date: 2017-02-02
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import urllib
import urllib2
import traceback


def get(url, data_list=None, max_try=3):
    if data_list:
        url = "{}?{}".format(url, urllib.urlencode(data_list))
    query = urllib2.Request(url)
    current_try = 0
    while current_try < max_try:
        try:
            response = urllib2.urlopen(query)
            html = response.read()
            response.close()
            return html
        except Exception, e:
            traceback.print_exc()
            current_try += 1
    raise Exception("Cannot open page {}".format(url))
