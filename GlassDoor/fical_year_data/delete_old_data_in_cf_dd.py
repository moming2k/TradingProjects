#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: delete_old_data_in_cf_dd
# Author: Mark Wang
# Date: 5/11/2016


import os
import datetime

import numpy as np
import pandas as pd

path = '/home/wangzg/Documents/WangYouan/research/Glassdoor'
input_path = 'input_data'
output_path = 'output'
result_path = 'result'
data_path = '20161025merge_data'

df = pd.read_csv(os.path.join(path, result_path, 'glassdoor_indicators_addPolMag.csv'),
                 dtype={'FK_employerId': str, 'FK_dateId': str, 'commentYear': str})

date_index = df['FK_dateId'].apply(lambda x: datetime.datetime.strptime(x, '%Y%m%d'))
oldest_date = date_index.min()

# handle cf data delete date too old
cf = pd.read_csv(os.path.join(path, data_path, 'accrual_cf_control.csv'),
                 dtype={'gvkey': str, 'fyear': str, 'datadate': str, 'gvkey1': str})

cf = cf.dropna(subset=['datadate'])

cf_date = cf['datadate'].apply(lambda x: datetime.datetime.strptime(x, '%Y%m%d'))
cf = cf[cf_date >= oldest_date]
cf.to_csv(os.path.join(path, output_path, 'cf_drop_old.csv'), index=False, encoding='utf8')

# handle dd data delete date too old
dd = pd.read_csv(os.path.join(path, data_path, 'dd_quality_control.csv'),
                 dtype={'gvkey': str, 'fyear': str, 'datadate': str, 'gvkey1': str})
dd = dd.dropna(subset=['datadate'])
dd_date = dd['datadate'].apply(lambda x: datetime.datetime.strptime(x, '%Y%m%d'))
dd = dd[dd_date >= oldest_date]
dd.to_csv(os.path.join(path, output_path, 'dd_drop_old.csv'), index=False, encoding='utf8')

# merge dd and cf together
df = cf.merge(dd, how='outer', on=['fyear', 'tic', 'datadate'], suffixes=['', '_y'])

keys = df.keys()
for key in keys:
    if key.endswith('_y') or '{}_y'.format(key) not in keys:
        continue

    df[key] = df[key].fillna(df['{}_y'.format(key)])
    del df['{}_y'.format(key)]

df['gvkey'] = df['gvkey'].apply(lambda x: str(int(x)))

# add glassdoor id
glassdoor_id_df = pd.read_csv(os.path.join(path, data_path, 'gvkey_glassdoorID', 'glassdoor_id_gvkey.csv'),
                              dtype={'GDID': str, 'GVKEY': str})


def get_gdid(gvkey):
    tmp = glassdoor_id_df[glassdoor_id_df['GVKEN'] == gvkey]
    if tmp.empty:
        return np.nan
    else:
        return tmp['GDID'].tolist()[0]


df['gdid'] = df['gvkey'].apply(get_gdid)
df.to_csv(os.path.join(path, output_path, 'cf_dd_merged.csv'), index=False, encoding='utf8')
