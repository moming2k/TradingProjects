#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: generate_volume_df
# Author: Mark Wang
# Date: 13/9/2016

import os
import datetime

import pandas as pd

parent_path = '/home/wangzg/Documents/WangYouan/research/Wrong_tickers'

if __name__ == '__main__':
    volume_df = pd.read_csv(os.path.join(parent_path, 'Stock_data', 'Volume.csv'), dtype={'date': str},
                            usecols=['date', 'VOL'])
    # open_close_df = open_close_df.sample(100)
    # open_close_df['date'] = open_close_df['date'].apply(lambda x: datetime.datetime.strptime(x, "%Y%m%d"))
    volume_groups = volume_df.groupby('date')
    new_df = pd.DataFrame(columns=['TradingVolume'])
    for date, sub_volume_df in volume_groups:
        true_date = datetime.datetime.strptime(date, "%Y%m%d")
        new_df.loc[true_date] = {'TradingVolume': int(sub_volume_df['VOL'].sum())}
    new_df = new_df.rename_axis('date')

    new_df.to_csv(os.path.join(parent_path, 'Stock_data', 'daily_volume_info.csv'), encoding='utf8')
