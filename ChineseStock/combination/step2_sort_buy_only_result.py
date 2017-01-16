#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step2_sort_buy_only_result
# @Date: 2017-01-16
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

from util_functions import generate_wealth_df

from get_root_path import get_root_path

root_path = get_root_path()

data_path = os.path.join(root_path, 'data')
temp_path = os.path.join(root_path, 'temp')
result_path = os.path.join(root_path, 'result')
buy_only_result_path = os.path.join(result_path, 'buy_only')

if not os.path.isdir(buy_only_result_path):
    os.makedirs(buy_only_result_path)

folder_dict = {'buy_only_wealth': 'only_buy_all',
               'buy_only_wealth_company': 'only_buy_company',
               'buy_only_wealth_senior': 'only_buy_exe',
               'buy_only_wealth_senior_self': 'only_buy_exe_self',
               'buy_only_wealth_senior_brothers': 'only_buy_exe_brother',
               'buy_only_wealth_senior_parents': 'only_buy_exe_parents',
               'buy_only_wealth_senior_spouse': 'only_buy_exe_spouse',
               }

for key in folder_dict:
    result_df = generate_wealth_df(os.path.join(temp_path, key), folder_dict[key])
    result_df.to_pickle(os.path.join(result_path, '{}.p'.format(folder_dict[key])))
    result_df.to_csv(os.path.join(result_path, '{}.csv'.format(folder_dict[key])))
