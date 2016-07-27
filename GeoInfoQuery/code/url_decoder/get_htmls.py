#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: get_htmls
# Author: Mark Wang
# Date: 27/7/2016

import re
import urllib2

import js2py


def get(cid):
    url = 'https://maps.google.com/?cid={}'.format(cid)
    req = urllib2.urlopen(url)
    return req.read()


def get_html_file():
    cid_list = ["9207955936104980714"]

    index = 6
    for cid in cid_list:
        file_name = "file{}.html".format(index)
        html = get(cid)
        with open(file_name, 'w') as f:
            f.write(html)
        index += 1


if __name__ == '__main__':
    get_html_file()
    # html = ""
    # with open('file5.html') as f:
    #     html = f.read()
    #
    # result = re.findall(r'cacheResponse\((.*)\)', html)
    # print result[0]
    #
    # left_brace = 0
    # s = list(result[0])
    # new_s = []
    # index = 0
    # for c in s[1:-1]:
    #     if c == '[':
    #         left_brace += 1
    #     if c == ']':
    #         left_brace -= 1
    #
    #     if left_brace == 0 and c == ',':
    #         index += 1
    #     elif index > 9:
    #         break
    #     elif index == 9:
    #         new_s.append(c)
    #
    # s = ''.join(new_s)
    # print s