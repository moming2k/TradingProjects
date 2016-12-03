#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: get_all_draw_down
# @Date: 2016-12-02
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from functions import max_draw_down

root_path = '/home/wangzg/Documents/WangYouan/research/HongKongStock/20161125SimulateResult/data'

statistic_df = pd.DataFrame(columns=['annualized_return', 'draw_back', 'sharpe_ratio'])

for stock in os.listdir(root_path):
    stock_path = os.path.join(root_path, stock)
    if not os.path.isdir(stock_path):
        continue

    max_ann = float('-inf')

    for data in os.listdir(stock_path):
        if not data.endswith('csv'):
            continue
        df = pd.read_csv(os.path.join(stock_path, data), index_col=0, skiprows=31,
                         names=['open', 'high', 'low', 'Close', 'volume', 'close', 'wealth', 'short', 'long', 'cash',
                                'pnl', 'long_pos', 'short_pos', 'operation'])
        sharpe = float(data[:-4].split('_')[-1])
        annualized_return = df.pnl.mean() * 247
        if annualized_return > max_ann:
            statistic_df.loc[data] = {'annualized_return': annualized_return,
                                      'sharpe_ratio': sharpe,
                                      'draw_back': max_draw_down(df)}
