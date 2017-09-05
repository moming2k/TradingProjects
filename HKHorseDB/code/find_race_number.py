#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: find_race_number
# @Date: 2017-03-09
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os

import pandas as pd

data_path = '/Users/moming2k/project/TradingProjects/HKHorseDB/data/horse_win_loss_data'

date_list = os.listdir(data_path)

match_info = {}

for date_dir in date_list:
    date_dir_path = os.path.join(data_path, date_dir)
    if not os.path.isdir(date_dir_path):
        continue
    race_num = 0

    for file_name in os.listdir(date_dir_path):
        if file_name.endswith('csv'):
            race_num += 1

    match_info[date_dir] = race_num

df = pd.Series(match_info)
