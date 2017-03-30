#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step5_draw_histogram_with_year_sep
# @Date: 2017-03-29
# @Author: Mark Wang
# @Email: wangyouan@gmial.

import os

import pandas as pd

from ..constants.constants import Constant as const
from ..util_functions.util_function_class import UtilFunction

util = UtilFunction()


def get_sub_df(df, start_date=None, end_date=None):
    if start_date is not None:
        sub_df = df[df.index >= start_date]

    else:
        sub_df = df.copy()

    if end_date is not None:
        sub_df = sub_df[sub_df.index <= end_date]

    return sub_df


def plot_histogram_of_target_time_period(result_path, start_date=None, end_date=None, tag=None):
    file_list = os.listdir(result_path)

    alpha_df_list = []
    raw_df_list = []

    for dir_file in file_list:
        if not os.path.isdir(os.path.join(result_path, dir_file)):
            continue

        current_path = os.path.join(result_path, dir_file)

        alpha_file_name = util.get_target_file_name(current_path, 'sr_alpha', '.p')
        raw_file_name = util.get_target_file_name(current_path, 'sr_raw', '.p')

        alpha_df = get_sub_df(pd.read_pickle(os.path.join(current_path, alpha_file_name)), start_date, end_date)
        raw_df = get_sub_df(pd.read_pickle(os.path.join(current_path, raw_file_name)), start_date, end_date)

        alpha_df_list.append(alpha_df)
        raw_df_list.append(raw_df)

    merged_alpha_df = pd.concat(alpha_df_list, axis=1)
    merged_raw_df = pd.concat(raw_df_list, axis=1)

    alpha_return = util.get_annualized_return(merged_alpha_df, const.WEALTH_DATAFRAME)
    raw_return = util.get_annualized_return(merged_raw_df, const.WEALTH_DATAFRAME)

    alpha_sharpe = util.get_sharpe_ratio(merged_alpha_df, const.WEALTH_DATAFRAME)
    raw_sharpe = util.get_sharpe_ratio(merged_raw_df, const.WEALTH_DATAFRAME)

    util.draw_histogram(data_series=raw_sharpe.dropna(),
                        xlabel='Raw Strategy Sharpe Ratio',
                        ylabel='Strategies Number', title='Histogram of Raw Strategy Sharpe Ratio',
                        save_path=os.path.join(result_path, 'raw_sharpe_ratio_histogram_{}.png'.format(tag)))

    util.draw_histogram(data_series=raw_return.dropna(),
                        xlabel='Raw Strategy Annualized Return',
                        ylabel='Strategies Number', title='Histogram of Raw Strategy Annualized Return',
                        save_path=os.path.join(result_path, 'raw_ann_return_histogram_{}.png'.format(tag)))

    util.draw_histogram(data_series=alpha_return.dropna(),
                        xlabel='Alpha Strategy Annualized Return',
                        ylabel='Strategies Number', title='Histogram of Alpha Strategy Annualized Return',
                        save_path=os.path.join(result_path, 'alpha_ann_return_histogram_{}.png'.format(tag)))
    #
    util.draw_histogram(data_series=alpha_sharpe.dropna(),
                        xlabel='Alpha Strategy Sharpe Ratio',
                        ylabel='Strategies Number', title='Histogram of Alpha Strategy Sharpe Ratio',
                        save_path=os.path.join(result_path, 'alpha_sharpe_ratio_histogram_{}.png'.format(tag)))


if __name__ == '__main__':
    import datetime

    from xvfbwrapper import Xvfb

    vdisplay = Xvfb(width=1366, height=768)
    vdisplay.start()

    plot_histogram_of_target_time_period(os.path.join(const.RESULT_PATH, 'insider_exe_gt2'),
                                         start_date=datetime.datetime(2016, 2, 1),
                                         tag='after_16')

    plot_histogram_of_target_time_period(os.path.join(const.RESULT_PATH, 'insider_exe_gt2'),
                                         start_date=datetime.datetime(2013, 7, 22),
                                         end_date=datetime.datetime(2016, 7, 20),
                                         tag='13_16')

    plot_histogram_of_target_time_period(os.path.join(const.RESULT_PATH, 'forecast_report_stock_20170214'),
                                         start_date=datetime.datetime(2016, 2, 1),
                                         tag='after_16')

    plot_histogram_of_target_time_period(os.path.join(const.RESULT_PATH, 'forecast_report_stock_20170214'),
                                         start_date=datetime.datetime(2013, 7, 22),
                                         end_date=datetime.datetime(2016, 7, 20),
                                         tag='13_16')

    vdisplay.stop()
