#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step10_generate_table5
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

    test_currency = '48'
    sep_num = 4
    table_index = 5

    pool = pathos.multiprocessing.ProcessingPool(4)

    file_list = os.listdir(return_data_path)

    test_path = []
    for file_name in file_list:
        if test_currency in file_name:
            test_path.append(os.path.join(return_data_path, file_name))

    for i in range(2, sep_num):
        panel_index = chr(ord('a') + i - 1)
        print 'Start to generate table {} panel {}'.format(table_index, panel_index)

        test_info_list = zip(test_path, [i] * 4)


        def process_df(test_info):
            data_df = pd.read_pickle(test_info[0])
            month_info = re.findall(r'\d+m', test_info[0])
            # print test_info
            return create_period_table(data_df=data_df, month_period=month_info[0], period_index=test_info[1],
                                       sep_num=sep_num)


        # process_df(test_info_list[0])
        result_dfs = pool.map(process_df, test_info_list)
        result_df = pd.concat(result_dfs, axis=1)
        result_df.to_pickle(os.path.join(temp_path, 'table{}{}.p'.format(table_index, panel_index)))
