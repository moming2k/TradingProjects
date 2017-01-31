#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: util_function
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime
import calendar

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from constants import Constant
from path_info import stock_price_path

const = Constant()


def load_stock_info(trade_date, ticker, market_type, price_path=None):
    """
    Load stock info
    :param trade_date: datetime type
    :param ticker: '000001'
    :param market_type: SZ of SH
    :return: stock data info
    """
    if price_path is None:
        price_path = stock_price_path
    if not os.path.isfile(os.path.join(price_path, '{}.p'.format(trade_date.strftime('%Y%m%d')))):
        return pd.DataFrame()
    trade_day_stock_df = pd.read_pickle(os.path.join(price_path, '{}.p'.format(trade_date.strftime('%Y%m%d'))))
    used_stock_data = trade_day_stock_df[trade_day_stock_df[const.STOCK_TICKER] == ticker]

    # use different data based on market type
    if market_type == 'SZ':
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 1]
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 2]

    else:
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 4]
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 8]
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 16]

    return used_stock_data


def merge_result(result_path):
    file_list = os.listdir(result_path)

    df = pd.DataFrame()

    for file_name in file_list:
        if not file_name.endswith('.p'):
            continue

        column_name = file_name[:-2]
        new_column = pd.read_pickle(os.path.join(result_path, file_name))
        new_column *= (10000.0 / new_column[0])
        df[column_name] = new_column

    return df


def date_as_float(dt):
    size_of_day = 1. / 366.
    size_of_second = size_of_day / (24. * 60. * 60.)
    days_from_jan1 = dt - datetime.datetime(dt.year, 1, 1)
    if not calendar.isleap(dt.year) and days_from_jan1.days >= 31 + 28:
        days_from_jan1 += datetime.timedelta(1)
    return dt.year + days_from_jan1.days * size_of_day + days_from_jan1.seconds * size_of_second


def plot_picture(data_series, picture_title, picture_save_path, text=None):
    # get data series info
    date_series = data_series.index

    # plot file and save picture
    fig = plt.figure(figsize=(15, 6))
    if text is not None:
        plt.figtext(0.01, 0.01, text, horizontalalignment='left')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.plot(date_series, data_series, 'r-')
    min_date = date_series[0]
    max_date = date_series[-1]
    plt.gca().set_xlim(min_date, max_date)
    fig.autofmt_xdate()
    fig.suptitle(picture_title)

    # print dir(fig)
    fig.savefig(picture_save_path)
    plt.close()


def get_sharpe_ratio(df):
    """ Input should be return df """
    return df.mean() / df.std() * np.sqrt(const.working_days)


def get_annualized_return(df):
    """ input should be wealth df """
    start_date = df.first_valid_index()
    end_date = df.last_valid_index()

    ann_return = (df.ix[end_date] / df.ix[start_date]) ** (1 / (date_as_float(end_date) - date_as_float(start_date))
                                                           ) - 1
    return ann_return


def get_max_draw_down(data_series):
    max_wealth = data_series[0]
    draw_back_rate = float('-inf')

    for i in data_series[1:]:
        draw_back_rate = max(draw_back_rate, 1 - i / max_wealth)
        max_wealth = max(max_wealth, i)

    return draw_back_rate
