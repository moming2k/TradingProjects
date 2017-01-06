#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: test_insider
# @Date: 2017-01-06
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd
import numpy as np

from constant import Constant as const

today_str = datetime.datetime.today().strftime('%Y-%m-%d')
root_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'
data_path = os.path.join(root_path, 'data')
temp_path = os.path.join(root_path, 'temp')
today_path = os.path.join(temp_path, today_str)

if not os.path.join(today_path):
    os.makedirs(today_path)

report_info = pd.read_excel(os.path.join(data_path, 'insider2007_2016.xlsx'))
stock_data = pd.read_sas(os.path.join(data_path, 'daily_0516.sas7bdat'))
stock_data.loc[:, 'Markettype'] = stock_data['Markettype'].apply(int)
stock_data.loc[:, 'Trdsta'] = stock_data['Trdsta'].apply(int)
stock_data.loc[:, const.STOCK_DATE] = stock_data[const.STOCK_DATE].apply(
    lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
stock_data.to_pickle(os.path.join(today_path, 'daily_0516.p'))
