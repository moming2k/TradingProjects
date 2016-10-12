#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: utils
# Author: Mark Wang
# Date: 12/10/2016

import re

import numpy as np
import pandas as pd
import pathos.multiprocessing as process


def reformat_para(para_str):
    if not hasattr(para_str, 'decode'):
        return ''
    sentences = para_str.decode("utf8")
    sentences = sentences.replace('\r\n', '.')
    sentences = re.sub(r'[.]+', '. ', sentences)
    sentences = re.sub(r'[ ]+', ' ', sentences)
    return sentences.lower()


def multi_process_df(process_num, df, process_func):

    pool = process.ProcessingPool(process_num)

    split_dfs = np.array_split(df, process_num)
    result_dfs = pool.map(process_func, split_dfs)
    return pd.concat(result_dfs, axis=0)


def count_target_num(target_list, target):
    count_result = 0
    for i in target_list:
        if i == target:
            count_result += 1
    return count_result
