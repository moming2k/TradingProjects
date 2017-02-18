#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sort_new_data_20170127
# @Date: 2017-01-27
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd

from path_info import original_new_data, minute_level_data_path, daily_ticker_sep_path, daily_date_sep_path
from constants import Constant as const


def process_file_info(file_name):
    df = pd.read_csv(os.path.join(original_new_data, file_name))
    df['time'] = df.time.apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    df = df.set_index('time', drop=True).drop(['high', 'low'], axis=1)
    df.to_pickle(os.path.join(minute_level_data_path, '{}.p'.format(file_name[:-4])))
    return None


def generate_daily_date(file_name):
    df = pd.read_pickle(os.path.join(minute_level_data_path, file_name))
    df['date'] = df.index
    df['date'] = df.date.apply(lambda x: x.strftime('%Y%m%d'))
    date_groups = df.groupby('date')

    def process_group(group_df):
        date_index = group_df.index
        if len(date_index) > 1:
            open_price = group_df.ix[date_index[0], 'open']
            close_price = group_df.ix[date_index[-1], 'close']
            open_price_2 = group_df.ix[date_index[1], 'open']
            close_price_2 = group_df.ix[date_index[-2], 'close']
        else:
            open_price = group_df.ix[date_index[0], 'open']
            close_price = group_df.ix[date_index[0], 'close']
            open_price_2 = group_df.ix[date_index[0], 'open']
            close_price_2 = group_df.ix[date_index[0], 'close']

        volume = group_df.volume.sum()
        high_price = max(group_df.open.max(), group_df.close.max())
        low_price = max(group_df.open.min(), group_df.close.min())
        return pd.Series({const.STOCK_OPEN_PRICE: open_price, const.STOCK_CLOSE_PRICE: close_price,
                          const.STOCK_HIGH_PRICE: high_price, const.STOCK_LOW_PRICE: low_price,
                          const.STOCK_VOLUME: volume, const.STOCK_OPEN_PRICE2: open_price_2,
                          const.STOCK_CLOSE_PRICE2: close_price_2})

    result = date_groups.apply(process_group)
    result['date'] = result.index
    result['date'] = result.date.apply(lambda x: datetime.datetime.strptime(x, '%Y%m%d'))
    result = result.set_index('date', drop=True)
    result.to_pickle(os.path.join(daily_ticker_sep_path, file_name))
    return result


if __name__ == '__main__':
    import pathos

    pool = pathos.multiprocessing.ProcessingPool(15)
    # file_list = os.listdir(original_new_data)

    # pool.map(process_file_info, file_list)

    file_list = os.listdir(minute_level_data_path)
    pool.map(generate_daily_date, file_list)

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
