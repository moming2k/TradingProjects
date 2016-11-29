#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: merge_dd_cf
# Author: Mark Wang
# Date: 6/11/2016

import os
import datetime

import pandas as pd

path = '/home/wangzg/Documents/WangYouan/research/Glassdoor'
input_path = 'input_data'
output_path = 'output'
result_path = 'result'

today = datetime.datetime.today().strftime('%Y%m%d')

dd_cf = pd.read_csv(os.path.join(path, output_path, 'cf_dd_merged.csv'),
                    dtype={'gvkey': str, 'fyear': str, 'gdid': str})

fiscal_info = pd.read_csv(os.path.join(path, result_path, 'firm_fiscal_year_statistics_sample.csv'),
                          dtype={'fiscalYear': str, 'FK_employerId': str})

fiscal_info['gdid'] = fiscal_info['FK_employerId']
fiscal_info['fyear'] = fiscal_info['fiscalYear']
fiscal_info.drop(['FK_employerId', 'fiscalYear'], axis=1, inplace=True)

df = dd_cf.merge(fiscal_info, how='outer', on=['gdid', 'fyear'])

df.to_csv(os.path.join(path, result_path, '{}cf_dd_merged_ind.csv'.format(today)), index=False, encoding='utf8')


def process_name(name):
    new_name = name.replace('CommunGNLP', '')
    new_name = new_name.replace('_firmYear_', '_')
    new_name = new_name.replace('netProsConsAdviceNum', 'allNum')
    new_name = new_name.replace('netProsConsAdviceCommunNum', 'allCommunNum')
    new_name = new_name.replace('netProsConsCommunNum', 'allCommunNum')
    new_name = new_name.replace('netProsConsNum', 'allNum')
    new_name = new_name.replace('net', '')
    new_name = new_name.replace('average', 'avg')
    new_name = new_name.replace('Advice', 'Adv')
    new_name = new_name.replace('advice', 'adv')
    new_name = new_name.replace('Commun', 'Com')
    new_name = new_name.replace('NumWord', 'NWd')
    new_name = new_name.replace('NumSent', 'NSt')
    new_name = new_name.replace('NumChar', 'NCh')
    new_name = new_name.replace('NumCom', 'NCom')
    new_name = new_name.replace('Pol', 'P')
    new_name = new_name.replace('Mag', 'M')
    return new_name


keys = df.keys()

for key in keys:
    new_key = process_name(key)
    if new_key == key:
        continue

    df[new_key] = df[key]
    df.drop(key, axis=1, inplace=True)

df.to_stata(os.path.join(path, result_path, '{}cf_dd_merged_ind.pta'.format(today)), write_index=False)

df['fyear'] = df['fyear'].apply(int)
df['sic2'] = df['sic2'].apply(int)

df.to_stata(os.path.join(path, result_path, '{}cf_dd_merged_ind_right.pta'.format(today)), write_index=False)

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

df.to_stata(os.path.join(path, result_path, '{}cf_dd_merged.dta'.format(today)), write_index=False)
