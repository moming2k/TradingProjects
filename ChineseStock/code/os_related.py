#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: os_related
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os


def get_root_path():
    if hasattr(os, 'uname'):
        if os.uname()[1] == 'ewin3102':
            return '/home/zigan/Documents/WangYouan/trading/ChineseStock'
        else:
            return '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'
    else:
        return r'C:\Users\CFID\Documents\ChinaStock'


def get_process_num():
    if hasattr(os, 'uname'):
        if os.uname()[1] == 'ewin3102':
            return 30
        else:
            return 15
    else:
        return 30
