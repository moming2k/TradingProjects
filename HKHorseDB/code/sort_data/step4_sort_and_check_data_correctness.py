#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step4_sort_and_check_data_correctness
# @Date: 2017-03-11
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os
import datetime

import pandas as pd

from ..constant import Constant as const


def convert_finish_time(time_str):
    try:
        dot_count = time_str.count('.')
        if dot_count == 1:
            return float(dot_count)

        elif dot_count == 2:
            time_split = time_str.split('.')
            return 60 * int(time_split[0]) + float('.'.join(time_split[1:]))

        return time_str
    except Exception:
        return time_str


def merge_race_and_detail_data(race_type):
    data_path = os.path.join(const.RACE_DATA_PATH, 'race_in_{}'.format(race_type.lower()))
    if race_type.lower() == 'st':
        race_df = pd.read_excel(os.path.join(const.RACE_DATA_PATH, '20170211_race_ST.xlsx'))
    elif race_type.lower() == 'hv':
        race_df = pd.read_excel(os.path.join(const.RACE_DATA_PATH, '20170208_race_HV.xlsx'))
    else:
        return None

    df_list = []
    race_df['Date'] = race_df['Date'].apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d'))

    for file_name in os.listdir(data_path):
        if not file_name.endswith('.xlsx'):
            continue
        tmp_df = pd.read_excel(os.path.join(data_path, file_name))
        tmp_df[const.FINISH_TIME] = tmp_df[const.FINISH_TIME].apply(convert_finish_time)
        tmp_result_df = pd.DataFrame(index=tmp_df.index, columns=tmp_df.columns)
        for col in tmp_df.columns:
            tmp_result_df['{}{}'.format(const.RACE, col)] = tmp_df[col]

        tmp_result_df[const.ID] = file_name.split('.')[0]
        df_list.append(tmp_result_df)

    merged_race_detail_df = pd.concat(df_list, axis=0, ignore_index=True).reset_index(drop=True)
