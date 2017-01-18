#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step3_spa_src_stepwise_test
# @Date: 2017-01-17
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import pandas as pd

from path_info import *


def bootstrap(data_df, num):
    """
    generate bootstrap info
    :param data_df: input data frame, column is carry trade method, row is date
    :param num: bootstrap times
    :return: bootstrap sample
    """
    df_mean = data_df.mean()
    df_demean = data_df - df_mean
    result_df = pd.DataFrame(columns=data_df.keys())
    data_length = data_df.shape[0]
    for i in range(num):
        result_df.loc[i, :] = df_demean.sample(data_length, replace=True).mean()

    return result_df


def stepwise_spa_test(data_df, bootstrap_df, ):
    """ Do stepwise spa test """
    pass
