#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step4_generate_buy_only_all
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

from constant import Constant, portfolio_num_range, holding_days_list, info_type_list
from util_functions import generate_buy_only_return_df, calculate_portfolio_return
from get_root_path import data_path, temp_path, process_num

wealth_path = os.path.join(temp_path, 'buy_only_wealth')
return_path = os.path.join(temp_path, 'buy_only_return')

if __name__ == '__main__':
    import multiprocessing

    const = Constant()

    # define some parameters
    portfolio_info = []
    for portfolio_num in portfolio_num_range:
        for holding_days in holding_days_list:
            portfolio_info.append({const.PORTFOLIO_NUM: portfolio_num, const.HOLDING_DAYS: holding_days})

    for info_type in info_type_list:
        buy_only_report_data_path = os.path.join(data_path, 'report_info_buy_only')

        if not os.path.isdir(buy_only_report_data_path):
            os.makedirs(buy_only_report_data_path)

        if not os.path.isdir(return_path):
            os.makedirs(return_path)

        if not os.path.isdir(wealth_path):
            os.makedirs(wealth_path)


        def calculate_return_and_wealth_all(info):
            const = Constant()
            portfolio_num = info[const.PORTFOLIO_NUM]
            holding_days = info[const.HOLDING_DAYS]

            return_df = generate_buy_only_return_df(return_path, holding_days, info_type=info_type)

            wealth_df = calculate_portfolio_return(return_df, portfolio_num)
            wealth_df.to_pickle(
                os.path.join(wealth_path, '{}_{}_port_{}d.p'.format(info_type, portfolio_num, holding_days)))
            wealth_df.to_csv(
                os.path.join(wealth_path, '{}_{}_port_{}d.csv'.format(info_type, portfolio_num, holding_days)),
                encoding='utf8')

            return wealth_df


        pool = multiprocessing.Pool(process_num)
        pool.map(calculate_return_and_wealth_all, portfolio_info)
        pool.close()
