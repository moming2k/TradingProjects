#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: make_up_missing_variables
# @Date: 2016-12-10
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd

from constants import dep_other_vars

today_str = datetime.datetime.today().strftime('%Y%m%d')

root_path = '/home/wangzg/Documents/WangYouan/research/Glassdoor'

data_path = os.path.join(root_path, '20121210data')

temp_path =os.path.join(root_path, '{}_temp'.format(today_str))

if not os.path.isdir(temp_path):
    os.makedirs(temp_path)

da_df = pd.read_stata(os.path.join(data_path, 'da_commun_dropna.dta'))
dd_df = pd.read_stata(os.path.join(data_path, 'dd_commun_dropna.dta'))

da_keys = da_df.keys()

for key in da_keys:
    if key not in dep_other_vars and not (key.endswith('simple') or key.endswith('simple1k')):
        del da_df[key]

dd_keys = dd_df.keys()

for key in dd_keys:
    if key not in dep_other_vars and not (key.endswith('simple') or key.endswith('simple1k')):
        del dd_df[key]

dd_df.to_pickle(os.path.join(temp_path, 'dd_commun_simple.p'))
da_df.to_pickle(os.path.join(temp_path, 'da_commun_simple.p'))

