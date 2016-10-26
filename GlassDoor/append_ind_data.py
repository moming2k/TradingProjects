#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: append_ind_data
# Author: Mark Wang
# Date: 26/10/2016

import os

import numpy as np
import pandas as pd
import pathos

root_path = '/home/wangzg/Documents/WangYouan/research/Glassdoor'
result_path = 'result'
data_path = '20161025merge_data'
file_name = 'guidance_qtr'

key_info_df = pd.read_csv(os.path.join(root_path, data_path, 'gvkey_glassdoorID', 'glassdoor_id_gvkey.csv'),
                          dtype=str)
firm_df = pd.read_csv(os.path.join(root_path, result_path, 'firm_year_statistics.csv'),
                      dtype={'FK_employerId': str, 'commentYear': str})
firm_key = firm_df.keys()


def get_gdid(gvkey):
    gdid = key_info_df[key_info_df['GVKEY'] == gvkey]
    if gdid.empty:
        try:
            gvkey = str(int(gvkey))
            gdid = key_info_df[key_info_df['GVKEY'] == gvkey]
        except Exception:
            return np.nan

    if gdid.empty:
        return np.nan
    return gdid.ix[gdid.index[0], 'GDID']


def get_firm_info(row):
    gdid = row['gdid']
    year = row['year']
    sub_df = firm_df[firm_df['FK_employerId'] == gdid]
    sub_df = sub_df[sub_df['commentYear'] == year]
    if sub_df.empty:
        result_dict = {}
        for key in firm_key:
            result_dict[key] = np.nan
    else:
        result_dict = sub_df.head(1).transpose().to_dict().values()[0]

    del result_dict['FK_employerId']
    del result_dict['commentYear']
    return pd.Series(result_dict)


def process_df(df):
    return df.apply(get_firm_info, axis=1)


if __name__ == '__main__':
    process_num = 10
    pool = pathos.multiprocessing.ProcessingPool(process_num)
    guidence_df = pd.read_csv(os.path.join(root_path, data_path, '{}.csv'.format(file_name)),
                              dtype={'year': str, 'gvkey': str})

    guidence_df['gdid'] = guidence_df['gvkey'].apply(get_gdid)

    split_dfs = np.array_split(guidence_df, process_num)
    ind_infos = pool.map(process_df, split_dfs)
    ind_info = pd.concat(ind_infos)
    # ind_info = guidence_df.apply(get_firm_info, axis=1)

    result_df = guidence_df.merge(ind_info, how='left', left_index=True, right_index=True)

    result_df.to_csv(os.path.join(root_path, result_path, '{}_ind.csv'.format(file_name)), index=False,
                     encoding='utf8')
