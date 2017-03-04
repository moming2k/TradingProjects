#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step1_sort_race_data
# @Date: 2017-03-04
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import re

import pandas as pd

root_path = '/home/wangzg/Documents/WangYouan/Trading/HKHorse'
data_path = os.path.join(root_path, 'data')
race_info_path = os.path.join(data_path, 'race_data')
temp_path = os.path.join(root_path, 'temp')
race_tmp_path = os.path.join(temp_path, 'race_data')
if not os.path.isdir(race_tmp_path):
    os.makedirs(race_tmp_path)

df_st = pd.read_excel(os.path.join(race_info_path, '20170211_race_ST.xlsx'))
df_hv = pd.read_excel(os.path.join(race_info_path, '20170208_race_HV.xlsx'))

race_df = pd.concat([df_hv, df_st], axis=0, ignore_index=True).reset_index(drop=True)
race_df['Distance'] = race_df['Distance'].dropna().apply(lambda x: re.findall(r'\w+', x)[0])


def get_count_df(input_df, col_name):
    count = input_df[col_name].value_counts()
    sum_value = count.sum()
    count_df = pd.DataFrame(index=count.index)
    count_df['count'] = count
    count_df['percentage'] = count.apply(float) / sum_value
    return count_df

for key in ['Track', 'Course', 'Distance', 'Going', 'Class', 'Name']:
    result_df = get_count_df(input_df=race_df, col_name=key)
    result_df.to_pickle(os.path.join(race_tmp_path, '{}.p'.format(key)))
    result_df.to_csv(os.path.join(race_tmp_path, '{}.csv'.format(key)))

df_list = []

for suffix in ['hv', 'st']:
    path = os.path.join(race_info_path, 'race_in_{}'.format(suffix))
    files = os.listdir(path)

    for file_name in files:
        try:
            tmp_df = pd.read_excel(os.path.join(path, file_name))
            tmp_df.loc[:, 'ID'] = file_name.split('.')[0]
            df_list.append(tmp_df)
        except Exception, err:
            print file_name
            raise Exception(err)

merged_df = pd.concat(df_list, axis=0, ignore_index=True).reset_index(drop=True)

for key in [u'HorseCode', u'JockeyCode', u'TrianerCode']:
    result_df = get_count_df(input_df=merged_df, col_name=key)
    result_df.to_pickle(os.path.join(race_tmp_path, '{}.p'.format(key)))
    result_df.to_csv(os.path.join(race_tmp_path, '{}.csv'.format(key)))