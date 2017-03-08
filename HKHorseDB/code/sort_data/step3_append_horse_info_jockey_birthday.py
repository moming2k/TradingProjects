#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step3_append_horse_info_jockey_birthday
# @Date: 2017-03-07
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd

from ..constant import Constant as const

horse_df = pd.read_pickle(os.path.join(const.HORSE_DATA_PATH, '20170306_horse_info_add_birthday.p'))
race_df = pd.read_pickle(os.path.join(const.MERGED_DATA_PATH, 'all_race_information.p'))

horse_df['{}{}'.format(const.HORSE, const.CODE)] = horse_df.index

horse_df['{}{}'.format(const.HORSE, const.BIRTHDAY)] = horse_df['Birthday']
horse_df['{}{}'.format(const.HORSE, const.FORMER_NAME)] = horse_df['FormerName']

horse_df = horse_df.drop(['FormerName', 'Birthday', '{}{}{}'.format(const.HORSE, const.ENGLISH, const.NAME)], axis=1)

horse_df.to_pickle(os.path.join(const.HORSE_DATA_PATH, '20170307_horse_info_format_key.p'))

race_add_horse = pd.merge(race_df, horse_df, how='left', on=['{}{}'.format(const.HORSE, const.CODE)])

# some horse info missing, add those info
missed_horse_code = race_add_horse[race_add_horse.HorseDamSire.isnull()].HorseCode.dropna().drop_duplicates()
missed_horse_code.to_pickle(os.path.join(const.HORSE_TEMP_PATH, '20170307_miss_horse_list.p'))

race_add_horse.to_pickle(os.path.join(const.MERGED_TEMP_PATH, '20170307_race_info_add_horse_info.p'))
race_add_horse.to_csv(os.path.join(const.MERGED_RESULT_PATH, '20170307_race_info_add_horse_info.csv'), encoding='utf8',
                      index=False)

jockey_df = pd.read_excel(os.path.join(const.JOCKEY_DATA_PATH, '20170307_jockey_info_add_birthday.xlsx'))

# jockey_df['{}{}'.format(const.JOCKEY, const.CODE)] = jockey_df.index
jockey_df['{}{}'.format(const.JOCKEY, const.NATIONALITY)] = jockey_df[
    '{}{}{}'.format(const.JOCKEY, const.CURRENT_SEASON, const.NATIONALITY)].fillna(
    jockey_df['{}{}{}'.format(const.JOCKEY, const.LAST_SEASON, const.NATIONALITY)])

keys = jockey_df.keys()

for key in keys:
    if const.LAST_SEASON in key or const.CURRENT_SEASON in key:
        del jockey_df[key]

jockey_df.to_pickle(os.path.join(const.JOCKEY_DATA_PATH, '20170307_jockey_info_del_season_info.p'))

race_horse_jockey_df = pd.merge(race_add_horse, jockey_df, how='left', on=['{}{}'.format(const.JOCKEY, const.CODE)])

race_horse_jockey_df.to_pickle(os.path.join(const.MERGED_TEMP_PATH, '20170307_race_horse_jockey_info.p'))
race_horse_jockey_df.to_csv(os.path.join(const.MERGED_DATA_PATH, '20170307_race_horse_jockey_info.csv'),
                            index=False, encoding='utf8')

# The following is written in 20170308
race_horse_jockey_df = pd.read_pickle(os.path.join(const.MERGED_TEMP_PATH, '20170307_race_horse_jockey_info.p'))
race_horse_jockey_df = race_horse_jockey_df.rename(
    index=str, columns={'HorseName': 'HorseEnglishName'}).drop('JockeyName', axis=1)

race_horse_jockey_df[const.DATE] = race_horse_jockey_df[const.ID].apply(
    lambda x: datetime.datetime.strptime(x.split('_')[0], '%Y%m%d'))

race_horse_jockey_df[const.YEAR] = race_horse_jockey_df[const.DATE].apply(lambda x: x.year)
race_horse_jockey_df[const.MONTH] = race_horse_jockey_df[const.DATE].apply(lambda x: x.month)
race_horse_jockey_df[const.DAY] = race_horse_jockey_df[const.DATE].apply(lambda x: x.day)

race_horse_jockey_df = race_horse_jockey_df.sort_values(const.DATE, ascending=False).reset_index(drop=True)
race_horse_jockey_df.to_pickle(os.path.join(const.MERGED_TEMP_PATH, '20170308_race_horse_jockey_info.p'))
race_horse_jockey_df.to_csv(os.path.join(const.MERGED_DATA_PATH, '20170308_race_horse_jockey_info.csv'),
                            index=False, encoding='utf8')

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

    for key in keys:
        result_df = result_df.rename(index=str, columns={key: '{}{}'.format(const.LAST_RACE, key)})

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
    os.path.join(const.MERGED_TEMP_PATH, '20170308_race_horse_jockey_add_last_horse_race.p'))
all_info_merged_add_last_race.to_csv(
    os.path.join(const.MERGED_RESULT_PATH, '20170308_race_horse_jockey_add_last_horse_race.csv'),
    index=False, encoding='utf8')

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

        for key in keys:
            result_df = result_df.rename(index=str, columns={key: '{}{}'.format(last_info, key)})

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
        os.path.join(const.MERGED_TEMP_PATH, '20170308_merged_{}.p'.format(last_info)))
    merged_last_df.to_csv(
        os.path.join(const.MERGED_RESULT_PATH, '20170308_merged_{}.csv'.format(last_info)),
        index=False, encoding='utf8')

