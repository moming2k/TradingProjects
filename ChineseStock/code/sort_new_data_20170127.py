#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sort_new_data_20170127
# @Date: 2017-01-27
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd

from path_info import original_new_data, minute_level_data_path, daily_ticker_sep_path
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
        first_date = group_df.first_valid_index()
        last_date = group_df.last_valid_index()
        open_price = group_df.ix[first_date, 'open']
        close_price = group_df.ix[last_date, 'close']
        volume = group_df.volume.sum()
        high_price = max(group_df.open.max(), group_df.close.max())
        low_price = max(group_df.open.min(), group_df.close.min())
        return pd.Series({const.STOCK_OPEN_PRICE: open_price, const.STOCK_CLOSE_PRICE: close_price,
                          const.STOCK_HIGH_PRICE: high_price, const.STOCK_LOW_PRICE: low_price,
                          const.STOCK_VOLUME: volume})

    result = date_groups.apply(process_group)
    result['date'] = result.index
    result['date'] = result.date.apply(lambda x: datetime.datetime.strptime(x, '%Y%m%d'))
    result = result.set_index('date', drop=True)
    result.to_pickle(os.path.join(daily_ticker_sep_path, file_name))
    return result


if __name__ == '__main__':
    import pathos

    pool = pathos.multiprocessing.ProcessingPool(4)
    # file_list = os.listdir(original_new_data)

    # pool.map(process_file_info, file_list)

    file_list = os.listdir(minute_level_data_path)
    pool.map(generate_daily_date, file_list)
