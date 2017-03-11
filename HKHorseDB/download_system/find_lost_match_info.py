#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: find_lost_match_info
# @Date: 2017-03-09
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

race_number = pd.read_pickle('/Users/warn/Documents/RAForWangZG/HKHorse/race_info/race_number.p')


def find_lost_match_info(folder_path):
    files = os.listdir(folder_path)
    match_dict = {}

    for file_name in files:
        if not file_name.endswith('xlsx'):
            continue

        race_date = file_name.split('_')[0]
        race_id = int(file_name.split('_')[1].split('.')[0])
        if race_date in match_dict:
            match_dict[race_date].append(race_id)

        else:
            match_dict[race_date] = [race_id]

    missing_dict = {}
    for race_date in match_dict:
        info_list = match_dict[race_date]
        max_match = race_number.ix[race_date]
        miss_id = set(range(1, max_match + 1)).difference(info_list)
        if miss_id:
            missing_dict[race_date] = list(miss_id)

    return missing_dict


if __name__ == '__main__':

    import pprint

    path1 = '/Users/warn/Documents/RAForWangZG/HKHorse/race_in_hv'
    path2 = '/Users/warn/Documents/RAForWangZG/HKHorse/race_in_st'
    lack_in_hv = find_lost_match_info(path1)
    lack_in_st = find_lost_match_info(path2)

    with open('lack_in_hv.txt', 'w') as f:
        f.write(pprint.pformat(lack_in_hv))

    with open('lack_in_st.txt', 'w') as f:
        f.write(pprint.pformat(lack_in_st))
