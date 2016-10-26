#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: replace_gvkid
# Author: Mark Wang
# Date: 26/10/2016

import os

import pandas as pd

root_path = '/home/wangzg/Documents/WangYouan/research/Glassdoor'
result_path = 'result'
data_path = '20161025merge_data'

if __name__ == '__main__':
    df = pd.read_csv(os.path.join(root_path, data_path, 'gvkey_glassdoorID', 'crosswalk_combined.csv'),
                     dtype={'GVKEY': str, 'GDID_ZG': str, 'GDID_NEW': str},
                     usecols=['GVKEY', 'GDID_ZG', 'GDID_NEW'])
    df['GDID'] = df['GDID_ZG']
    df['GDID'].update(df['GDID_NEW'])
    df[['GDID', 'GVKEY']].to_csv(os.path.join(root_path, data_path, 'gvkey_glassdoorID', 'glassdoor_id_gvkey.csv'),
                                 index=False)
