#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: generate_market_return
# Author: Mark Wang
# Date: 13/9/2016

import os
import datetime

import pandas as pd

parent_path = '/home/wangzg/Documents/WangYouan/research/Wrong_tickers'

if __name__ == '__main__':
    open_close_df = pd.read_csv(os.path.join(parent_path, 'Stock_data', 'open_close.csv'), dtype={'date': str},
                                usecols=['date', 'PRC', 'OPENPRC'])
    # open_close_df = open_close_df.sample(100)
    open_close_groups = open_close_df.groupby('date')
    new_df = pd.DataFrame(columns=['MarketReturn'])
    for date, sub_df in open_close_groups:
        true_date = datetime.datetime.strptime(date, "%Y%m%d")
        market_return = (sub_df['PRC'] - sub_df['OPENPRC']) / sub_df['OPENPRC']
        new_df.loc[true_date] = {'MarketReturn': market_return.mean()}
    new_df = new_df.rename_axis('date')

    new_df.to_csv(os.path.join(parent_path, 'Stock_data', 'daily_market_return.csv'), encoding='utf8')