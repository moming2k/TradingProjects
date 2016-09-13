#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: generate_stock_volatility
# Author: Mark Wang
# Date: 13/9/2016

import os
import datetime

import pandas as pd

parent_path = '/home/wangzg/Documents/WangYouan/research/Wrong_tickers'

if __name__ == '__main__':
    highlow_df = pd.read_csv(os.path.join(parent_path, 'Stock_data', 'highlow.csv'), dtype={'date': str},
                             usecols=['date', 'BIDLO', 'ASKHI'])
    # open_close_df = open_close_df.sample(100)
    # open_close_df['date'] = open_close_df['date'].apply(lambda x: datetime.datetime.strptime(x, "%Y%m%d"))
    highlow_groups = highlow_df.groupby('date')
    new_df = pd.DataFrame(columns=['Volatility'])
    for date, sub_df in highlow_groups:
        true_date = datetime.datetime.strptime(date, "%Y%m%d")
        volatility = (sub_df['ASKHI'] - sub_df['BIDLO']) * 2 / (sub_df['ASKHI'] + sub_df['BIDLO'])
        new_df.loc[true_date] = {'Volatility': volatility.mean()}
    new_df = new_df.rename_axis('date')

    new_df.to_csv(os.path.join(parent_path, 'Stock_data', 'daily_stock_volatility.csv'), encoding='utf8')
