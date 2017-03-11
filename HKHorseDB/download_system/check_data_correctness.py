#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: check_data_correctness
# @Date: 2017-03-10
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import re

import pandas as pd

st_path = '/Users/warn/Documents/RAForWangZG/HKHorse/race_in_st'
hv_path = '/Users/warn/Documents/RAForWangZG/HKHorse/race_in_hv'


def check_data_correctness(file_path):
    if not file_path.endswith('xlsx'):
        return ''

    file_name = file_path.split('/')[-1]
    dir_name = file_path.split('/')[-2].split('_')[-1].upper()
    race_date = file_name.split('_')[0]
    race_index = file_name.split('_')[1].split('.')[0]

    try:
        df = pd.read_excel(file_path)

        df_place = df['Place'].dropna()

        for i in range(df_place.size - 1, -1, -1):
            if isinstance(df_place[i], int):
                if df_place[i] != i + 1:
                    return "('{}', {}, {}) seq error".format(race_date, race_index, dir_name)
                else:
                    return ''

            elif isinstance(df_place[i], float):
                if int(df_place[i]) != i + 1:
                    return "('{}', {}, {}) seq error".format(race_date, race_index, dir_name)
                else:
                    return ''

            elif hasattr(df_place[i], 'encode') and 'DH' in df_place[i]:
                place = int(df_place[i].split(' ')[0])

                for j in range(i - 1, -1):
                    if 'DH' not in df_place[j]:
                        break
                    else:
                        place += 1

                if place != i + 1:
                    return "('{}', {}, {}) seq error".format(race_date, race_index, dir_name)
                else:
                    return ''

        return "('{}', {}, {}) no data".format(race_date, race_index, dir_name)
    except Exception, err:
        return "('{}', {}, {}) file error".format(race_date, race_index, dir_name)


if __name__ == '__main__':
    import pathos

    pool = pathos.multiprocessing.ProcessingPool(3)

    for data_path in [st_path, hv_path]:
        print st_path
        file_list = os.listdir(data_path)
        path_list = map(lambda x: os.path.join(data_path, x), file_list)
        failed_list = pool.map(check_data_correctness, path_list)

        for i in failed_list:
            if i:
                print i

    pool.close()

    # print check_data_correctness('/Users/warn/Documents/RAForWangZG/HKHorse/race_in_hv/20130417_5.xlsx')
