#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step6_draw_portfolio_num_gt20
# @Date: 2017-03-30
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


def get_sub_df(df, start_date=None, end_date=None, portfolio_num=None):
    if start_date is not None:
        sub_df = df[df.index >= start_date]

    else:
        sub_df = df.copy()

    if end_date is not None:
        sub_df = sub_df[sub_df.index <= end_date]

    if portfolio_num is not None:
        key_df = pd.DataFrame(sub_df.keys(), columns=['key'])
        key_df['portfolio_num'] = key_df['key'].apply(lambda x: int(x.split('_')[1][:-1]))
        key_df = key_df[key_df['portfolio_num'] >= portfolio_num]
        sub_df = sub_df[key_df['key']]

    return sub_df


def get_alpha_raw_df(result_path, portfolio_lower_bound):
    file_list = os.listdir(result_path)

    alpha_df_list = []
    raw_df_list = []

    for dir_file in file_list:
        if not os.path.isdir(os.path.join(result_path, dir_file)):
            continue

        current_path = os.path.join(result_path, dir_file)

        alpha_file_name = util.get_target_file_name(current_path, 'sr_alpha', '.p')
        raw_file_name = util.get_target_file_name(current_path, 'sr_raw', '.p')

        alpha_df = get_sub_df(pd.read_pickle(os.path.join(current_path, alpha_file_name)),
                              portfolio_num=portfolio_lower_bound)
        raw_df = get_sub_df(pd.read_pickle(os.path.join(current_path, raw_file_name)),
                            portfolio_num=portfolio_lower_bound)

        alpha_df_list.append(alpha_df)
        raw_df_list.append(raw_df)

    merged_alpha_df = pd.concat(alpha_df_list, axis=1)
    merged_raw_df = pd.concat(raw_df_list, axis=1)

    return merged_alpha_df, merged_raw_df


if __name__ == '__main__':
    import datetime

    from xvfbwrapper import Xvfb

    portfolio_lower_bound = 20

    vdisplay = Xvfb(width=1366, height=768)

    info_list = [{'start': None,
                  'end': None,
                  'tag': 'all'},
                 {'start': datetime.datetime(2016, 2, 1),
                  'end': None,
                  'tag': 'after_16'},
                 {'start': datetime.datetime(2013, 7, 22),
                  'end': datetime.datetime(2016, 7, 20),
                  'tag': '13_16'},
                 {'start': datetime.datetime(2009, 1, 1),
                  'end': datetime.datetime(2015, 1, 1),
                  'tag': '09_14'},
                 ]

    result_path_list = [os.path.join(const.RESULT_PATH, 'insider_exe_gt2'),
                        os.path.join(const.RESULT_PATH, 'forecast_report_stock_20170214')]

    vdisplay.start()

    for result_path in result_path_list:
        alpha_df, raw_df = get_alpha_raw_df(result_path, portfolio_lower_bound)

        save_path = os.path.join(result_path, 'p{}'.format(portfolio_lower_bound))

        if not os.path.isdir(save_path):
            os.makedirs(save_path)

        for info in info_list:
            tag = '{}_{}p'.format(info['tag'], portfolio_lower_bound)
            sub_alpha_df = get_sub_df(alpha_df, info['start'], info['end'])
            sub_raw_df = get_sub_df(raw_df, info['start'], info['end'])

            alpha_return = util.get_annualized_return(sub_alpha_df, const.WEALTH_DATAFRAME)
            raw_return = util.get_annualized_return(sub_raw_df, const.WEALTH_DATAFRAME)

            alpha_sharpe = util.get_sharpe_ratio(sub_alpha_df, const.WEALTH_DATAFRAME)
            raw_sharpe = util.get_sharpe_ratio(sub_raw_df, const.WEALTH_DATAFRAME)

            util.draw_histogram(data_series=raw_sharpe.dropna(),
                                xlabel='Raw Strategy Sharpe Ratio',
                                ylabel='Strategies Number', title='Histogram of Raw Strategy Sharpe Ratio',
                                save_path=os.path.join(save_path, 'raw_sharpe_ratio_histogram_{}.png'.format(tag)))

            util.draw_histogram(data_series=raw_return.dropna(),
                                xlabel='Raw Strategy Annualized Return',
                                ylabel='Strategies Number', title='Histogram of Raw Strategy Annualized Return',
                                save_path=os.path.join(save_path, 'raw_ann_return_histogram_{}.png'.format(tag)))

            util.draw_histogram(data_series=alpha_return.dropna(),
                                xlabel='Alpha Strategy Annualized Return',
                                ylabel='Strategies Number', title='Histogram of Alpha Strategy Annualized Return',
                                save_path=os.path.join(save_path, 'alpha_ann_return_histogram_{}.png'.format(tag)))
            #
            util.draw_histogram(data_series=alpha_sharpe.dropna(),
                                xlabel='Alpha Strategy Sharpe Ratio',
                                ylabel='Strategies Number', title='Histogram of Alpha Strategy Sharpe Ratio',
                                save_path=os.path.join(save_path, 'alpha_sharpe_ratio_histogram_{}.png'.format(tag)))

            alpha_return_max = alpha_return.idxmax()

            stop_loss_rate = re.findall(r'\d+', alpha_return_max)[-1]

            util._plot_multiline_picture_text(alpha_return_max, [raw_df[alpha_return_max], alpha_df[alpha_return_max]],
                                              ['Raw Strategy', 'Alpha Strategy'],
                                              save_path=os.path.join(save_path,
                                                                     'best_alpha_return_{}.png'.format(tag)),
                                              stop_loss_rate=stop_loss_rate)

            raw_return_max = raw_return.idxmax()

            stop_loss_rate = re.findall(r'\d+', raw_return_max)[-1]

            util._plot_multiline_picture_text(raw_return_max, [raw_df[raw_return_max], alpha_df[raw_return_max]],
                                              ['Raw Strategy', 'Alpha Strategy'],
                                              save_path=os.path.join(save_path,
                                                                     'best_raw_return_{}.png'.format(tag)),
                                              stop_loss_rate=stop_loss_rate)

    vdisplay.stop()
