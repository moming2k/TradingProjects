#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step1_generate_return_info_with_reduction
# @Date: 2017-01-08
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd
import numpy as np

from constant import Constant
from functions import calculate_trade_info

const = Constant()

# Define some folder path
today_str = datetime.datetime.today().strftime('%Y%m%d')
root_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'
data_path = os.path.join(root_path, 'data')
temp_path = os.path.join(root_path, 'temp')
today_path = os.path.join(temp_path, today_str)
stock_price_path = os.path.join(root_path, 'stock_price')
report_action_path = os.path.join(data_path, 'report_info')

if not os.path.isdir(today_path):
    os.makedirs(today_path)

if not os.path.isdir(report_action_path):
    os.makedirs(report_action_path)

# read data file
trading_day_list = pd.read_pickle(os.path.join(temp_path, '20170108', 'trading_days_list.p'))

report_info = pd.read_excel(os.path.join(data_path, 'insider2007_2016.xlsx'))
report_groups = report_info.groupby(const.REPORT_TICKER)

holding_days = 22


def delete_unused_info(df):
    date_groups = df.groupby(const.REPORT_ANNOUNCE_DATE)
    result_df = pd.DataFrame()

    for _, group in date_groups:
        if group.drop_duplicates(const.REPORT_ACTION).shape[0] > 1:
            continue
        else:
            result_df = result_df.append(group, ignore_index=False)

    return result_df


result_groups = report_groups.apply(delete_unused_info)
index = result_groups.index.levels[0]

for ticker in index:
    result_groups.ix[ticker].to_pickle(os.path.join(report_action_path, '{}.p'.format(ticker)))



