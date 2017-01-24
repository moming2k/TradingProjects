#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: util_function
# @Date: 2017-01-19
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime
import calendar

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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


def plot_date_picture(date_list, data_series, picture_title, picture_save_path):
    # get data series info
    data_series = data_series.shift(1) + 1
    data_series[0] = 1
    for i in range(1, len(data_series)):
        data_series[i] = data_series[i - 1] * data_series[i]

    # plot file and save picture
    plt.clf()
    fig = plt.figure(figsize=(15, 6))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.plot(date_list, data_series, 'r-')
    min_date = date_list[0]
    max_date = date_list[-1]
    plt.gca().set_xlim(min_date, max_date)
    fig.autofmt_xdate()
    fig.suptitle(picture_title)
    fig.savefig(picture_save_path)
