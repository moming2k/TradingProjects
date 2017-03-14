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

from constants import Constant

const = Constant()


def get_process_num():
    if hasattr(os, 'uname'):
        if os.uname()[1] == 'ewin3102':
            return 38
        else:
            return 18
    else:
        return 38


def make_dirs(dir_or_dirs):
    for dir_path in dir_or_dirs:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)


def get_target_file_name(target_path, keyword, suffix):
    current_path_files = os.listdir(target_path)
    for file_name in current_path_files:
        if keyword in file_name and file_name.endswith(suffix):
            return file_name

    else:
        return None


def load_stock_info(trade_date, ticker, price_path=None):
    """
    Load stock info
    :param trade_date: datetime type
    :param ticker: '000001'
    :return: stock data info
    """
    if price_path is None:
        price_path = const.STOCK_DATA_PATH
    if not os.path.isfile(os.path.join(price_path, '{}.p'.format(trade_date.strftime('%Y%m%d')))):
        return pd.DataFrame()
    trade_day_stock_df = pd.read_pickle(os.path.join(price_path, '{}.p'.format(trade_date.strftime('%Y%m%d'))))
    used_stock_data = trade_day_stock_df[trade_day_stock_df[const.STOCK_TICKER] == ticker]

    return used_stock_data


def merge_result(result_path):
    file_list = os.listdir(result_path)

    df = pd.DataFrame()

    for file_name in file_list:
        if not file_name.endswith('.p'):
            continue

        column_name = file_name[:-2]
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


def plot_multiline_picture_text(pic_title, data_list, legends, save_path, stop_loss_rate):
    line1 = 'Transaction cost 0.2% SR {}%'.format(stop_loss_rate)

    info_list = [line1]

    raw_strategy = data_list[0]
    alpha_strategy = data_list[1]

    time_period = ['all', '09_14', '13_16', 'after_16']
    period_list = [(None, None), (datetime.datetime(2009, 1, 1), datetime.datetime(2015, 1, 1)),
                   (datetime.datetime(2013, 7, 22), datetime.datetime(2016, 7, 20)),
                   (datetime.datetime(2016, 2, 1), None)]

    def generate_line_info(i, date_tuple):
        current_line = 'Date {}'.format(time_period[i])
        result_list = [current_line]

        def get_line_not_alpha(data_series, prefix_info):
            if date_tuple[0] is not None:
                sub_data_series = data_series[data_series.index > date_tuple[0]]
            else:
                sub_data_series = data_series

            if date_tuple[1] is not None:
                sub_data_series = sub_data_series[sub_data_series.index < date_tuple[1]]

            sharpe_ratio = get_sharpe_ratio(sub_data_series, df_type=const.WEALTH_DATAFRAME)
            ann_return = get_annualized_return(sub_data_series, df_type=const.WEALTH_DATAFRAME) * 100
            max_draw_down = get_max_draw_down(sub_data_series) * 100

            current_line = '{}: Sharpe Ratio {:.3f}, Annualized Return {:.2f}%, Max Drawdown rate {:.2f}%'.format(
                prefix_info, sharpe_ratio, ann_return, max_draw_down
            )
            return current_line

        for prefix in ['Raw', 'Alpha']:

            if prefix == 'Raw':
                result_list.append(get_line_not_alpha(raw_strategy, prefix))

            else:
                result_list.append(get_line_not_alpha(alpha_strategy, prefix))

        return result_list

    for index, data_info in enumerate(period_list[:2]):
        info_list.extend(generate_line_info(index, data_info))

    text1 = '\n'.join(info_list)

    info_list = []
    for index, data_info in enumerate(period_list[2:]):
        info_list.extend(generate_line_info(index + 2, data_info))

    text2 = '\n'.join(info_list)

    plot_multiline_alpha(data_list,
                         legend_list=legends,
                         picture_title=pic_title,
                         picture_save_path=save_path,
                         text1=text1, text2=text2)


def plot_multiline_alpha(data_list, legend_list, picture_title, picture_save_path, text1, text2):
    """ Draw data series info """

    # plot file and save picture
    fig = plt.figure(figsize=(15, 8))

    left = 0.1
    bottom = 0.3
    width = 0.75
    height = 0.60
    ax = fig.add_axes([left, bottom, width, height])
    ax.set_title(picture_title)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.figtext(0.01, 0.01, text1, horizontalalignment='left')
    plt.figtext(0.51, 0.01, text2, horizontalalignment='left')

    date_series = data_list[0].index

    color_list = ['r-', 'b-', 'y-', 'g-']

    for i, data_series in enumerate(data_list):
        plt.plot(date_series, data_series, color_list[i], label=legend_list[i])

    min_date = date_series[0]
    max_date = date_series[-1]
    plt.gca().set_xlim(min_date, max_date)
    plt.legend(loc=0)
    fig.autofmt_xdate()
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
    :param price_type: price type of input data
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


