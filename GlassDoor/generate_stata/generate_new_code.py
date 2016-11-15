#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: generate_new_code
# Author: Mark Wang
# Date: 8/11/2016

import os

import pandas as pd

path = '/home/wangzg/Documents/WangYouan/research/Glassdoor'
input_path = 'input_data'
output_path = 'output'
result_path = 'result'

df = pd.read_stata(os.path.join(path, result_path, 'cf_dd_merged_ind_right.pta'))
df['fyear'] = df['fyear'].apply(int)
df['sic2'] = df['sic2'].apply(int)

df.to_stata(os.path.join(path, result_path, 'cf_dd_merged_ind_right.dta'), write_index=False)

df['ProsConsAdvPM_allComNCom_avAll'] = df['ProsConsAdvPM_allComNCom_avgAll']
df['ProsConsAdvPM_allComNCom_avCom'] = df['ProsConsAdvPM_allComNCom_avgCom']

df.drop(['ProsConsAdvPM_allComNCom_avgCom', 'ProsConsAdvPM_allComNCom_avgAll'], axis=1, inplace=True)

keys = df.keys()
start_modify = False

for key in keys:
    if start_modify:
        df['{}1k'.format(key)] = df[key] / 1000

    if key == 'gdid':
        start_modify = True

df.to_stata(os.path.join(path, result_path, 'cf_dd_merged_ind_enlarged.dta'), write_index=False)
