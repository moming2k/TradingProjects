#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_column_name_to_log_return
# Author: Mark Wang
# Date: 28/8/2016

import os
import datetime

import pathos
import pandas as pd
import numpy as np

log_return_path = "Stock_data/logReturn"
simple_return_path = "Stock_data/simpleReturn"


def process_log_return_file(file_names):
    for name in file_names:
        path = os.path.join(log_return_path, name)
        df = pd.read_csv(path, header=None, names=['date', 'LR'])
        df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y%m%d'))
        df.to_csv(path, index=False)

    return ""


def process_simple_return_file(file_names):
    for name in file_names:
        path = os.path.join(simple_return_path, name)
        df = pd.read_csv(path, header=None, names=['date', 'SR'])
        df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y%m%d'))
        df.to_csv(path, index=False)

    return ""


process_num = 19
pool = pathos.multiprocessing.ProcessingPool(process_num)

file_list = os.listdir(log_return_path)

split_list = np.array_split(file_list, process_num)
pool.map(process_log_return_file, split_list)

file_list = os.listdir(simple_return_path)
split_list = np.array_split(file_list, process_num)
pool.map(process_simple_return_file, split_list)
