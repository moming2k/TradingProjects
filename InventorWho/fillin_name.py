#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: fillin_name
# Author: warn
# Date: warn

import os

import pandas as pd

root_path = '/home/wangzg/Documents/WangYouan/research/InventorWho'

data_path = os.path.join(root_path, 'data')
tmp_path  = os.path.join(root_path, 'temp')
google_data_path = os.path.join(root_path, 'GooglePatentData')
samput_data_path = os.path.join(root_path, 'SampatData')
result_path = os.path.join(root_path, 'result')

origin_df = pd.read_pickle(os.path.join(tmp_path, 'inventor_info.p'))

raw_inventor_info = pd.read_sas(os.path.join(data_path, 'grant_rawinventor.sas7bdat')).drop(
    ['uuid', 'sequence'], axis=1).dropna(subset=['name_first']).drop_duplicates('inventor_id')

origin_df['name_first'] = raw_inventor_info[u'name_first'].fillna(origin_df['name_first'])
origin_df['name_last'] = raw_inventor_info[u'name_last'].fillna(origin_df['name_last'])

origin_df.to_pickle(tmp_path, 'inventor_info_fullname.p')
df_10 = origin_df[origin_df.patent_num > 10]
df_5 = origin_df[origin_df.patent_num > 5]

df_10.to_pickle(os.path.join(tmp_path, 'inventor_p_10_fc_10_new.p'))
df_5.to_pickle(os.path.join(tmp_path, 'inventor_p_5_fc_10_new.p'))

df_10.to_csv(os.path.join(result_path, 'inventor_p_10_fc_10.csv'))
df_5.to_csv(os.path.join(result_path, 'inventor_p_5_fc_10.csv'))
