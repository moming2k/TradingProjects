#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: path_info
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from os_related import get_root_path

root_path = get_root_path()
temp_path = os.path.join(root_path, 'temp')
data_path = os.path.join(root_path, 'data')
result_path = os.path.join(root_path, 'result')
stock_price_path = os.path.join(data_path, 'stock_price')
buy_only_report_data_path = os.path.join(data_path, 'report_info_buy_only')

# trading_day_list = pd.read_pickle(os.path.join(data_path, 'trading_days_list.p'))

# the following path are used in 20170127 data
new_stock_data_path = os.path.join(data_path, '20170117_new_data')
original_new_data = os.path.join(new_stock_data_path, 'original_data')
minute_level_data_path = os.path.join(new_stock_data_path, 'minute_level')
daily_level_data_path = os.path.join(new_stock_data_path, 'daily_level')
daily_ticker_sep_path = os.path.join(daily_level_data_path, 'ticker_sep')
daily_date_sep_path = os.path.join(daily_level_data_path, 'date_sep')


if __name__ == '__main__':
    from util_function import plot_picture

    path = '/Users/warn/PycharmProjects/QuestionFromProfWang/ChineseStock/result'
    path = os.path.join(path, 'buy_only_no_cost_no_down')
    wealth_df = pd.read_pickle(os.path.join(path, '20170129_only_buy_no_cost_no_drawdown_wealth.p'))
    plot_picture(wealth_df['exe_self_5p_14d'], 'exe_self_5p_14d', os.path.join(path, 'test.png'))
