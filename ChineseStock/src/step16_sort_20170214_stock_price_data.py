#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step16_sort_20170214_stock_price_data
# @Date: 2017-02-14
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import datetime
import os

import pandas as pd

from constants.path_info import stock_20170214_path, stock_path, temp_path
from constants import Constant as const

new_data_path = os.path.join(stock_path, 'stock_price_20170214')
temp_stock_path = os.path.join(temp_path, 'stock_price')

sz_path = os.path.join(new_data_path, 'STOCK_SZ')
sh_path = os.path.join(new_data_path, 'STOCK_SH')


def process_df(df, ticker):
    """ Formatting input file """
    result_df = pd.DataFrame(index=df.index)
    result_df[const.STOCK_DATE] = df['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    result_df.loc[:, const.STOCK_TICKER] = ticker
    result_df[const.STOCK_OPEN_PRICE] = df['open']
    result_df[const.STOCK_CLOSE_PRICE] = df['close']
    result_df[const.STOCK_HIGH_PRICE] = df['high']
    result_df[const.STOCK_LOW_PRICE] = df['low']
    result_df[const.STOCK_VOLUME] = df['volume']
    return result_df


# Format stock price file and save it into temp file
df_list = []
for dir_path in [sz_path, sh_path]:
    file_list = os.listdir(dir_path)
    for file_name in file_list:
        df = pd.read_csv(os.path.join(dir_path, file_name))
        ticker = file_name[:6]
        new_df = process_df(df, ticker)
        new_df.to_pickle(os.path.join(temp_stock_path, '{}.p'.format(ticker)))
        df_list.append(new_df)

merged_df = pd.concat(df_list, axis=0, ignore_index=True)
trading_days_list = merged_df.Trddt.drop_duplicates().sort_values()

groups = merged_df.groupby(const.STOCK_DATE)


def save_groups(group):
    date_info = group.ix[group.first_valid_index(), const.STOCK_DATE]
    group.to_pickle(os.path.join(stock_20170214_path, '{}.p'.format(date_info.strftime('%Y%m%d'))))


groups.apply(save_groups)
