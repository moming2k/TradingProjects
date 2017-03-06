#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step2_merge_race_data_to_every_race_data
# @Date: 2017-03-05
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd
import numpy as np

from ..constant import Constant as const

race_detail_df = pd.read_pickle(os.path.join(const.RACE_TEMP_PATH, 'all_race_information.p'))

df_st = pd.read_excel(os.path.join(const.RACE_DATA_PATH, '20170211_race_ST.xlsx'))
df_hv = pd.read_excel(os.path.join(const.RACE_DATA_PATH, '20170208_race_HV.xlsx'))

race_df = pd.concat([df_hv, df_st], axis=0, ignore_index=True).reset_index(drop=True)

race_df[const.DATE] = race_df[const.DATE].apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d'))
race_df[const.SEASON_INDEX] = race_df[const.SEASON_INDEX].apply(lambda x: '' if np.isnan(x) else str(int(x)))

new_race_df = pd.DataFrame(index=race_df.index)

for key in race_df.keys():
    if key in {const.ID, const.DATE}:
        new_key = key

    else:
        new_key = '{}{}'.format(const.RACE, key)

    new_race_df[new_key] = race_df[key]

new_race_df.to_pickle(os.path.join(const.MERGED_TEMP_PATH, 'sorted_race_df.p'))

race_df = pd.merge(race_detail_df, new_race_df, how='left', on=const.ID)

race_df[const.YEAR] = race_df[const.DATE].apply(lambda x: str(x.year))
race_df[const.MONTH] = race_df[const.DATE].apply(lambda x: str(x.month))
race_df[const.DAY] = race_df[const.DATE].apply(lambda x: str(x.day))

race_df.to_pickle(os.path.join(const.MERGED_TEMP_PATH, 'race_detailed_merged_data.p'))
race_df.to_csv(os.path.join(const.MERGED_RESULT_PATH, 'race_detailed_merged_data.csv'), index=False)
