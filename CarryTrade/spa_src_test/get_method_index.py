#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: get_method_index
# Author: Mark Wang
# Date: 27/9/2016

import os
import pandas as pd

FORMER_RESULT_PATH = '/Users/warn/Documents/RAForWangZG/CarryTrade/no_origin_data/xlsx_results'
CSV_RESULT_PATH = '/Users/warn/Documents/RAForWangZG/CarryTrade/no_origin_data'

FILE_NAME_DICT = {'48': {'1m': '20160919_1m_updated_48_curr_add_learning.csv',
                         '3m': '20160919_3m_updated_48_curr_add_learning.csv',
                         '6m': '20160919_6m_updated_48_curr_add_learning.csv',
                         '12m': '20160919_12m_updated_48_curr_add_learning.csv',
                         },
                  '15': {'1m': '20160919_1m_updated_15_curr_add_learning.csv',
                         '3m': '20160919_3m_updated_15_curr_add_learning.csv',
                         '6m': '20160919_6m_updated_15_curr_add_learning.csv',
                         '12m': '20160919_12m_updated_15_curr_add_learning.csv',
                         },
                  }

if __name__ == '__main__':
    div_4_max_df = pd.read_excel(os.path.join(FORMER_RESULT_PATH, 'max_info_statistics.xlsx'),
                                 sheetname='division 4 (no dup)')
    div_8_max_df = pd.read_excel(os.path.join(FORMER_RESULT_PATH, 'max_info_statistics.xlsx'),
                                 sheetname='division 8 (no dup)')

    for method in div_4_max_df['method']:
        method_info_list = method.split('_')
        data_df = pd.read_csv(os.path.join(CSV_RESULT_PATH, FILE_NAME_DICT[method_info_list[0]][method_info_list[-1]]),
                              index_col=0)
        print data_df.keys().tolist().index(method)
