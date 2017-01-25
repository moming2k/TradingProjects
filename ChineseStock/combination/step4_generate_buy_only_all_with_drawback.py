#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step4_generate_buy_only_all_with_drawback
# @Date: 2017-01-24
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os

from constant import Constant, drawdown_rate_range, holding_days_list, portfolio_num_range
from util_functions import calculate_portfolio_return
from draw_down_util import generate_buy_only_return_df_add_drawback
from get_root_path import data_path, temp_path, process_num

info_type = 'all'

wealth_path = os.path.join(temp_path, 'buy_only_wealth_{}'.format(info_type))
return_path = os.path.join(temp_path, 'buy_only_return_{}'.format(info_type))
buy_only_report_data_path = os.path.join(data_path, 'report_info_with_drawdown')

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
    draw_down = info[const.DRAWDOWN_RATE]

    return_df = generate_buy_only_return_df_add_drawback(return_path, holding_days, info_type=info_type,
                                                         drawback_rate=draw_down)

    wealth_df = calculate_portfolio_return(return_df, portfolio_num)
    wealth_df.to_pickle(
        os.path.join(wealth_path, 'buy_only_{}_{}port_{}d_{}draw.p'.format(info_type, portfolio_num, holding_days,
                                                                           int(100 * abs(draw_down)))))
    wealth_df.to_csv(
        os.path.join(wealth_path, 'buy_only_{}_{}port_{}d_{}draw.csv'.format(info_type, portfolio_num, holding_days,
                                                                             int(100 * abs(draw_down)))),
        encoding='utf8')

    return wealth_df


if __name__ == '__main__':
    import multiprocessing

    const = Constant()

    portfolio_info = []
    for portfolio_num in portfolio_num_range:
        for holding_days in holding_days_list:
            for draw_down in drawdown_rate_range:
                portfolio_info.append({const.PORTFOLIO_NUM: portfolio_num, const.HOLDING_DAYS: holding_days,
                                       const.DRAWDOWN_RATE: draw_down})

    pool = multiprocessing.Pool(process_num)

    pool.map(calculate_return_and_wealth_all, portfolio_info)
