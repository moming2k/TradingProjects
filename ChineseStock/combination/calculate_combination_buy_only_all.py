#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: calculate_combination_buy_only_all
# @Date: 2017-01-13
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

from constant import Constant as const
from constant import holding_days_list, portfolio_num_range
from util_functions import generate_buy_only_return_df, calculate_portfolio_return
from get_root_path import data_path, temp_path, process_num

wealth_path = os.path.join(temp_path, 'buy_only_wealth')
return_path = os.path.join(temp_path, 'buy_only_return')
buy_only_report_data_path = os.path.join(data_path, 'report_info_buy_only')

if not os.path.isdir(buy_only_report_data_path):
    os.makedirs(buy_only_report_data_path)

if not os.path.isdir(return_path):
    os.makedirs(return_path)

if not os.path.isdir(wealth_path):
    os.makedirs(wealth_path)


def calculate_return_and_wealth_all(info):
    portfolio_num = info[const.PORTFOLIO_NUM]
    holding_days = info[const.HOLDING_DAYS]

    return_df = generate_buy_only_return_df(return_path, holding_days)

    wealth_df = calculate_portfolio_return(return_df, portfolio_num)
    wealth_df.to_pickle(os.path.join(wealth_path, '{}_port_{}d.p'.format(portfolio_num, holding_days)))
    # raw_strategy_df.to_excel(os.path.join(wealth_path, 'buy_only_all_{}_port_{}d.xlsx'.format(portfolio_num, holding_days)))
    wealth_df.to_csv(os.path.join(wealth_path, '{}_port_{}d.csv'.format(portfolio_num, holding_days)),
                     encoding='utf8')

    return wealth_df


if __name__ == '__main__':
    # calculate_return_and_wealth_all({const.PORTFOLIO_NUM: 5, const.HOLDING_DAYS: 11})

    import multiprocessing

    portfolio_info = []
    for portfolio_num in portfolio_num_range:
        for holding_days in holding_days_list:
            portfolio_info.append({const.PORTFOLIO_NUM: portfolio_num, const.HOLDING_DAYS: holding_days})

    pool = multiprocessing.Pool(process_num)

    pool.map(calculate_return_and_wealth_all, portfolio_info)
