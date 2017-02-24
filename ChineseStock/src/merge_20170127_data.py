#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: mert_20170127_date
# @Date: 2017-01-29
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from constants.path_info import daily_ticker_sep_path, temp_path
from util_functions.os_related import make_dirs

file_list = os.listdir(daily_ticker_sep_path)

# df_dict = []
#
# for file_name in file_list:
#     tmp_df = pd.read_pickle(os.path.join(daily_ticker_sep_path, file_name))
#     tmp_df[const.STOCK_DATE] = tmp_df.index
#     tmp_df[const.STOCK_DATE] = tmp_df[const.STOCK_DATE].apply(lambda x: x.strftime('%Y%m%d'))
#     tmp_df.ix[:, const.STOCK_TICKER] = file_name[:6]
#     if 'SH' in file_name:
#         tmp_df.ix[:, const.STOCK_MARKET_TYPE] = 1
#     else:
#         tmp_df.ix[:, const.STOCK_MARKET_TYPE] = 4
#
#     df_dict.append(tmp_df)
#
# merged_df = pd.concat(df_dict, ignore_index=True)
#
# merged_group = merged_df.groupby(const.STOCK_DATE)
#
# keys = merged_group.groups.keys()
#
# for key in keys:
#     tmp_df = merged_group.get_group(key)
#     tmp_df.to_pickle(os.path.join(daily_date_sep_path, '{}.p'.format(key)))

output_path = os.path.join(temp_path, 'stock_price_data')

make_dirs([output_path])

for file_name in file_list:
    tmp_df = pd.read_pickle(os.path.join(daily_ticker_sep_path, file_name))
    tmp_df.to_csv(os.path.join(output_path, '{}.csv'.format(file_name[:-2])))
