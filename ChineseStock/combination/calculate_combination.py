#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: calculate_combination
# @Date: 2017-01-13
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd

from constant import Constant as const

today_str = datetime.datetime.today().strftime('%Y%m%d')

root_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'
data_path = os.path.join(root_path, 'data')
temp_path = os.path.join(root_path, 'temp')
today_path = os.path.join(temp_path, today_str)
stock_data_path = os.path.join(data_path, 'stock_price')
report_data_path = os.path.join(data_path, 'report_info')

if not os.path.isdir(today_path):
    os.makedirs(today_path)

trading_days = pd.read_pickle(os.path.join(data_path, 'trading_days_list.p'))
