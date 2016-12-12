#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: get_inventor_greater_than_certain_variable
# @Date: 2016-12-11
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd

today_str = datetime.datetime.today().strftime('%Y%m%d')

root_path = '/home/wangzg/Documents/WangYouan/research/InventorWho'
temp_path = os.path.join(root_path, 'temp')
today_temp_path = os.path.join(temp_path, today_str)
if not os.path.isdir(today_temp_path):
    os.makedirs(today_temp_path)
result_path = os.path.join(root_path, 'result')
data_path = os.path.join(root_path, 'data')

forward_ciation_df = pd.read_pickle(os.path.join(temp_path, 'forward_citation.p'))

raw_inventor_info = pd.read_sas(os.path.join(data_path, 'grant_rawinventor.sas7bdat')).drop(
    ['uuid', 'sequence'], axis=1).dropna(subset=['name_first']).drop_duplicates('inventor_id').set_index(
    'inventor_id'
)

merged_df = forward_ciation_df.merge(raw_inventor_info, left_index=True, right_index=True, how='left',
                                     suffixes=['', '_r'])

keys = merged_df.keys()

for key in keys:
    if key.endswith('_r') or '{}_r'.format(key) not in keys:
        continue

    merged_df['{}'.format(key)] = merged_df['{}_r'.format(key)].fillna(merged_df[key])
    del merged_df['{}_r'.format(key)]

merged_df.to_pickle(os.path.join(today_temp_path, 'fill_names.p'))
