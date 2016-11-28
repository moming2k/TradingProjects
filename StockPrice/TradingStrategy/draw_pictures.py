#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: draw_pictures
# Author: Mark Wang
# Date: 25/11/2016

import os
import shutil

import pandas as pd

from functions import plot_output_data

root_path = '/home/wangzg/Documents/WangYouan/research/HongKongStock/20161125SimulateResult'

data_path = os.path.join(root_path, 'data')

photo_path = os.path.join(root_path, 'photo')

max_sharpe_path = os.path.join(root_path, 'max_sharpe')

significant_path = os.path.join(root_path, 'significant')

if not os.path.isdir(photo_path):
    os.makedirs(photo_path)

if not os.path.isdir(max_sharpe_path):
    os.makedirs(max_sharpe_path)

if not os.path.isdir(significant_path):
    os.makedirs(significant_path)

for stock in os.listdir(data_path):
    stock_path = os.path.join(data_path, stock)
    if not os.path.isdir(stock_path) or not str.isdigit(stock):
        continue

    max_sharpe = 0
    max_sharpe_file = None

    for performance in os.listdir(stock_path):
        if not performance.startswith('p1') or not performance.endswith('.csv'):
            continue

        sharpe = float(performance[:-4].split('_')[-1])
        if sharpe > max_sharpe:
            max_sharpe = sharpe
            max_sharpe_file = performance

    if max_sharpe_file is None:
        continue

    df = pd.read_csv(os.path.join(stock_path, max_sharpe_file), index_col=0, skiprows=31,
                     names=['open', 'high', 'low', 'Close', 'volume', 'close', 'wealth', 'short', 'long', 'cash',
                            'pnl', 'long_pos', 'short_pos', 'operation']
                     )
    plot_output_data(df, max_sharpe, os.path.join(photo_path, '{}.png'.format(stock)), '{}.HK'.format(stock))
    shutil.copy(os.path.join(stock_path, max_sharpe_file),
                os.path.join(max_sharpe_path, '{}_{}'.format(stock, max_sharpe_file)))

    if max_sharpe > 1:
        shutil.copy(os.path.join(stock_path, max_sharpe_file),
                    os.path.join(significant_path, '{}_{}'.format(stock, max_sharpe_file)))
