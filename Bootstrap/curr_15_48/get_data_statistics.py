#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: get_data_statistics
# Author: Mark Wang
# Date: 27/9/2016

import os

import scipy.io
import pandas as pd

mat_data_path = '/Users/warn/Documents/RAForWangZG/2016.9.18/csv_results/output'
FORMER_RESULT_PATH = '/Users/warn/Documents/RAForWangZG/2016.9.18/xlsx_results'

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
    div_4_max_df = pd.read_excel(os.path.join(FORMER_RESULT_PATH, 'max_info_statistics.xlsx'),
                                 sheetname='division 4 (no dup)')
    div_8_max_df = pd.read_excel(os.path.join(FORMER_RESULT_PATH, 'max_info_statistics.xlsx'),
                                 sheetname='division 8 (no dup)')

    for index in div_4_max_df.index:
        method = div_4_max_df.ix[index, 'method']
        method_info_list = method.split('_')
        mat_file_name = 'division_4_curr_{}_{}'.format(method_info_list[0], method_info_list[-1])
        mat = scipy.io.loadmat(os.path.join(mat_data_path, mat_file_name))
        method_index = div_4_max_df.ix[index, 'Target Index']
        src = mat[SRC][method_index]
        src_k = mat[SRC_K][method_index]
        spa_mean = mat[SPA_MEAN][method_index]
        spa_k_mean = mat[SPA_K_MEAN][method_index]
        spa_sharpe = mat[SPA_SHARPE][method_index]
        spa_k_sharpe = mat[SPA_K_SHARPE][method_index]
        step_spa_mean = mat[STEP_SPA_MEAN][method_index]
        step_spa_sharpe = mat[STEP_SPA_SHARPE][method_index]

        result = ''
        for i in range(4):
            result = '{},{},{},{},{},{},{},{},{}'.format(result, src[i], src_k[i], spa_mean[i], spa_k_mean[i],
                                                         step_spa_mean[i], spa_sharpe[i], spa_k_sharpe[i],
                                                         step_spa_sharpe[i])

        print result[1:]
