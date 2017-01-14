#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: calculate_combination
# @Date: 2017-01-13
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd

from constant import Constant as const
from test_function import generate_buy_only_return_df, calculate_portfolio_return

today_str = datetime.datetime.today().strftime('%Y%m%d')

root_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'
data_path = os.path.join(root_path, 'data')
temp_path = os.path.join(root_path, 'temp')
today_path = os.path.join(temp_path, today_str)
wealth_path = os.path.join(today_path, 'wealth')
return_path = os.path.join(today_path, 'buy_only_return')
stock_data_path = os.path.join(data_path, 'stock_price')
buy_only_report_data_path = os.path.join(data_path, 'report_info_buy_only')

if not os.path.isdir(today_path):
    os.makedirs(today_path)

if not os.path.isdir(buy_only_report_data_path):
    os.makedirs(buy_only_report_data_path)

if not os.path.isdir(return_path):
    os.makedirs(return_path)



trading_days = pd.read_pickle(os.path.join(data_path, 'trading_days_list.p'))


def calculate_return_and_wealth(info):
    portfolio_num = info[const.PORTFOLIO_NUM]
    holding_days = info[const.HOLDING_DAYS]

    return_df = generate_buy_only_return_df(return_path, holding_days)

    wealth_df = calculate_portfolio_return(return_df, portfolio_num)
    wealth_df.to_pickle(os.path.join(wealth_path, 'buy_only_all_{}_port_{}d.p'.format(portfolio_num, holding_days)))
    wealth_df.to_excel(os.path.join(wealth_path, 'buy_only_all_{}_port_{}d.xlsx'.format(portfolio_num, holding_days)))
    wealth_df.to_csv(os.path.join(wealth_path, 'buy_only_all_{}_port_{}d.csv'.format(portfolio_num, holding_days)),
                     encoding='utf8')

    return wealth_df
