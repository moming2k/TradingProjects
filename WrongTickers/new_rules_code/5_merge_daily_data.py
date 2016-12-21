#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: 5_merge_daily_data
# Author: warn
# Date: warn

import os
import datetime

import pandas as pd
import numpy as np

root_path = '/home/wangzg/Documents/WangYouan/research/Wrong_tickers/temp/20161218'

today_str = datetime.datetime.today().strftime('%Y%m%d')

temp_path = os.path.join(root_path, 'temp')
today_temp_path = os.path.join(temp_path, today_str)
data_path = os.path.join(root_path, 'data')
result_path = os.path.join(root_path, 'result_csv')
stock_data_path = os.path.join(root_path, 'Stock_data')

if not os.path.isdir(today_temp_path):
    os.makedirs(today_temp_path)

for days in [1, 2, 3, 5, 10, 30]:
    df_2a2b = pd.read_pickle(os.path.join(temp_path, '20161218', 'pair_2a2b_days_{}_add_market_data.p'.format(days)))
    df_4a = pd.read_pickle(os.path.join(temp_path, '20161218', 'pair_4a_days_{}_add_market_data.p'.format(days)))
    df_4a[u'Volume_wrong'] = df_4a[u'Volume_wrong'].apply(lambda x: int(x) if np.isfinite(x) else 0)
    df_2a2b[u'Volume_wrong'] = df_2a2b[u'Volume_wrong'].apply(lambda x: int(x) if np.isfinite(x) else 0)

    df_2a2b.to_csv(os.path.join(today_temp_path, 'pair_2a2b_days_{}_add_market_data.csv'.format(days)), index=False)
    df_4a.to_csv(os.path.join(today_temp_path, 'pair_4a_days_{}_add_market_data.csv'.format(days)), index=False)

    df_2a2b.to_stata(os.path.join(today_temp_path, 'pair_2a2b_days_{}_add_market_data.dta'.format(days)),
                     write_index=False)
    df_4a.to_stata(os.path.join(today_temp_path, 'pair_4a_days_{}_add_market_data.dta'.format(days)),
                   write_index=False)

    new_df = pd.concat([df_2a2b, df_4a], axis=0, ignore_index=True)
    new_df.to_csv(os.path.join(today_temp_path, 'join_days_{}_pair_data.csv'.format(days)))
    new_df.to_stata(os.path.join(today_temp_path, 'join_days_{}_pair_data.dta'.format(days)))
