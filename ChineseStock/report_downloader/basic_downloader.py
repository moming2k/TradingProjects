#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: basic_downloader
# @Date: 2017-02-19
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import logging
import datetime

from http_ctrl import HttpCtrl
from url_constants import URLConstant


class BasicDownloader(URLConstant):
    def __init__(self, logger=None):
        if logger is None:
            logger = logging
        self.logger = logger.getLogger(self.__class__.__name__)
        self.ctrl = HttpCtrl(logger)

    def download_report(self, start_date=None, end_date=None):
        pass

    @staticmethod
    def get_datetime_type_str(date_str):
        try:
            return datetime.datetime.strptime(date_str, '%Y-%m-%d')
        except Exception:
            return None

    @staticmethod
    def get_int_type_str(int_str):

        try:
            return int(int_str)
        except Exception:
            return None

    @staticmethod
    def get_float_type_str(input_str):

        try:
            return float(input_str)
        except Exception:
            return None

    @staticmethod
    def get_root_path():
        if hasattr(os, 'uname'):
            if os.uname()[1] == 'ewin3102':
                return '/home/zigan/Documents/WangYouan/trading/ChineseStock'
            elif os.uname()[0] == 'Darwin':
                return '/Users/warn/PycharmProjects/QuestionFromProfWang/ChineseStock'
            else:
                return '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'
        else:
            return r'C:\Users\CFID\Documents\ChinaStock'
