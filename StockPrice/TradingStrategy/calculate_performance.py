#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: calculate_performance
# Author: Mark Wang
# Date: 25/11/2016

import os

import pandas as pd

root_path = '/home/wangzg/Documents/WangYouan/research/HongKongStock/20161125SimulateResult/data'

df = pd.DataFrame(columns=['sharpe', 'p1', 'p2', 'p3', 'threshold', 'symbol'])
index = 0
for i in os.listdir(root_path):
    if not os.path.isdir(os.path.join(root_path, i)):
        continue
    for j in os.listdir(os.path.join(root_path, i)):
        if not j.endswith('csv') or not j.startswith('p1'):
            continue

        info = j[:-4].split('_')

        p1 = int(info[1])
        p2 = int(info[3])
        p3 = int(info[5])
        th = info[7]
        sharpe = float(info[9])
        df.loc[index] = {'sharpe': sharpe,
                         'p1': p1,
                         'p2': p2,
                         'p3': p3,
                         'threshold': th,
                         'symbol': j}
        index += 1
