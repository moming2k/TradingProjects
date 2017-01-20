#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step8_generate_table7b
# @Date: 2017-01-20
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from step3_spa_src_stepwise_test import generate_table_3or4
from path_info import total_data_path, temp_path

if __name__ == '__main__':
    import pathos

    pool = pathos.multiprocessing.ProcessingPool(4)
    file_list = os.listdir(total_data_path)

    test_currency = '15'

    test_path = []
    for file_name in file_list:
        if test_currency in file_name:
            test_path.append(os.path.join(total_data_path, file_name))


    def process_df(file_path):
        return generate_table_3or4(file_path)


    result_dfs = pool.map(process_df, test_path)
    result_df = pd.concat(result_dfs, axis=1)
    result_df.to_pickle(os.path.join(temp_path, 'table7b.p'))