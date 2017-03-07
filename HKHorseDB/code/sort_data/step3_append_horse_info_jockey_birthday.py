#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step3_append_horse_info_jockey_birthday
# @Date: 2017-03-07
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

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
