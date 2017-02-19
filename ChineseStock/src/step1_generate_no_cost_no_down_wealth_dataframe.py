#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step1_generate_no_cost_no_down_wealth_dataframe
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime
import os

from ChineseStock.src.calculate_return_utils.calculate_return_utils_2 import calculate_return_and_wealth, generate_result_statistics
from ChineseStock.src.constants.path_info import temp_path, result_path
from ChineseStock.src.util_functions.os_related import get_process_num
from ChineseStock.src.util_functions.util_function import merge_result
from constants import portfolio_num_range, holding_days_list, info_type_list, Constant

wealth_path = os.path.join(temp_path, 'buy_only_no_cost_no_draw_wealth')
return_path = os.path.join(temp_path, 'buy_only_no_cost_no_draw_return')
save_path = os.path.join(result_path, 'buy_only_no_cost_no_down')

if not os.path.isdir(wealth_path):
    os.makedirs(wealth_path)

if not os.path.isdir(return_path):
    os.makedirs(return_path)

if not os.path.isdir(save_path):
    os.makedirs(save_path)

if __name__ == '__main__':
    import multiprocessing

    from ChineseStock.src.util_functions.util_function import plot_picture

    const = Constant()
    process_num = get_process_num()

    # define some parameters
    portfolio_info = []
    for portfolio_num in portfolio_num_range:
        for holding_days in holding_days_list:
            portfolio_info.append({const.PORTFOLIO_NUM: portfolio_num, const.HOLDING_DAYS: holding_days,
                                   const.REPORT_RETURN_PATH: return_path,
                                   const.WEALTH_DATA_PATH: wealth_path})

    pool = multiprocessing.Pool(process_num)
    for info_type in info_type_list:
        print datetime.datetime.today(), 'info type: {}'.format(info_type)


        def change_info_type(x):
            x[const.INFO_TYPE] = info_type
            return x


        new_portfolio_info = map(change_info_type, portfolio_info)

        pool.map(calculate_return_and_wealth, new_portfolio_info)
        print datetime.datetime.today(), 'info type {} processed finished'.format(info_type)

    print datetime.datetime.today(), 'all info type processed finished, start generate result'
    result = merge_result(wealth_path)
    today_str = datetime.datetime.today().strftime('%Y%m%d')
    result.to_pickle(os.path.join(save_path,
                                  '{}_only_buy_no_cost_no_drawdown_wealth.p'.format(today_str)))

    statistic_df, best_strategy_df = generate_result_statistics(result)
    statistic_df.to_pickle(os.path.join(save_path, '{}_statistic.p'.format(today_str)))
    best_strategy_df.to_pickle(os.path.join(save_path, '{}_best_strategies.p'.format(today_str)))
    statistic_df.to_csv(os.path.join(save_path, '{}_statistic.csv'.format(today_str)))
    best_strategy_df.to_csv(os.path.join(save_path, '{}_best_strategies.csv'.format(today_str)))

    best_strategy_path = os.path.join(save_path, 'best_strategy')
    if not os.path.isdir(best_strategy_path):
        os.makedirs(best_strategy_path)

    for name in best_strategy_df['name']:
        plot_picture(result[name], name, os.path.join(best_strategy_path, '{}.png'.format(name)))
