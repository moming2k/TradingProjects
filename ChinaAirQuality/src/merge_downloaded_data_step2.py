#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: merge_downloaded_data_step2
# @Date: 2017-01-03
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

root_path = '/home/wangzg/Documents/WangYouan/research/ChinaAirQuality'

data_path = os.path.join(root_path, 'data')
output_path = os.path.join(root_path, 'result')

df_list = []

for file_name in os.listdir(data_path):
    if file_name.endswith('csv'):
        continue

    df_list.append(pd.read_pickle(os.path.join(data_path, file_name)))

df = pd.concat(df_list, axis=0, ignore_index=True)

df.to_pickle(os.path.join(output_path, 'ChinaAirQuality20140101_20161231.p'))
df.to_csv(os.path.join(output_path, 'ChinaAirQuality20140101_20161231.csv'), encoding='utf8')
