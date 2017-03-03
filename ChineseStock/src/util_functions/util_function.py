#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: util_function
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import calendar
import datetime
import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..constants.constants import Constant
from ..constants.path_info import stock_price_path

const = Constant()


def load_stock_info(trade_date, ticker, market_type=None, price_path=None):
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
    # if market_type == 'SZ':
    #     used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 1]
    #     used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 2]
    #
    # else:
    #     used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 4]
    #     used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 8]
    #     used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 16]

    return used_stock_data


def merge_result(result_path):
    file_list = os.listdir(result_path)

    df = pd.DataFrame()

    for file_name in file_list:
        if not file_name.endswith('.p'):
            continue

        column_name = file_name[:-2]
        # new_column = pd.read_pickle(os.path.join(result_path, file_name))
        # new_column *= (10000.0 / new_column[0])
        df[column_name] = pd.read_pickle(os.path.join(result_path, file_name))

    return df


def date_as_float(dt):
    size_of_day = 1. / 366.
    size_of_second = size_of_day / (24. * 60. * 60.)
    days_from_jan1 = dt - datetime.datetime(dt.year, 1, 1)
    if not calendar.isleap(dt.year) and days_from_jan1.days >= 31 + 28:
        days_from_jan1 += datetime.timedelta(1)
    return dt.year + days_from_jan1.days * size_of_day + days_from_jan1.seconds * size_of_second


def plot_picture(data_series, picture_title, picture_save_path, text=None):
    """ Draw data series info """

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


def plot_multiline(data_list, legend_list, picture_title, picture_save_path, text=None):
    """ Draw data series info """

    # plot file and save picture
    fig = plt.figure(figsize=(15, 7))

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    if text is not None:
        plt.figtext(0.01, 0.01, text, horizontalalignment='left')

    date_series = data_list[0].index

    color_list = ['r-', 'b-', 'y-', 'g-']

    for i, data_series in enumerate(data_list):
        # get data series info
        plt.plot(date_series, data_series, color_list[i], label=legend_list[i])

    min_date = date_series[0]
    max_date = date_series[-1]
    plt.gca().set_xlim(min_date, max_date)
    plt.legend(loc=0)
    fig.autofmt_xdate()
    fig.suptitle(picture_title)

    # print dir(fig)
    fig.savefig(picture_save_path)
    plt.close()


def draw_histogram(data_series, ylabel, xlabel, title, save_path):
    import matplotlib.pyplot as plt
    plt.hist(data_series, 50, normed=1, color='green', alpha=0.75)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)

    plt.savefig(save_path)
    plt.close()


def get_sharpe_ratio(df, df_type=const.RETURN_DATAFRAME, working_days=const.working_days):
    """ Input should be return own_report_df """
    if df_type == const.RETURN_DATAFRAME:
        return df.mean() / df.std() * np.sqrt(working_days)

    elif df_type == const.WEALTH_DATAFRAME:
        return_df = (df - df.shift(1)) / df.shift(1)
        # return_df.loc[return_df.first_valid_index(), :] = 0.0
        return get_sharpe_ratio(return_df, df_type=const.RETURN_DATAFRAME, working_days=working_days)

    else:
        raise ValueError('Unknown dataframe type {}'.format(df_type))


def get_annualized_return(df, df_type=const.WEALTH_DATAFRAME):
    """ input should be wealth own_report_df """

    if df_type == const.WEALTH_DATAFRAME:
        start_date = df.first_valid_index()
        end_date = df.last_valid_index()
        return (df.ix[end_date] / df.ix[start_date]) ** (1 / (date_as_float(end_date) - date_as_float(start_date))) - 1

    elif df_type == const.RETURN_DATAFRAME:
        wealth_df = (df + 1).cumprod()
        return get_annualized_return(wealth_df, df_type=const.WEALTH_DATAFRAME)

    else:
        raise ValueError('Unknown dataframe type {}'.format(df_type))


def get_max_draw_down(data_series):
    max_wealth = data_series[0]
    draw_back_rate = float('-inf')

    for i in data_series[1:]:
        draw_back_rate = max(draw_back_rate, 1 - i / max_wealth)
        max_wealth = max(max_wealth, i)

    return draw_back_rate


def print_info(info_str):
    print datetime.datetime.today(), info_str


def calculate_stock_run_up_rate(ticker, query_date, x, y, stock_price_path, index_price_df,
                                price_type=const.STOCK_CLOSE_PRICE):
    """
    Calculate stock run up info, to check get the final run up rate
    :param ticker: stock ticker info
    :param query_date: the query date of the run up rate
    :param x:
    :param y:
    :param stock_price_path:
    :param index_price_df:
    :return:
    """

    trading_days = index_price_df.index
    trading_days = trading_days[trading_days < query_date]
    if trading_days.shape[0] < x:
        return np.nan

    x_date = trading_days[-x]
    y_date = trading_days[-y]

    x_stock_data = load_stock_info(x_date, ticker, price_path=stock_price_path)
    y_stock_data = load_stock_info(y_date, ticker, price_path=stock_price_path)

    if x_stock_data.empty or y_stock_data.empty:
        return np.nan

    price_stock_x = x_stock_data.ix[x_stock_data.first_valid_index(), price_type]
    price_stock_y = y_stock_data.ix[y_stock_data.first_valid_index(), price_type]

    price_index_x = index_price_df.ix[x_date, price_type]
    price_index_y = index_price_df.ix[y_date, price_type]

    return (price_stock_y - price_stock_x) / price_stock_x - (price_index_y - price_index_x) / price_index_x
