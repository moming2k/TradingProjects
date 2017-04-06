#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step7_sort_forecast_runup_result
# @Date: 2017-04-06
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd
import numpy as np
import pathos

from ..constants.constants import Constant as const


def merge_result(temp_path, process_num):
    dir_list = os.listdir(temp_path)

    pool = pathos.multiprocessing.ProcessingPool(process_num)

    alpha_df_list = []
    raw_df_list = []

    for dir_name in dir_list:
        if not dir_name.endswith('wealth'):
            continue

        current_path = os.path.join(temp_path, dir_name)

        if not os.path.isdir(current_path):
            continue

        file_list = os.listdir(current_path)

        def process_file_list(file_list_info):

            raw_df = pd.DataFrame()
            alpha_df = pd.DataFrame()
            for f in file_list_info:
                if not f.endswith('.p'):
                    continue

                df = pd.read_pickle(os.path.join(current_path, f))
                col_name = '_'.join(f.split('_')[:-1])

                if 'raw' in f:
                    raw_df[col_name] = df

                elif 'alpha' in f:
                    alpha_df[col_name] = df

            return alpha_df, raw_df

        split_file = np.array_split(file_list, process_num)

        result_dfs = pool.map(process_file_list, split_file)

        alpha_df_list.extend([i[0] for i in result_dfs])
        raw_df_list.extend([i[1]] for i in result_dfs)

    return pd.concat(alpha_df_list, axis=1), pd.concat(raw_df_list, axis=1)


if __name__ == '__main__':
    temp_path = os.path.join(const.TEMP_PATH, 'forecast_run_up_stock_data_20170214')
    result_path = os.path.join(const.RESULT_PATH, 'forecast_run_up_stock_data_20170214', 'result')

    if not os.path.isdir(result_path):
        os.makedirs(result_path)

    alpha_df, raw_df = merge_result(temp_path, 18)

    alpha_df.to_pickle(os.path.join(result_path, 'alpha_statistics.p'))
    alpha_df.to_csv(os.path.join(result_path, 'alpha_statistics.csv'), index=False)

    raw_df.to_pickle(os.path.join(result_path, 'raw_statistics.p'))
    raw_df.to_csv(os.path.join(result_path, 'raw_statistics.csv'), index=False)
