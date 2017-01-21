#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: util_function
# @Date: 2017-01-19
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime
import calendar

import pandas as pd

from constant import Constant as const


def date_as_float(dt):
    size_of_day = 1. / 366.
    size_of_second = size_of_day / (24. * 60. * 60.)
    days_from_jan1 = dt - datetime.datetime(dt.year, 1, 1)
    if not calendar.isleap(dt.year) and days_from_jan1.days >= 31 + 28:
        days_from_jan1 += datetime.timedelta(1)
    return dt.year + days_from_jan1.days * size_of_day + days_from_jan1.seconds * size_of_second


def sort_result(input_df):
    result_df = pd.DataFrame(index=input_df.index)
    for i in [const.MEAN_RETURN, const.SHARPE_RATIO]:
        for j in [const.ONE_MONTH, const.THREE_MONTH, const.SIX_MONTH, const.TWELVE_MONTH]:
            key = '{} {}'.format(i, j)
            result_df[key] = input_df[key]

    return result_df