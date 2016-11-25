#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: calculate_trading_days
# Author: Mark Wang
# Date: 25/11/2016

import os
import datetime

import pandas as pd

root_path = '/home/wangzg/Documents/WangYouan/research/HongKongStock'

stock_path = 'YahooStockPrice'

days = {}

for i in range(2001, 2016):
    days[str(i)] = 0


for file_name in os.listdir(os.path.join(root_path, stock_path)):
    if not str.isdigit(file_name[:-4]):
        continue
    df = pd.read_csv(os.path.join(root_path, stock_path, file_name), dtype={'Volume': int})
    df = df[df['Volume'] != 0]
    df['Date'] = df['Date'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))

    for i in range(2001, 2016):
        tmp = df[df.Date >= datetime.datetime(i, 1, 1)]
        tmp = tmp[tmp.Date < datetime.datetime(i + 1, 1, 1)]

        days[str(i)] = max(tmp.shape[0], days[str(i)])
