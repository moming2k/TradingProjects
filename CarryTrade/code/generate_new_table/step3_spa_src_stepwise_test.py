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
    return df_demean.sample(num, replace=True)
