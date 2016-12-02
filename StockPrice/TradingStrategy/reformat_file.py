#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: reformat_file
# Author: warn
# Date: 2016/12/3

import os

import pandas as pd

from functions import plot_output_data

root_path = '~/Documents/WangYouan/research/HongKongStock/20161125SimulateResult/data'

for stock_name, file_name in [('0169', 'p1_6_p2_30_p3_19_th_0.1_sharpe_0.0292.csv'),
                              ('0929', 'p1_6_p2_14_p3_7_th_0.1_sharpe_0.0253.csv'),
                              ('0289', 'p1_8_p2_24_p3_19_th_1.1_sharpe_0.0591.csv')]:
    df = pd.read_csv(
        os.path.join(root_path, stock_name, file_name),
        index_col=0, skiprows=31,
        names=['open', 'high', 'low', 'Close', 'volume', 'close', 'wealth', 'short', 'long', 'cash',
               'pnl', 'long_pos', 'short_pos', 'operation']
    )

    plot_output_data(df, float(file_name[:-4].split('_')[-1]),
                     '{}.png'.format(stock_name),
                     '{}.HK'.format(stock_name))
