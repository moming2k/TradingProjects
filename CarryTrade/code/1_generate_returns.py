#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: 1_generate_returns
# @Date: 2016-12-24
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os
import datetime

import pandas as pd
import numpy as np

# define some parameters
today_str = datetime.datetime.today().strftime('%Y%m%d')
root_path = '/home/wangzg/Documents/WangYouan/research/CarryTrade'
curr_data_path = os.path.join(root_path, 'CurrData')
temp_path = os.path.join(root_path, 'temp')
today_temp_path = os.path.join(temp_path, today_str)

if not os.path.isdir(today_temp_path):
    os.makedirs(today_temp_path)

# this is used to generate new list
review_month_list = pd.Series([1, 2, 3, 4, 6, 12, 18, 24])
memory_month_list = pd.Series([1, 2, 3, 4, 6, 12, 18, 24])


def generate_return_table(return_df, cumprod_df, new_key_list):
    for key in new_key_list:
        key_info = key.split('_')
        review = int(key_info[1])
        memory = int(key_info[-1])


# start to generate learning returns
for data_file in os.listdir(curr_data_path):
    if not data_file.startswith('20160919') or not data_file.endswith('csv'):
        continue

    df = pd.read_csv(os.path.join(curr_data_path, data_file))
    df['datetime'] = df.datetime.apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    df = df.set_index('datetime', drop=True)

    # decide how many months are in this file
    if '12m' in data_file:
        month_num = 12

    elif '6m' in data_file:
        month_num = 6

    elif '3m' in data_file:
        month_num = 3

    else:
        month_num = 1
    current_review_list = review_month_list[(review_month_list % month_num) == 0]
    current_memory_list = memory_month_list[(memory_month_list % month_num) == 0]

    # generate new column name
    new_col_list = []
    for m in current_memory_list:
        for r in current_review_list:
            new_col_list.append('review_{}_memory_{}'.format(r, m))

    cumprod_df = (df + 1).cumprod()

    new_df = generate_return_table(df, cumprod_df, new_col_list)
    new_df.to_pickle(os.path.join(today_temp_path, '{}_add_learning.p'.format(data_file[:-4])))
