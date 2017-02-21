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
        if date_str is None:
            return date_str
        try:
            date = datetime.datetime.strptime(date_str.strip(), '%Y-%m-%d')
            if date < datetime.datetime(1677, 9, 21) or date > datetime.datetime(2262, 4, 11):
                return date_str
            else:
                return date
        except Exception:
            return None

    @staticmethod
    def get_int_type_str(int_str):
        if int_str is None:
            return int_str

        try:
            return int(int_str.strip())
        except Exception:
            return None

    @staticmethod
    def get_float_type_str(input_str):
        if input_str is None:
            return input_str

        try:
            return float(input_str.strip())
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
