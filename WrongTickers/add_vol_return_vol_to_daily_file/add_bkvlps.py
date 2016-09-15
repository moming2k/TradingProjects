#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_bkvlps
# Author: Mark Wang
# Date: 14/9/2016

import os

import pandas as pd
import numpy as np
import pathos

from ..constants import *

parent_path = '/home/wangzg/Documents/WangYouan/research/Wrong_tickers'
data_dir = 'Stock_data'
result_dir = 'result_csv'
bkvlps_df = pd.read_csv(os.path.join(parent_path, data_dir, 'BKVLPS.csv'),
                        usecols=['fyear', 'cusip', 'bkvlps', 'tic'],
                        dtype={'fyear': str, 'cusip': str},
                        )
# bkvlps_df['cusip'] = bkvlps_df['cusip'].apply(lambda x: x[:-1] if isinstance(x, str) else np.nan)


def get_bkvlps_from_row_info(row):
    year = row[DATE][:4]
    wrong_ticker = row[TICKER_WRONG]
    wrong_cusip = row[CUSIP_WRONG]
    sub_df = bkvlps_df[bkvlps_df['fyear'] == year]
    if sub_df.empty:
        return np.nan
    target_list = sub_df[sub_df['cusip'] == wrong_cusip].bkvlps.tolist()
    if target_list:
        return target_list[0]

    target_list = sub_df[sub_df['tic'] == wrong_ticker].bkvlps.tolist()
    if target_list:
        return target_list[0]

    else:
        return np.nan


def process_df(df):
    data_series = df.apply(get_bkvlps_from_row_info, axis=1)
    return data_series


if __name__ == "__main__":
    process_num = 16
    pool = pathos.multiprocessing.ProcessingPool(process_num)
    data_df = pd.read_csv(os.path.join(parent_path, result_dir, 'wrong_ticker_whole_daily_data_SDC(add_daily).csv'),
                          dtype={CUSIP_WRONG: str, CUSIP_REAL: str})
    split_dfs = np.array_split(data_df, process_num, axis=0)
    result_dfs = pool.map(process_df, split_dfs)
    result_df = pd.concat(result_dfs, axis=0)
    data_df['{}_{}'.format(BOOK_VALUE_PER_SHARE, WRONG)] = result_df
    data_df.to_csv(os.path.join(parent_path, result_dir, 'wrong_ticker_whole_daily_data_SDC(add_bkvlps).csv'),
                   index=False, encoding='utf8')
