#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: calculate_combination_buy_only_company
# @Date: 2017-01-15
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

from constant import Constant as const
from util_functions import generate_buy_only_return_df, calculate_portfolio_return
from get_root_path import temp_path, data_path

info_type = 'company'

wealth_path = os.path.join(temp_path, 'buy_only_wealth_{}'.format(info_type))
return_path = os.path.join(temp_path, 'buy_only_return_{}'.format(info_type))
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

    return_df = generate_buy_only_return_df(return_path, holding_days, info_type=info_type)

    wealth_df = calculate_portfolio_return(return_df, portfolio_num)
    wealth_df.to_pickle(
        os.path.join(wealth_path, 'buy_only_{}_{}_port_{}d.p'.format(info_type, portfolio_num, holding_days)))
    wealth_df.to_csv(
        os.path.join(wealth_path, 'buy_only_{}_{}_port_{}d.csv'.format(info_type, portfolio_num, holding_days)),
        encoding='utf8')

    return wealth_df


if __name__ == '__main__':
    # calculate_return_and_wealth_all({const.PORTFOLIO_NUM: 5, const.HOLDING_DAYS: 11})

    import pathos

    process_num = 30

    portfolio_info = []
    for portfolio_num in range(5, 101, 5):
        for holding_days in [3, 5, 10, 22, 33, 44, 55, 66, 77, 88, 99, 110]:
            portfolio_info.append({const.PORTFOLIO_NUM: portfolio_num, const.HOLDING_DAYS: holding_days})

    pool = pathos.multiprocessing.ProcessingPool(process_num)

    pool.map(calculate_return_and_wealth_all, portfolio_info)
