#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: get_avg_polmag
# Author: Mark Wang
# Date: 17/11/2016


import pandas as pd

df = pd.read_csv('/home/wangzg/Documents/WangYouan/research/Glassdoor/result/glassdoor_communication_indicators.csv')

mean_result = {}
has_mean_result = {}
num_dict = {}

for key in df.keys():
    if not (key.endswith('Pol') or key.endswith('Mag')):
        continue

    mean_result[key] = df[key].mean()
    num_dict[key] = df[key].count()
    has_mean_result[key] = df[key].sum() / float(num_dict[key])
