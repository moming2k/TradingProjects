#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step1_generate_buy_only_report_info
# @Date: 2017-01-14
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os

import pandas as pd

from constant import Constant as const

root_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'

data_path = os.path.join(root_path, 'data')
buy_only_report_data_path = os.path.join(data_path, 'report_info_buy_only')

report_info = pd.read_excel(os.path.join(data_path, 'insider2007_2016.xlsx'))

report_info = report_info[report_info[const.REPORT_ACTION] == const.OVERWEIGHT]

report_groups = report_info.groupby(const.REPORT_TICKER)


def save_dataframe(df):
    ticker_info = df.ix[df.first_valid_index(), const.REPORT_TICKER]
    df.to_pickle(os.path.join(buy_only_report_data_path, ticker_info))


report_groups.apply(save_dataframe)