class UtilFunction(Constant):
    @staticmethod
    def merge_result(result_path):
        file_list = os.listdir(result_path)

        df = pd.DataFrame()

        for file_name in file_list:
            if not file_name.endswith('.p'):
                continue

            column_name = file_name[:-2]
            df[column_name] = pd.read_pickle(os.path.join(result_path, file_name))

        return df

    @staticmethod
    def get_alpha_strategy_simple_return(alpha_strategy):
        """ Input must be wealth data frame """

        start_index = alpha_strategy.first_valid_index()
        end_index = alpha_strategy.last_valid_index()
        years = UtilFunction.date_as_float(end_index) - UtilFunction.date_as_float(start_index)
        return (alpha_strategy.ix[end_index] - alpha_strategy.ix[start_index]) / 10000.0 / years

    @staticmethod
    def get_alpha_strategy_simple_return2(alpha_strategy):
        """ Input must be wealth data frame """

        start_index = alpha_strategy.first_valid_index()
        end_index = alpha_strategy.last_valid_index()
        years = UtilFunction.date_as_float(end_index) - UtilFunction.date_as_float(start_index)
        # if abs(alpha_strategy.ix[start_index]) > 0.01:
        return (alpha_strategy.ix[end_index] - alpha_strategy.ix[start_index]) / alpha_strategy.ix[start_index] / years
        # else:
        # return float('inf')

    @staticmethod
    def get_wealth_return_mean(alpha_strategy):
        """ Input must be wealth data, return its return mean """
        return_series = (alpha_strategy - alpha_strategy.shift(1)) / alpha_strategy.shift(1)
        return return_series.mean()

    @staticmethod
    def get_wealth_return_std(wealth_series):
        """ Input must be wealth data, return its return std """
        return_series = (wealth_series - wealth_series.shift(1)) / wealth_series.shift(1)
        return return_series.std()

    @staticmethod
    def get_alpha_strategies_pseude_sharpe_ratio(alpha_strategy):
        return_series = (alpha_strategy - alpha_strategy.shift(1)) / alpha_strategy.shift(1)
        return return_series.mean() / return_series.std()

    @staticmethod
    def date_as_float(dt):
        size_of_day = 1. / 366.
        size_of_second = size_of_day / (24. * 60. * 60.)
        days_from_jan1 = dt - datetime.datetime(dt.year, 1, 1)
        if not calendar.isleap(dt.year) and days_from_jan1.days >= 31 + 28:
            days_from_jan1 += datetime.timedelta(1)
        return dt.year + days_from_jan1.days * size_of_day + days_from_jan1.seconds * size_of_second

    @staticmethod
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

    @staticmethod
    def plot_multiline(data_list, legend_list, picture_title, picture_save_path, text=None):
        """ Draw data series info """

        # plot file and save picture
        fig = plt.figure(figsize=(15, 6))

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

    @staticmethod
    def draw_histogram(data_series, ylabel, xlabel, title, save_path):
        plt.hist(data_series, 50, normed=1, color='green', alpha=0.75)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True)

        plt.savefig(save_path)
        plt.close()

    def get_sharpe_ratio(self, df, df_type=None, working_days=None):
        """ Input should be return own_report_df """
        if df_type is None:
            df_type = self.RETURN_DATAFRAME

        if working_days is None:
            working_days = self.working_days

        if df_type == self.RETURN_DATAFRAME:
            return df.mean() / df.std() * np.sqrt(working_days)

        elif df_type == self.WEALTH_DATAFRAME:
            return_df = (df - df.shift(1)) / df.shift(1)
            return self.get_sharpe_ratio(return_df, df_type=self.RETURN_DATAFRAME, working_days=working_days)

        else:
            raise ValueError('Unknown dataframe type {}'.format(df_type))

    def get_annualized_return(self, df, df_type=None):
        """ input should be wealth own_report_df """
        if df_type is None:
            df_type = self.WEALTH_DATAFRAME

        if df_type == self.WEALTH_DATAFRAME:
            start_date = df.first_valid_index()
            end_date = df.last_valid_index()
            return (df.ix[end_date] / df.ix[start_date]) ** (
                1 / (self.date_as_float(end_date) - self.date_as_float(start_date))) - 1

        elif df_type == self.RETURN_DATAFRAME:
            wealth_df = (df + 1).cumprod()
            return self.get_annualized_return(wealth_df, df_type=self.WEALTH_DATAFRAME)

        else:
            raise ValueError('Unknown dataframe type {}'.format(df_type))

    @staticmethod
    def get_max_draw_down(data_series):
        max_wealth = data_series[0]
        draw_back_rate = float('-inf')

        for i in data_series[1:]:
            draw_back_rate = max(draw_back_rate, 1 - i / max_wealth)
            max_wealth = max(max_wealth, i)

        return draw_back_rate

    @staticmethod
    def get_target_file_name(target_path, keyword, suffix):
        current_path_files = os.listdir(target_path)
        for file_name in current_path_files:
            if keyword in file_name and file_name.endswith(suffix):
                return file_name

        else:
            return None

    @staticmethod
    def get_sub_df(df, start_date, end_date):
        if start_date is not None:
            df = df[df.index > start_date]

        if end_date is not None:
            df = df[df.index < end_date]

        return df
