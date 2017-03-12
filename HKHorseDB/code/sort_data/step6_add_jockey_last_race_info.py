#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step6_add_jockey_last_race_info
# @Date: 2017-03-12
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd

from ..constant import Constant as const

race_jockey_horse_merged_df = pd.read_pickle(os.path.join(const.MERGED_TEMP_PATH,
                                                          '20170312_merged_race_horse_jockey_data_sorted.p'))

merged_last_df = pd.read_pickle(
    os.path.join(const.MERGED_TEMP_PATH, '20170312_merged_horse_{}.p'.format(const.LAST_TOP_THREE)))

jockey_groups = race_jockey_horse_merged_df.groupby('{}{}'.format(const.JOCKEY, const.CODE))


def get_last_race_data(group_key):
    tmp_df = jockey_groups.get_group(group_key)
    df_index = tmp_df.index

    result_df = pd.DataFrame(index=df_index, columns=tmp_df.keys())
    days_between = pd.Series()

    for i in range(df_index.size - 1):
        current_race_index = df_index[i]
        last_race_index = df_index[i + 1]
        result_df.loc[current_race_index] = tmp_df.loc[last_race_index]
        current_date = tmp_df.loc[current_race_index, const.DATE]
        last_date = tmp_df.loc[last_race_index, const.DATE]
        days_between.loc[current_race_index] = (current_date - last_date).days

    result_df[const.DAYS_BETWEEN] = days_between

    keys = result_df.keys()

    column_dict = {}
    for key in keys:
        column_dict[key] = '{}{}{}'.format(const.JOCKEY, const.LAST_RACE, key)

    result_df = result_df.rename(index=str, columns=column_dict)

    return result_df


last_race_dfs = map(get_last_race_data, jockey_groups.groups.keys())
last_race_df = pd.concat(last_race_dfs, axis=0)
last_race_df['index'] = last_race_df.index
last_race_df['index'] = last_race_df['index'].apply(int)
last_race_df = last_race_df.set_index('index')

all_info_merged_add_last_race = pd.merge(merged_last_df,
                                         last_race_df, how='left',
                                         left_index=True, right_index=True)

all_info_merged_add_last_race.to_pickle(
    os.path.join(const.MERGED_TEMP_PATH, '201703012_race_horse_jockey_add_last_race_jockey.p'))
all_info_merged_add_last_race.to_csv(
    os.path.join(const.MERGED_RESULT_PATH, '201703012_race_horse_jockey_add_last_race_jockey.csv'),
    index=False, encoding='utf8')
all_info_merged_add_last_race.to_excel(
    os.path.join(const.MERGED_RESULT_PATH, '201703012_race_horse_jockey_add_last_race_jockey.xlsx'),
    index=False)

# add last top n data
merged_last_df = all_info_merged_add_last_race
for last_info in [const.LAST_NO_ONE, const.LAST_NO_TWO, const.LAST_NO_THREE, const.LAST_TOP_THREE]:

    # the following code use to get last win data
    def get_last_race_data(group_key):
        tmp_df = jockey_groups.get_group(group_key)
        df_index = tmp_df.index

        result_df = pd.DataFrame(index=df_index, columns=tmp_df.keys())
        if last_info == const.LAST_NO_ONE:
            number_df = tmp_df[tmp_df[const.PLACE] == 1]
        elif last_info == const.LAST_NO_TWO:
            number_df = tmp_df[tmp_df[const.PLACE] == 2]
        elif last_info == const.LAST_NO_THREE:
            number_df = tmp_df[tmp_df[const.PLACE] == 3]
        else:
            number_df = tmp_df[tmp_df[const.PLACE] <= 3]
        days_between = pd.Series()

        for index in df_index:
            current_date = tmp_df.loc[index, const.DATE]
            number_df = number_df[number_df[const.DATE] < current_date]
            if number_df.empty:
                break

            last_date = number_df.loc[number_df.first_valid_index(), const.DATE]
            days_between.loc[index] = (current_date - last_date).days
            result_df.loc[index] = number_df.loc[number_df.first_valid_index()]

        result_df[const.DAYS_BETWEEN] = days_between
        keys = result_df.keys()

        column_dict = {}
        for key in keys:
            column_dict[key] = '{}{}{}'.format(const.JOCKEY, last_info, key)

        result_df = result_df.rename(index=str, columns=column_dict)

        return result_df


    last_dfs = map(get_last_race_data, jockey_groups.groups.keys())
    last_df = pd.concat(last_dfs, axis=0)
    last_df['index'] = last_df.index
    last_df['index'] = last_df['index'].apply(int)
    last_df = last_df.set_index('index')

    merged_last_df = pd.merge(merged_last_df,
                              last_df, how='left',
                              left_index=True, right_index=True)

    merged_last_df.to_pickle(
        os.path.join(const.MERGED_TEMP_PATH, '20170312_merged_jockey_{}.p'.format(last_info)))
    merged_last_df.to_csv(
        os.path.join(const.MERGED_RESULT_PATH, '20170312_merged_jockey_{}.csv'.format(last_info)),
        index=False, encoding='utf8')
