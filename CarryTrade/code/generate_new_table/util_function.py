#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: util_function
# @Date: 2017-01-19
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime
import calendar

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from constant import Constant as const
from constant import TIME_SEP


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


def plot_sub_date_picture(data_series, picture_title, picture_save_path, period=1):
    # get data series info

    time_sep = TIME_SEP[::2]
    in_start_date = time_sep[period - 1]
    out_end_date = time_sep[period + 1]

    data_series = data_series[data_series.index >= in_start_date]
    data_series = data_series[data_series.index < out_end_date]

    wealth_series = (data_series + 1).cumprod()
    date_series = data_series.index

    # plot file and save picture
    plt.clf()
    fig = plt.figure(figsize=(15, 6))

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.plot(date_series, wealth_series, 'r-')
    min_date = date_series[0]
    max_date = date_series[-1]
    plt.gca().set_xlim(min_date, max_date)
    fig.autofmt_xdate()
    fig.suptitle(picture_title)
    plt.axvline(time_sep[period], color='b')
    # print dir(fig)
    fig.text(0.28, 0.6, 'In-sample', fontsize=15)
    fig.text(0.7, 0.4, 'Out-of-sample', fontsize=15)
    fig.savefig(picture_save_path)


if __name__ == '__main__':
    import os

    data_path = '/Users/warn/PycharmProjects/QuestionFromProfWang/CarryTrade/data/adjusted_return'
    data_file_path = os.path.join(data_path, '20160919_1m_updated_15_curr.p')

    df = pd.read_pickle(data_file_path)

    plot_sub_date_picture(df['15_currs_10_liquid_2_parts_1m'], 'test', 'test.png', 2)