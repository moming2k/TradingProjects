#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: fill_in_missing_info_to_forward_citation
# Author: warn
# Date: warn

import os
import datetime

import pandas as pd
import numpy as np

today_str = datetime.datetime.today().strftime('%Y%m%d')
root_path = '/home/wangzg/Documents/WangYouan/research/InventorWho'
temp_path = os.path.join(root_path, 'temp')
today_temp_path = os.path.join(temp_path, today_str)
if not os.path.isdir(today_temp_path):
    os.makedirs(today_temp_path)
result_path = os.path.join(root_path, 'result')
data_path = os.path.join(root_path, 'data')
file_path = '/home/wangzg/Documents/WangYouan/research/InventorWho/temp/20161211/fill_names.p'
df = pd.read_pickle(file_path)

merged_join_df = pd.read_pickle(os.path.join(temp_path, 'merged_join.p'))
merged_join_df = merged_join_df.sort_values('year')
merged_join_groups = merged_join_df.groupby('inventor_id')


def get_required_information(row):
    try:
        df_info = merged_join_groups.get_group(row['inventor_id'])
        state_list = df_info.state.tolist()
        city_list = df_info.city.tolist()
        permno_list = df_info.permno.tolist()
        patent_id_list = df_info.patent_id.tolist()
        return pd.Series({'first_state': state_list[0], 'last_state': state_list[-1], 'first_city': city_list[0],
                          'last_city': city_list[-1], 'first_permno': permno_list[0], 'last_permno': permno_list[-1],
                          'first_patent_id': patent_id_list[0], 'last_patent_id': patent_id_list[-1]})
    except Exception:

        return pd.Series({'first_state': None, 'last_state': None, 'first_city': None,
                          'last_city': None, 'first_permno': None, 'last_permno': None,
                          'first_patent_id': None, 'last_patent_id': None})


df['first_state'], df['last_state'], df['first_patent_id'], df['last_patent_id'], \
df['first_city'], df['last_city'], df['first_permno'], df['last_permno'], = df.apply(get_required_information,
                                                                                     axis=1)

df.to_pickle(os.path.join(today_temp_path, 'add_missing_info.p'))