# remove maybe not usable data out of merged last df
merged_keys = merged_last_df.keys()
keys_to_remove = []

for key in merged_keys:
    if const.ACHIEVEMENTS in key or const.BACKGROUND in key or const.NOTABLE_WINS in key or const.IJC_RECORD in key:
        keys_to_remove.append(key)

merged_last_df_dropped = merged_last_df.drop(keys_to_remove, axis=1)
merged_last_df_dropped.to_pickle(
    os.path.join(const.MERGED_TEMP_PATH, '20170308_merged_dropped.p'))
merged_last_df_dropped.to_csv(
    os.path.join(const.MERGED_RESULT_PATH, '20170308_merged_dropped.csv'),
    index=False, encoding='utf8')

# remove maybe not usable data out of race_horse_jockey_df
merged_keys = race_horse_jockey_df.keys()
keys_to_remove = []
for key in merged_keys:
    if const.ACHIEVEMENTS in key or const.BACKGROUND in key or const.NOTABLE_WINS in key or const.IJC_RECORD in key:
        keys_to_remove.append(key)

race_horse_jockey_df_dropped = race_horse_jockey_df.drop(keys_to_remove, axis=1)
race_horse_jockey_df_dropped[const.RACE_INDEX] = race_horse_jockey_df_dropped[const.ID].apply(
    lambda x: int(x.split('_')[-1]))
race_horse_jockey_df_dropped = race_horse_jockey_df_dropped.sort_values([const.RACE_INDEX, const.DATE], ascending=False)
race_horse_jockey_df_dropped.to_pickle(
    os.path.join(const.MERGED_TEMP_PATH, '20170308_race_horse_jockey_df_dropped.p'))
race_horse_jockey_df_dropped.to_csv(
    os.path.join(const.MERGED_RESULT_PATH, '20170308_race_horse_jockey_df_dropped.csv'),
    index=False, encoding='utf8')

useful_keys = merged_last_df_dropped.keys()

new_key_dict = {}
for key in useful_keys:

    if key.startswith('Last'):
        new_key_dict[key] = '{}{}'.format(const.HORSE, key)

merged_last_df_dropped_rename = merged_last_df_dropped.rename(index=str, columns=new_key_dict)

# sort_data
merged_last_df_dropped_rename['index'] = merged_last_df_dropped_rename.index
merged_last_df_dropped_rename['index'] = merged_last_df_dropped_rename['index'].apply(int)
merged_last_df_dropped_rename = merged_last_df_dropped_rename.set_index('index')

merged_last_df_dropped_rename.to_pickle(
    os.path.join(const.MERGED_TEMP_PATH, '20170308_merged_dropped_rename.p'))
merged_last_df_dropped_rename.to_csv(
    os.path.join(const.MERGED_RESULT_PATH, '20170308_merged_dropped_rename.csv'),
    index=False, encoding='utf8')

# The following code are used to append jockey data
jockey_group = race_horse_jockey_df_dropped.dropna(
    subset=['{}{}'.format(const.JOCKEY, const.CODE)]).groupby('{}{}'.format(const.JOCKEY, const.CODE))


def get_last_jockey_race_data(group_key):
    tmp_df = jockey_group.get_group(group_key)
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

    for key in keys:
        result_df = result_df.rename(index=str, columns={key: '{}{}{}'.format(const.JOCKEY, const.LAST_RACE, key)})

    return result_df


jockey_last_race_dfs = map(get_last_jockey_race_data, jockey_group.groups.keys())
jockey_last_race_df = pd.concat(jockey_last_race_dfs, axis=0)
jockey_last_race_df['index'] = jockey_last_race_df.index
jockey_last_race_df['index'] = jockey_last_race_df['index'].apply(int)
jockey_last_race_df = jockey_last_race_df.set_index('index')

all_info_merged_add_jockey_last_race = pd.merge(merged_last_df_dropped_rename,
                                                jockey_last_race_df, how='left',
                                                left_index=True, right_index=True)
all_info_merged_add_jockey_last_race.to_pickle(
    os.path.join(const.MERGED_TEMP_PATH, '20170308_race_horse_jockey_df_jockey_last_race.p'))
all_info_merged_add_jockey_last_race.to_csv(
    os.path.join(const.MERGED_RESULT_PATH, '20170308_race_horse_jockey_df_jockey_last_race.csv'),
    index=False, encoding='utf8')

merged_last_df = all_info_merged_add_jockey_last_race
for last_info in [const.LAST_NO_ONE, const.LAST_NO_TWO, const.LAST_NO_THREE, const.LAST_TOP_THREE]:

    # the following code use to get last win data
    def get_last_race_data(group_key):
        tmp_df = jockey_group.get_group(group_key)
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

        for key in keys:
            result_df = result_df.rename(index=str, columns={key: '{}{}{}'.format(const.JOCKEY, last_info, key)})

        return result_df


    last_dfs = map(get_last_race_data, jockey_group.groups.keys())
    last_df = pd.concat(last_dfs, axis=0)
    last_df['index'] = last_df.index
    last_df['index'] = last_df['index'].apply(int)
    last_df = last_df.set_index('index')

    merged_last_df = pd.merge(merged_last_df,
                              last_df, how='left',
                              left_index=True, right_index=True)

    merged_last_df.to_pickle(
        os.path.join(const.MERGED_TEMP_PATH, '20170308_merged_jockey_{}.p'.format(last_info)))
    merged_last_df.to_csv(
        os.path.join(const.MERGED_RESULT_PATH, '20170308_merged_jockey_{}.csv'.format(last_info)),
        index=False, encoding='utf8')
