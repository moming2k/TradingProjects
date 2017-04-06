#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step8_draw_historgram_and_other_picture
# @Date: 2017-04-06
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import re

import pandas as pd

from ..constants.constants import Constant as const
from ..report_generator.report_generator_add_max_drawdown_limit import ReportGenerator

transaction_cost = 0.002
max_draw_down_limit = float('inf')
suffix = 'insider_exe_gt2'
report_path = const.INSIDER_EXE_GT2_RUN_UP_PATH

util = ReportGenerator(transaction_cost=transaction_cost, report_path=report_path,
                       folder_suffix=suffix, trading_days_list_path=const.TRADING_DAYS_20170228_PATH,
                       stock_price_path=const.STOCK_PRICE_20170214_PATH)


def get_sub_df(df, start_date=None, end_date=None):
    if start_date is not None:
        sub_df = df[df.index >= start_date]

    else:
        sub_df = df.copy()

    if end_date is not None:
        sub_df = sub_df[sub_df.index <= end_date]

    return sub_df


def plot_histogram_of_target_time_period(result_path, alpha_df, raw_df, start_date=None, end_date=None, tag=None):
    merged_alpha_df = get_sub_df(alpha_df, start_date, end_date)
    merged_raw_df = get_sub_df(raw_df, start_date, end_date)

    alpha_return = util.get_annualized_return(merged_alpha_df, const.WEALTH_DATAFRAME)
    raw_return = util.get_annualized_return(merged_raw_df, const.WEALTH_DATAFRAME)

    alpha_sharpe = util.get_sharpe_ratio(merged_alpha_df, const.WEALTH_DATAFRAME)
    raw_sharpe = util.get_sharpe_ratio(merged_raw_df, const.WEALTH_DATAFRAME)

    util.draw_histogram(data_series=raw_sharpe.dropna(),
                        xlabel='Raw Strategy Sharpe Ratio',
                        ylabel='Strategies Number', title='Histogram of Raw Strategy Sharpe Ratio',
                        save_path=os.path.join(result_path, '{}_raw_sharpe_histogram.png'.format(tag)))

    util.draw_histogram(data_series=raw_return.dropna(),
                        xlabel='Raw Strategy Annualized Return',
                        ylabel='Strategies Number', title='Histogram of Raw Strategy Annualized Return',
                        save_path=os.path.join(result_path, '{}_raw_ann_histogram.png'.format(tag)))

    util.draw_histogram(data_series=alpha_return.dropna(),
                        xlabel='Alpha Strategy Annualized Return',
                        ylabel='Strategies Number', title='Histogram of Alpha Strategy Annualized Return',
                        save_path=os.path.join(result_path, '{}_alpha_ann_histogram.png'.format(tag)))
    #
    util.draw_histogram(data_series=alpha_sharpe.dropna(),
                        xlabel='Alpha Strategy Sharpe Ratio',
                        ylabel='Strategies Number', title='Histogram of Alpha Strategy Sharpe Ratio',
                        save_path=os.path.join(result_path, '{}_alpha_sharpe_histogram.png'.format(tag)))

    alpha_return_max = alpha_return.idxmax()

    stop_loss_rate = re.findall(r'\d+', alpha_return_max)[-1]

    util._plot_multiline_picture_text(alpha_return_max, [raw_df[alpha_return_max], alpha_df[alpha_return_max]],
                                      ['Raw Strategy', 'Alpha Strategy'],
                                      save_path=os.path.join(result_path,
                                                             '{}_best_alpha_return.png'.format(tag)),
                                      stop_loss_rate=stop_loss_rate)

    raw_return_max = raw_return.idxmax()

    stop_loss_rate = re.findall(r'\d+', raw_return_max)[-1]

    util._plot_multiline_picture_text(raw_return_max, [raw_df[raw_return_max], alpha_df[raw_return_max]],
                                      ['Raw Strategy', 'Alpha Strategy'],
                                      save_path=os.path.join(result_path,
                                                             '{}_best_raw_return.png'.format(tag)),
                                      stop_loss_rate=stop_loss_rate)


if __name__ == '__main__':
    import datetime
    from xvfbwrapper import Xvfb

    result_path = os.path.join(const.RESULT_PATH, 'forecast_run_up_stock_data_20170214', 'result')

    data_path = os.path.join(const.RESULT_PATH, 'forecast_run_up_stock_data_20170214')
    #
    # alpha_df_list = []
    # raw_df_list = []
    #
    # dir_list = os.listdir(data_path)
    #
    # for dir_name in dir_list:
    #     if not dir_name.startswith('cost'):
    #         continue
    #
    #     current_path = os.path.join(data_path, dir_name)
    #
    #     if not os.path.isdir(current_path):
    #         continue
    #
    #     raw_file = util.get_target_file_name(current_path, 'raw', '.p')
    #     alpha_file = util.get_target_file_name(current_path, 'alpha', '.p')
    #
    #     alpha_df_list.append(pd.read_pickle(os.path.join(current_path, alpha_file)))
    #     raw_df_list.append(pd.read_pickle(os.path.join(current_path, raw_file)))
    #
    # alpha_df = pd.concat(alpha_df_list, axis=1)
    # raw_df = pd.concat(raw_df_list, axis=1)
    #
    # raw_df.to_pickle(os.path.join(result_path, 'raw_data.p'))
    # raw_df.to_csv(os.path.join(result_path, 'raw_data.csv'))
    # alpha_df.to_pickle(os.path.join(result_path, 'alpha_data.p'))
    # alpha_df.to_csv(os.path.join(result_path, 'alpha_data.csv'))
    alpha_df = pd.read_pickle(os.path.join(result_path, 'alpha_data.p'))
    raw_df = pd.read_pickle(os.path.join(result_path, 'raw_data.p'))

    vdisplay = Xvfb(width=1366, height=768)
    vdisplay.start()

    plot_histogram_of_target_time_period(result_path=result_path, alpha_df=alpha_df, raw_df=raw_df,
                                         # start_date=datetime.datetime(2016, 2, 1),
                                         tag='all')

    plot_histogram_of_target_time_period(result_path=result_path, alpha_df=alpha_df, raw_df=raw_df,
                                         start_date=datetime.datetime(2009, 1, 1),
                                         end_date=datetime.datetime(2015, 1, 1),
                                         tag='09_14')

    plot_histogram_of_target_time_period(result_path=result_path, alpha_df=alpha_df, raw_df=raw_df,
                                         start_date=datetime.datetime(2016, 2, 1),
                                         tag='after_16')

    plot_histogram_of_target_time_period(result_path=result_path, alpha_df=alpha_df, raw_df=raw_df,
                                         start_date=datetime.datetime(2013, 7, 22),
                                         end_date=datetime.datetime(2016, 7, 20),
                                         tag='13_16')

    vdisplay.stop()
