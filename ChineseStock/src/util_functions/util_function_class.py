#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: util_function_class
# @Date: 2017-02-17
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime
import calendar

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import pandas as pd
from ..constants.constants import Constant


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
        return (alpha_strategy.ix[end_index] - alpha_strategy.ix[start_index]) / \
               alpha_strategy.ix[start_index] / years
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
        import matplotlib.pyplot as plt
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
            # return_df.loc[return_df.first_valid_index(), :] = 0.0
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
