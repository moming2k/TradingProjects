#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: get_avg_polmag
# Author: Mark Wang
# Date: 17/11/2016


import pandas as pd

# use to get average of every information
df = pd.read_csv('/home/wangzg/Documents/WangYouan/research/Glassdoor/result/glassdoor_communication_indicators.csv')

mean_result = {}
has_mean_result = {}
num_dict = {}

for key in df.keys():
    if not (key.endswith('Pol') or key.endswith('Mag')):
        continue

    mean_result[key] = df[key].mean()
    num_dict[key] = df[key].count()
    has_mean_result[key] = df[key].sum() / float(num_dict[key])

import pathos
import numpy as np

process_num = 12
df = pd.read_stata('/home/wangzg/Documents/WangYouan/research/Glassdoor/result/cf_dd_merged_ind.pta')

groupd = df.groupby('gvkey')
keys = groupd.groups.keys()

split_keys = np.array_split(keys, process_num)

pool = pathos.multiprocessing.ProcessingPool(process_num)


def process_df(key):
    tmp = groupd.get_group(key)
    null_df = tmp[tmp['ProsConsAdvPM_allNCh_avgCom'].isnull()]
    true_tmp = tmp.isnull()

    for index in null_df.index:
        if index == min(tmp.index):
            continue

        last_year_index = index - 1

        tmp_keys = tmp.keys()
        for tmp_key in tmp_keys:
            if not true_tmp.ix[index, tmp_key]:
                continue

            tmp.ix[index, tmp_key] = tmp.ix[last_year_index, tmp_key]

    return tmp


# split_dfs = pool.map(process_df, split_keys)
split_dfs = []

for k in keys:
    split_dfs.append(process_df(k))

result = pd.concat(split_dfs, axis=0)

result.to_stata('/home/wangzg/Documents/WangYouan/research/Glassdoor/result/cf_dd_merged_ind_fillna.dta')
result.to_csv('/home/wangzg/Documents/WangYouan/research/Glassdoor/result/cf_dd_merged_ind_fillna.csv')
