#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step1_sort_data
# @Date: 2017-02-14
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import re
import datetime

import pandas as pd
import numpy as np
from stdnum import cusip

from path_info import compustat_data_path, crsp_data_path, year_data_path, temp_path, result_path
from constants import Constant as const

today_str = datetime.datetime.today().strftime('%Y%m%d')

# Sort crsp data file
crsp_df = pd.read_excel(crsp_data_path)[[const.CRSP_CUSIP, const.CRSP_SIC]]
crsp_df[const.CRSP_CUSIP] = crsp_df[const.CRSP_CUSIP].apply(lambda x: '{}{}'.format(x, cusip.calc_check_digit(x)))
crsp_df.drop_duplicates('CUSIP').set_index('CUSIP', drop=True).to_pickle(os.path.join(temp_path, 'sorted_crsp_data.p'))

# Sort compustat data file
compustat_df = pd.read_csv(compustat_data_path)
compustat_df[const.COMPUSTAT_CUSIP] = compustat_df[const.COMPUSTAT_CUSIP].apply(
    lambda x: x if not x.isdigit() else '{:09d}'.format(int(x)))
compustat_df.set_index(const.COMPUSTAT_CUSIP, drop=True).to_pickle(os.path.join(temp_path, 'sorted_compustat_data.p'))

# Create some useful temp path
cusip_temp_save_path = os.path.join(temp_path, 'cusip_polution_data')
sic_temp_save_path = os.path.join(temp_path, 'sic_polution_data')
year_cusip_result_path = os.path.join(result_path, 'year_cusip_result')
year_sic_result_path = os.path.join(result_path, 'year_sic_result')

for dir_path in [cusip_temp_save_path, year_cusip_result_path, year_sic_result_path, sic_temp_save_path]:
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)


def find_sic(cusip):
    """ First find cusip info in CRSP data then COMPUSTAT. If both doesn't find, return None """
    if cusip in crsp_df.index:
        return crsp_df.ix[cusip, const.CRSP_SIC]

    elif cusip in compustat_df.index:
        return compustat_df.ix[cusip, const.COMPUSTAT_SIC]

    else:
        return np.nan


# generate sic file and cusip file
data_file_list = os.listdir(year_data_path)
for file_name in data_file_list:
    save_name = '{}_{}'.format(today_str, '_'.join(file_name[:-4].split('_')[1:]))
    data_df = pd.read_csv(os.path.join(year_data_path, file_name))
    data_df[const.DATA_CUSIP] = data_df[const.DATA_CUSIP].apply(
        lambda x: x if not x.isdigit() else '{:09d}'.format(int(x)))
    data_df[const.DATA_SIC] = data_df[const.DATA_CUSIP].apply(find_sic)

    data_df.to_pickle(os.path.join(cusip_temp_save_path, '{}.p'.format(save_name)))
    data_df.to_csv(os.path.join(year_cusip_result_path, '{}.csv'.format(save_name)), index=False)

    sic_df = data_df.drop(const.DATA_CUSIP, axis=1).groupby('sic').sum()
    sic_df.to_pickle(os.path.join(sic_temp_save_path, '{}.p'.format(save_name)))
    sic_df.to_csv(os.path.join(year_sic_result_path, '{}.csv'.format(save_name)))

# merge cusip data
cusip_file_list = os.listdir(cusip_temp_save_path)
df_list = []

for file_name in cusip_file_list:
    data_df = pd.read_pickle(os.path.join(cusip_temp_save_path, file_name))
    year = int(re.findall(r'\d+', file_name)[1])
    data_df.loc[:, const.DATA_YEAR] = year
    df_list.append(data_df)

merged_df = pd.concat(df_list, axis=0, ignore_index=True)

merged_df.to_pickle(os.path.join(temp_path, 'year_cusip_data.p'))
merged_df.to_csv(os.path.join(result_path, '{}_year_cusip_data.csv'.format(today_str)))

# merge sic data
sic_file_list = os.listdir(sic_temp_save_path)
df_list = []

for file_name in sic_file_list:
    data_df = pd.read_pickle(os.path.join(sic_temp_save_path, file_name))
    data_df[const.DATA_SIC] = data_df.index
    year = int(re.findall(r'\d+', file_name)[1])
    data_df.loc[:, const.DATA_YEAR] = year
    df_list.append(data_df)

merged_df = pd.concat(df_list, axis=0, ignore_index=True)

merged_df.to_pickle(os.path.join(temp_path, 'year_sic_data.p'))
merged_df.to_csv(os.path.join(result_path, '{}_year_sic_data.csv'.format(today_str)))
