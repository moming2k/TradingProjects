#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: mert_20170127_date
# @Date: 2017-01-29
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from path_info import daily_date_sep_path, daily_ticker_sep_path
from constants import Constant as const

file_list = os.listdir(daily_ticker_sep_path)

df_list = []

for file_name in file_list:
    tmp_df = pd.read_pickle(os.path.join(daily_ticker_sep_path, file_name))
    tmp_df[const.STOCK_DATE] = tmp_df.index
    tmp_df[const.STOCK_DATE] = tmp_df[const.STOCK_DATE].apply(lambda x: x.strftime('%Y%m%d'))
    tmp_df.ix[:, const.STOCK_TICKER] = file_name[:6]
    if 'SH' in file_name:
        tmp_df.ix[:, const.STOCK_MARKET_TYPE] = 1
    else:
        tmp_df.ix[:, const.STOCK_MARKET_TYPE] = 4

    df_list.append(tmp_df)

merged_df = pd.concat(df_list, ignore_index=True)

merged_group = merged_df.groupby(const.STOCK_DATE)

keys = merged_group.groups.keys()

for key in keys:
    tmp_df = merged_group.get_group(key)
    tmp_df.to_pickle(os.path.join(daily_date_sep_path, '{}.p'.format(key)))
