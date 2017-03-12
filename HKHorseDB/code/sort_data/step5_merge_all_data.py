#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step5_merge_all_data
# @Date: 2017-03-12
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os
import datetime

import pandas as pd

from ..constant import Constant as const
from step4_sort_and_check_data_correctness import convert_finish_time


def get_merged_race_detail_file(race_type):
    df_list = []
    data_path = os.path.join(const.RACE_DATA_PATH, 'race_in_{}'.format(race_type.lower()))
    for file_name in os.listdir(data_path):
        if not file_name.endswith('.xlsx'):
            continue
        tmp_df = pd.read_excel(os.path.join(data_path, file_name))
        tmp_df[const.FINISH_TIME] = tmp_df[const.FINISH_TIME].apply(convert_finish_time)
        tmp_df[const.ID] = file_name.split('.')[0]
        df_list.append(tmp_df)

    merged_race_detail_df = pd.concat(df_list, axis=0, ignore_index=True).reset_index(drop=True)
    return merged_race_detail_df


merged_dfs = []
for race_type in ['st', 'hv']:
    race_df = pd.read_pickle(os.path.join(const.RACE_DATA_PATH, '20170311_race_in_{}.p'.format(race_type.upper())))

    new_race_df = pd.DataFrame(index=race_df.index)
    for key in race_df.keys():
        if key == 'ID':
            new_race_df[key] = race_df[key]
        else:
            new_race_df['{}{}'.format(const.RACE, key)] = race_df[key]

    race_detail_df = get_merged_race_detail_file(race_type)

    race_detail_merged = pd.merge(race_detail_df, new_race_df, how='outer', on='ID')

    race_detail_merged.to_pickle(os.path.join(const.MERGED_TEMP_PATH, '20170313_race_race_detail_df.p'))
    merged_dfs.append(race_detail_merged)

df = pd.concat(merged_dfs, ignore_index=True, axis=0).reset_index(drop=True)

df[const.DATE] = df['{}{}'.format(const.RACE, const.DATE)].apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d'))
df[const.YEAR] = df[const.DATE].apply(lambda x: x.year)
df[const.MONTH] = df[const.DATE].apply(lambda x: x.month)
df[const.DAY] = df[const.DATE].apply(lambda x: x.day)

df.to_pickle(os.path.join(const.MERGED_TEMP_PATH, '20170312_merged_race_race_detail.p'))
df.to_excel(os.path.join(const.MERGED_RESULT_PATH, '20170312_merged_race_race_detail.xlsx'), index=False)
df.to_csv(os.path.join(const.MERGED_RESULT_PATH, '20170312_merged_race_race_detail.csv'), index=False)

# merge horse data to race data
horse_data = pd.read_pickle(os.path.join(const.HORSE_DATA_PATH, '20170307_horse_info_format_key.p'))
race_detail_merged = pd.read_pickle(os.path.join(const.MERGED_TEMP_PATH, '20170312_merged_race_race_detail.p'))

df = pd.merge(race_detail_merged, horse_data, how='left', on='{}{}'.format(const.HORSE, const.CODE))
df.to_pickle(os.path.join(const.MERGED_TEMP_PATH, '20170312_merged_race_horse_data.p'))
df.to_excel(os.path.join(const.MERGED_RESULT_PATH, '20170312_merged_race_horse_data.xlsx'), index=False)
df.to_csv(os.path.join(const.MERGED_RESULT_PATH, '20170312_merged_race_horse_data.csv'), index=False, encoding='utf8')

# The following code are used to merge jockey info:
horse_race_df = pd.read_pickle(os.path.join(const.MERGED_TEMP_PATH, '20170312_merged_race_horse_data.p'))
jockey_data = pd.read_pickle(os.path.join(const.JOCKEY_DATA_PATH, '20170312_jockey_info_drop_season_bg_info.p'))

df = pd.merge(horse_race_df, jockey_data, how='left', on='{}{}'.format(const.JOCKEY, const.CODE))
df.to_pickle(os.path.join(const.MERGED_TEMP_PATH, '20170312_merged_race_horse_jockey_data.p'))
df.to_excel(os.path.join(const.MERGED_RESULT_PATH, '20170312_merged_race_horse_jockey_data.xlsx'), index=False)
df.to_csv(os.path.join(const.MERGED_RESULT_PATH, '20170312_merged_race_horse_jockey_data.csv'), index=False,
          encoding='utf8')

# find last race info of horse data
race_horse_jockey_df = pd.read_pickle(os.path.join(const.MERGED_TEMP_PATH, '20170312_merged_race_horse_jockey_data.p'))
race_horse_jockey_df['RaceIndex'] = race_horse_jockey_df['RaceIndex'].apply(int)
race_horse_jockey_df = race_horse_jockey_df.sort_values([const.DATE, 'RaceIndex'], ascending=False)

race_horse_jockey_df.to_pickle(os.path.join(const.MERGED_TEMP_PATH, '20170312_merged_race_horse_jockey_data_sorted.p'))
horse_group = race_horse_jockey_df.groupby('{}{}'.format(const.HORSE, const.CODE))


def get_last_race_data(group_key):
    tmp_df = horse_group.get_group(group_key)
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
        column_dict[key] = '{}{}{}'.format(const.HORSE, const.LAST_RACE, key)

    result_df = result_df.rename(index=str, columns=column_dict)

    return result_df


last_race_dfs = map(get_last_race_data, horse_group.groups.keys())
last_race_df = pd.concat(last_race_dfs, axis=0)
last_race_df['index'] = last_race_df.index
last_race_df['index'] = last_race_df['index'].apply(int)
last_race_df = last_race_df.set_index('index')

all_info_merged_add_last_race = pd.merge(race_horse_jockey_df,
                                         last_race_df, how='left',
                                         left_index=True, right_index=True)

all_info_merged_add_last_race.to_pickle(
    os.path.join(const.MERGED_TEMP_PATH, '201703012_race_horse_jockey_add_last_horse_race.p'))
all_info_merged_add_last_race.to_csv(
    os.path.join(const.MERGED_RESULT_PATH, '20170312_race_horse_jockey_add_last_horse_race.csv'),
    index=False, encoding='utf8')
all_info_merged_add_last_race.to_excel(
    os.path.join(const.MERGED_RESULT_PATH, '20170312_race_horse_jockey_add_last_horse_race.xlsx'),
    index=False)

# add last top n data
merged_last_df = all_info_merged_add_last_race
for last_info in [const.LAST_NO_ONE, const.LAST_NO_TWO, const.LAST_NO_THREE, const.LAST_TOP_THREE]:

    # the following code use to get last win data
    def get_last_race_data(group_key):
        tmp_df = horse_group.get_group(group_key)
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
            column_dict[key] = '{}{}{}'.format(const.HORSE, last_info, key)

        result_df = result_df.rename(index=str, columns=column_dict)

        return result_df


    last_dfs = map(get_last_race_data, horse_group.groups.keys())
    last_df = pd.concat(last_dfs, axis=0)
    last_df['index'] = last_df.index
    last_df['index'] = last_df['index'].apply(int)
    last_df = last_df.set_index('index')

    merged_last_df = pd.merge(merged_last_df,
                              last_df, how='left',
                              left_index=True, right_index=True)

    merged_last_df.to_pickle(
        os.path.join(const.MERGED_TEMP_PATH, '20170312_merged_horse_{}.p'.format(last_info)))
    merged_last_df.to_csv(
        os.path.join(const.MERGED_RESULT_PATH, '20170312_merged_horse_{}.csv'.format(last_info)),
        index=False, encoding='utf8')
