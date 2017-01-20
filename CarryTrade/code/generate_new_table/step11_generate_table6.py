#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: generate_table6
# @Date: 2017-01-20
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import re

import pandas as pd

from step9_create_period_table import create_period_table
from path_info import return_data_path, temp_path

if __name__ == '__main__':
    import pathos
    file_list = os.listdir(return_data_path)

    test_currency = '15'
    sep_num = 4
    table_index = 6

    test_path = []
    for file_name in file_list:
        if test_currency in file_name:
            test_path.append(os.path.join(return_data_path, file_name))

    for i in range(1, sep_num):
        panel_index = chr(ord('a') + i - 1)
        print 'Start to generate table {} panel {}'.format(table_index, panel_index)

        pool = pathos.multiprocessing.ProcessingPool(4)

        def process_df(file_path):
            data_df = pd.read_pickle(file_path)
            month_info = re.findall(r'\d+m', file_path)
            return create_period_table(data_df=data_df, month_period=month_info[0], period_index=i, sep_num=sep_num)


        result_dfs = pool.map(process_df, test_path)
        result_df = pd.concat(result_dfs, axis=1)
        result_df.to_pickle(os.path.join(temp_path, 'table{}{}.p'.format(table_index, panel_index)))
