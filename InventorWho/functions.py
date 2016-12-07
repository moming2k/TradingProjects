#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: functions
# @Date: 2016-12-06
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import datetime

def str2int(int_str):
    try:
        return int(int_str)
    except Exception:
        return int_str


def data_str2datetime(date_str):
    if '/' in date_str:
        return datetime.datetime.strptime(date_str, '%m/%d/%Y')

    elif '-' in date_str:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d')

    else:
        return datetime.datetime.strptime(date_str, '%Y%m%d')

def format_inventor_year(year):
    if year > 9000:
        return year - 7200
    else:
        return year