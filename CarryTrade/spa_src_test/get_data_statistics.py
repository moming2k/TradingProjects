#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: get_data_statistics
# Author: Mark Wang
# Date: 27/9/2016

import os

import scipy.io
import pandas as pd

mat_data_path = '/Users/warn/Documents/RAForWangZG/CarryTrade/csv_results/output'
FORMER_RESULT_PATH = '/Users/warn/Documents/RAForWangZG/CarryTrade/csv_results/xlsx_results'

mat_data_list = os.listdir(mat_data_path)

SPA_K_MEAN = 'reject_rate_SPA_k_mean'
SPA_K_SHARPE = 'reject_rate_SPA_k_sharpe'
SPA_MEAN = 'reject_rate_SPA_mean'
SPA_SHARPE = 'reject_rate_SPA_sharpe'
SRC = 'reject_rate_SRC'
SRC_K = 'reject_rate_SRC_k'
STEP_SPA_SHARPE = 'reject_rate_step_SPA_sharpe'
STEP_SPA_MEAN = 'reject_rate_step_SPA_mean'

if __name__ == '__main__':
    q = 4
    # div_4_max_df = pd.read_excel(os.path.join(FORMER_RESULT_PATH, 'max_info_statistics.xlsx'),
    #                              sheetname='division 4 (no dup)')
    max_sta_df = pd.read_excel(os.path.join(FORMER_RESULT_PATH, 'max_info_statistics.xlsx'),
                               sheetname='division {} (no dup)'.format(q))

    # print div_4_max_df.keys()

    for index in max_sta_df.index:
        method = max_sta_df.ix[index, 'method']
        method_info_list = method.split('_')
        file_type = max_sta_df.ix[index, 'fileType']
        mat_file_name = 'division_{}_curr_{}_{}'.format(q, method_info_list[0], file_type)
        mat = scipy.io.loadmat(os.path.join(mat_data_path, mat_file_name))
        method_index = max_sta_df.ix[index, 'Target Index']
        src = mat[SRC][method_index]
        src_k = mat[SRC_K][method_index]
        spa_mean = mat[SPA_MEAN][method_index]
        spa_k_mean = mat[SPA_K_MEAN][method_index]
        spa_sharpe = mat[SPA_SHARPE][method_index]
        spa_k_sharpe = mat[SPA_K_SHARPE][method_index]
        step_spa_mean = mat[STEP_SPA_MEAN][method_index]
        step_spa_sharpe = mat[STEP_SPA_SHARPE][method_index]

        result = ''
        for i in range(q):
            temp = [src[i], src_k[i], spa_mean[i], spa_k_mean[i], step_spa_mean[i], spa_sharpe[i], spa_k_sharpe[i],
                    step_spa_sharpe[i]]

            result = '{},{}'.format(result, ','.join(map(lambda x: str(float(x) / 500), temp)))

        print result[1:]
