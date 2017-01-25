#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: test_step2
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

from os_related import get_process_num
from path_info import temp_path, result_path
from util_function import merge_result
from calculate_return_utils import generate_buy_only_return_df_add_drawback, calculate_portfolio_return
from constants import portfolio_num_range, holding_days_list, info_type_list, Constant, drawdown_rate_range

wealth_path = os.path.join(temp_path, 'buy_only_drawdown_wealth')
return_path = os.path.join(temp_path, 'buy_only_drawdown_return')

if not os.path.isdir(wealth_path):
    os.makedirs(wealth_path)

if not os.path.isdir(return_path):
    os.makedirs(return_path)

if __name__ == '__main__':
    import multiprocessing

    const = Constant()
    process_num = get_process_num()

    # define some parameters
    portfolio_info = []
    for portfolio_num in portfolio_num_range:
        for holding_days in holding_days_list:
            for drawdown_rate in drawdown_rate_range:
                portfolio_info.append({const.PORTFOLIO_NUM: portfolio_num, const.HOLDING_DAYS: holding_days,
                                       const.DRAWDOWN_RATE: drawdown_rate})

    # for info_type in info_type_list:
    #     print datetime.datetime.today(), 'info type: {}'.format(info_type)

    info_type = 'all'

    def calculate_return_and_wealth(info):
        const = Constant()
        portfolio_num = info[const.PORTFOLIO_NUM]
        holding_days = info[const.HOLDING_DAYS]

        return_df = generate_buy_only_return_df_add_drawback(return_path, holding_days, info_type=info_type,
                                                             drawback_rate=info[const.DRAWDOWN_RATE])

        wealth_df = calculate_portfolio_return(return_df, portfolio_num)
        wealth_df.to_pickle(
            os.path.join(wealth_path, '{}_{}p_{}d.p'.format(info_type, portfolio_num, holding_days)))
        wealth_df.to_csv(
            os.path.join(wealth_path, '{}_{}p_{}d.csv'.format(info_type, portfolio_num, holding_days)),
            encoding='utf8')

        return wealth_df

    calculate_return_and_wealth(portfolio_info[0])
        # pool = multiprocessing.Pool(process_num)
        # pool.map(calculate_return_and_wealth, portfolio_info)
        # pool.close()
        # print datetime.datetime.today(), 'info type {} processed finished'.format(info_type)

    print datetime.datetime.today(), 'all info type processed finished, start generate result'
    # result = merge_result(wealth_path)
    # today_str = datetime.datetime.today().strftime('%Y%m%d')
    # result.to_pickle(os.path.join(result_path,
    #                               '{}_only_buy_no_cost_drawdown.p'.format(today_str)))