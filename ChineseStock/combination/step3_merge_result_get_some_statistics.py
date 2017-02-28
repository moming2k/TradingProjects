#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step3_merge_result_get_some_statistics
# @Date: 2017-01-18
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime
import calendar

import pandas as pd
import numpy as np

from constant import Constant as const
from get_root_path import get_root_path

root_path = get_root_path()
data_path = os.path.join(root_path, 'data')
temp_path = os.path.join(root_path, 'temp')
result_path = os.path.join(root_path, 'result')
buy_only_result = os.path.join(result_path, 'buy_only')

file_list = os.listdir(result_path)

merged_df = None

for file_name in file_list:
    if not file_name.startswith('only') or not file_name.endswith('.p'):
        continue
    df = pd.read_pickle(os.path.join(result_path, file_name))
    if merged_df is None:
        merged_df = pd.DataFrame(index=df.index)

    merged_df.merge(df, left_index=True, right_index=True,
                    how='outer')

merged_df.to_pickle(os.path.join(buy_only_result, 'buy_only_wealth.p'))

# calculate return info
one_diff = merged_df.shift(1)
return_df = (one_diff - merged_df) / merged_df

return_df.to_pickle(os.path.join(buy_only_result, 'buy_only_return.p'))

# get trading days statistics
trading_days_list = pd.read_pickle(os.path.join(data_path, '__trading_days_list.p'))

period = trading_days_list[trading_days_list > datetime.datetime(2005, 12, 31)]
period = period[period < datetime.datetime(2016, 1, 1)]

# there are 2429 days in total
working_days = 251.0

# start to calculate some statistics
statistics_df = pd.DataFrame(columns=return_df.keys())
strategy_names = return_df.keys()

wealth_df = merged_df.transpose()
total_return = wealth_df[merged_df.index[-1]] / wealth_df[merged_df.index[0]]

statistics_df.loc['total_return', :] = total_return.transpose()

size_of_day = 1. / 366.
size_of_second = size_of_day / (24. * 60. * 60.)


def date_as_float(dt):
    days_from_jan1 = dt - datetime.datetime(dt.year, 1, 1)
    if not calendar.isleap(dt.year) and days_from_jan1.days >= 31 + 28:
        days_from_jan1 += datetime.timedelta(1)
    return dt.year + days_from_jan1.days * size_of_day + days_from_jan1.seconds * size_of_second


total_years = date_as_float(merged_df.index[-1]) - date_as_float(merged_df.index[0])

annualized_return = total_return.apply(lambda x: x ** (1 / total_years) - 1)

statistics_df.loc['annualized_return_all', :] = annualized_return.transpose()
statistics_df.loc['sharpe_ratio_all', :] = return_df.mean() / return_df.std() * working_days ** 0.5


def get_annualized_return_sharpe_return(period1, period2):
    if period1 > period2:
        period1, period2 = period2, period1

    years = date_as_float(period2) - date_as_float(period1)
    temp_df = merged_df[merged_df.index >= period1]
    temp_df = temp_df[temp_df.index < period2]
    transpose_df = temp_df.transpose()
    total_return = transpose_df[temp_df.last_valid_index()] / transpose_df[temp_df.first_valid_index()]
    annualized_interest_rate = total_return.apply(lambda x: x ** (1 / years) - 1)
    temp_return_df = return_df[return_df.index >= period1]
    temp_return_df = temp_return_df[temp_return_df.index < period2]
    sharpe_ratio = temp_return_df.mean() / temp_return_df.std() * working_days ** 0.5
    return annualized_interest_rate.transpose(), sharpe_ratio


# end_years is 2013
for start_years in range(2006, 2011):
    start_date = datetime.datetime(start_years, 1, 1)
    end_date = datetime.datetime(2014, 1, 1)
    key_suffix = '{:02d}_13'.format(start_years % 100)
    statistics_df.loc['annualized_return_{}'.format(key_suffix)], \
    statistics_df.loc['sharpe_ratio_{}'.format(key_suffix)] = get_annualized_return_sharpe_return(start_date,
                                                                                                  end_date)

# end_years is 2016
for start_years in range(2006, 2014):
    start_date = datetime.datetime(start_years, 1, 1)
    end_date = datetime.datetime(2017, 1, 1)
    key_suffix = '{:02d}_16'.format(start_years % 100)
    statistics_df.loc['annualized_return_{}'.format(key_suffix)], \
    statistics_df.loc['sharpe_ratio_{}'.format(key_suffix)] = get_annualized_return_sharpe_return(start_date,
                                                                                                  end_date)

statistics_df.to_pickle(os.path.join(buy_only_result, 'only_buy_statistics.p'))
statistics_df.to_csv(os.path.join(buy_only_result, 'only_buy_statistics.csv'))

# get_greater_than 1.5 list
transpose_statistic = statistics_df.transpose()
names = transpose_statistic.keys()

set_dict = {}

for index in names:
    if 'sharpe' not in index:
        continue

    remain = transpose_statistic[transpose_statistic[index] > 1.5]
    set_dict[index] = set(remain.index.tolist())

union_set = set_dict['sharpe_ratio_06_13']
for key in set_dict:
    union_set = union_set.intersection(set_dict[key])
