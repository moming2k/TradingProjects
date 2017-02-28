#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: path_info
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from ..util_functions.os_related import get_root_path

root_path = get_root_path()
temp_path = os.path.join(root_path, 'temp')
data_path = os.path.join(root_path, 'data')
result_path = os.path.join(root_path, 'result')

stock_path = os.path.join(data_path, 'stock_price_data')
stock_price_path = os.path.join(stock_path, 'stock_price')
stock_20170117_path = os.path.join(stock_path, 'stock_price_20170117')
original_new_data = os.path.join(stock_20170117_path, 'original_data')
minute_level_data_path = os.path.join(stock_20170117_path, 'minute_level')
daily_level_data_path = os.path.join(stock_20170117_path, 'daily_level')
daily_ticker_sep_path = os.path.join(daily_level_data_path, 'ticker_sep')
daily_date_sep_path = os.path.join(daily_level_data_path, 'date_sep')
stock_20170214_path = os.path.join(stock_path, 'stock_price_20170214', 'daily_sep')

report_path = os.path.join(data_path, 'report_data')
buy_only_report_data_path = os.path.join(report_path, 'report_info_buy_only')
buy_only_return_path = os.path.join(report_path, 'buy_only_return_path')
report_20170205_path = os.path.join(report_path, 'report_data_20170205')
report_20170214_path = os.path.join(report_path, 'report_data_20170214')

trading_days_path = os.path.join(data_path, 'trading_days_list')
trading_days_20170108_path = os.path.join(trading_days_path, 'trading_days_20170108.p')
trading_days_20170131_path = os.path.join(trading_days_path, 'trading_days_20170131.p')


class Path(object):
    ROOT_PATH = get_root_path()
    TEMP_PATH = os.path.join(ROOT_PATH, 'temp')
    DATA_PATH = os.path.join(ROOT_PATH, 'data')
    RESULT_PATH = os.path.join(ROOT_PATH, 'result')

    REPORT_DATA_PATH = os.path.join(DATA_PATH, 'report_data')
    STOCK_DATA_PATH = os.path.join(DATA_PATH, 'stock_price_data')

    STOCK_PRICE_20170214_PATH = os.path.join(DATA_PATH, 'stock_price_data', 'stock_price_20170214', 'daily_sep')

    REPORT_20170214_PATH = os.path.join(REPORT_DATA_PATH, 'report_data_20170214')
    REPORT_20170228_PATH = os.path.join(REPORT_DATA_PATH, 'report_data_20170228')

    INSIDER_EXE_GT2_PATH = os.path.join(REPORT_20170228_PATH, 'insider_exe_gt_2')
    INSIDER_REPORT_PATH = os.path.join(REPORT_DATA_PATH, 'report_info_buy_only')

    SZ_399300_PATH = os.path.join(STOCK_DATA_PATH, 'index_date', '399300_daily.p')

    # The longest trading days list from 1990 to 2017
    TRADING_DAYS_20170214_PATH = os.path.join(DATA_PATH, 'trading_days_list', 'trading_days_20170214.p')

    # This trading days list only cover 399300.SZ date
    TRADING_DAYS_20170216_PATH = os.path.join(DATA_PATH, 'trading_days_list', 'trading_days_20170216.p')
    TRADING_DAYS_20170228_PATH = os.path.join(DATA_PATH, 'trading_days_list', 'trading_days_20170228.p')


if __name__ == '__main__':
    from ChineseStock.src.util_functions.util_function import plot_picture

    path = '/Users/warn/PycharmProjects/QuestionFromProfWang/ChineseStock/result'
    path = os.path.join(path, 'buy_only_no_cost_no_down')
    wealth_df = pd.read_pickle(os.path.join(path, '20170129_only_buy_no_cost_no_drawdown_wealth.p'))
    plot_picture(wealth_df['exe_self_5p_14d'], 'exe_self_5p_14d', os.path.join(path, 'test.png'))
