#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: split_Compustat_tick
# Author: Mark Wang
# Date: 27/8/2016

import os

import pathos.multiprocessing as process
import pandas as pd
import numpy as np

combast_df = pd.read_csv('Stock_data/Compustat.csv', dtype={'datadate': str, 'cusip': str, 'gvkey': str, 'iid': str})
combast_group = combast_df.groupby('tic')

def process_df(group_keys):
    for ticker in group_keys:
        sub_df = combast_group.get_group(ticker)
        file_path = os.path.join('Stock_data', 'compustat', '{}_COMPU.csv'.format(ticker))
        del sub_df['tic']
        sub_df.to_csv(file_path, encoding='utf8', index=None)

    return ""


if __name__ == "__main__":
    process_num = 16
    pool = process.ProcessingPool(process_num)
    split_groups = np.array_split(combast_group.groups.keys(), process_num)
    pool.map(process_df, split_groups)