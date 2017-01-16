#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step1_keep_useful_data
# @Date: 2017-01-16
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime

import pandas as pd

from path_info import *

for file_name in os.listdir(original_return_data):
    if not file_name.endswith('csv'):
        continue
    df = pd.read_csv(os.path.join(original_return_data, file_name))
    df['datetime'] = df['datetime'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    df = df[df['datetime'] >= datetime.datetime(1984, 1, 1)]
    df = df[df['datetime'] <= datetime.datetime(2015, 12, 31)]
    df.to_pickle(os.path.join(return_data_path, '{}.p'.format(file_name[:-4])))
