#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step2_calculate_return_data_wd
# @Date: 2017-01-09
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd
import numpy as np

from constant import Constant

const = Constant()

# Define some folder path
today_str = datetime.datetime.today().strftime('%Y%m%d')
root_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'
data_path = os.path.join(root_path, 'data')
temp_path = os.path.join(root_path, 'temp')
today_path = os.path.join(temp_path, today_str)

if not os.path.isdir(today_path):
    os.makedirs(today_path)

# read data file
# stock_data = pd.read_pickle(os.path.join(temp_path, '20170106', 'daily_0516.p'))
report_info = pd.read_excel(os.path.join(data_path, 'insider2007_2016.xlsx'))

holding_days = 22