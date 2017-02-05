#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step2_generate_learning_return
# @Date: 2017-01-17
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import pandas as pd

from path_info import *

review_month_list = pd.Series([1, 2, 3, 4, 6, 12, 18, 24])
memory_month_list = pd.Series([1, 2, 3, 4, 6, 12, 18, 24])


def generate_return_table(return_df, cumprod_df, new_key_list, month_num):
    result_df = pd.DataFrame(index=return_df.index)
    result_df['datetime'] = return_df['datetime']
    for key in new_key_list:
        key_info = key.split('_')
        review = int(key_info[3]) / month_num
        memory = int(key_info[5]) / month_num

        index_start = max(review - memory, 0)
        index_end = max(review, memory)

        index = return_df.index

        result_df.loc[:, key] = 0

        while index_end < len(return_df.index):
            max_key_name = (cumprod_df.ix[index[index_end - 1]] /
                            cumprod_df.ix[index[index_end - review - 1]]).idxmax(axis=1)

            current_end = max(index_end + memory, len(result_df.index))
            result_df.loc[index_end: current_end, key] = return_df.loc[index_end: current_end, max_key_name]

            index_start += memory
            index_end = current_end

    return result_df


# start to generate learning returns
for data_file in os.listdir(return_data_path):
    if not data_file.startswith('20160919') or not data_file.endswith('p'):
        continue

    df = pd.read_pickle(os.path.join(return_data_path, data_file))
    # own_report_df = own_report_df.set_index('datetime', drop=True)

    # decide how many months are in this file
    if '12m' in data_file:
        month_num = 12

    elif '6m' in data_file:
        month_num = 6

    elif '3m' in data_file:
        month_num = 3

    else:
        month_num = 1

    if '48' in data_file:
        curr_num = 48

    else:
        curr_num = 15
    current_review_list = review_month_list[(review_month_list % month_num) == 0]
    current_memory_list = memory_month_list[(memory_month_list % month_num) == 0]

    # generate new column name
    new_col_list = []
    for m in current_memory_list:
        for r in current_review_list:
            new_col_list.append('{}_curr_review_{}_memory_{}_{}m'.format(curr_num, r, m, month_num))

    cumprod_df = (df.drop('datetime', axis=1) + 1).cumprod()

    new_df = generate_return_table(df, cumprod_df, new_col_list, month_num)
    new_df.to_pickle(os.path.join(learning_data_path, '{}_learning.p'.format(data_file[:-2])))
    # new_df.to_csv(os.path.join(learning_data_path, '{}_learning.csv'.format(data_file[:-2])), index=False)
