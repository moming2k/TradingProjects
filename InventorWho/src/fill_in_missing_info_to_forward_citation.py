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
first_info = merged_join_df.drop_duplicates(subset='inventor_id', keep='first').set_index('inventor_id')
last_info = merged_join_df.drop_duplicates(subset='inventor_id', keep='last').set_index('inventor_id')

merged_join_groups = merged_join_df.groupby('inventor_id')
# own_report_df.loc[:, 'inventor_id'] = own_report_df.index
last_info.drop(['name_first', 'name_last', 'street', 'zipcode', 'country'], axis=1, inplace=True)
first_info.drop(['name_first', 'name_last', 'street', 'zipcode', 'country'], axis=1, inplace=True)

df_merge_first = df.merge(first_info, left_index=True, right_index=True, how='left', suffixes=['', '_first'])

df_merge_first_last = df_merge_first.merge(last_info, left_index=True, right_index=True, how='left',
                                           suffixes=['', '_last'])
df_merge_first_last['year_first'] = df_merge_first_last['year']
df_merge_first_last['state_first'] = df_merge_first_last['state']
df_merge_first_last['city_first'] = df_merge_first_last['city']
df_merge_first_last['forwardCitationCount_first'] = df_merge_first_last['forwardCitationCountToSampleEnd']
df_merge_first_last['permno_first'] = df_merge_first_last['permno']

result_df = df_merge_first_last.drop(
    ['year', 'state', 'city', 'forwardCitationCountToSampleEnd', 'permno', u'patent_id',
     u'first_city', u'last_city', u'first_patent_year'], axis=1)


def float2str(str_info):
    try:
        return str(int(str_info))
    except Exception:
        return str_info

result_df['year_first'] = result_df['year_first'].apply(float2str)
result_df['permno_last'] = result_df['permno_last'].apply(float2str)
result_df['year_last'] = result_df['year_last'].apply(float2str)
result_df['permno_first'] = result_df['permno_first'].apply(float2str)

result_df.to_pickle(os.path.join(today_temp_path, 'add_missing_info.p'))

greater_than_100 = result_df[result_df.patent_num > 100]
greater_than_100.to_csv(os.path.join(result_path, 'statistics_inventor_greater_than_100.csv'))