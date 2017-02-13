#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: util_functions
# @Date: 2017-02-13
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import urllib
import urllib2


def get(url, data_list=None, max_try=3):
    if data_list:
        url = "{}?{}".format(url, urllib.urlencode(data_list))
    query = urllib2.Request(url)
    current_try = 0
    while current_try < max_try:
        try:
            response = urllib2.urlopen(query)
            html = ''
            while True:
                current_html = response.read(1024)
                print current_html
                if not len(current_html):
                    break

                html = '{}{}'.format(html, current_html)

            response.close()
            return html
        except Exception, e:
            return None
    raise Exception("Cannot open page {}".format(url))


if __name__ == '__main__':
    html = get('http://www.hkjc.com/chinese/racing/selecthorsebychar.asp', ('ordertype', 4))
    print html
