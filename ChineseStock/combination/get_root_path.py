#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: get_root_path
# @Date: 2017-01-15
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os


def get_root_path():
    if hasattr(os, 'uname'):
        return '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'
    else:
        return 'D:\\wya\\Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}'
