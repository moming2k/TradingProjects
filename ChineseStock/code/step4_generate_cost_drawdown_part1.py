#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step4_generate_cost_drawdown
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

#
# import os
# import datetime
#
# from os_related import get_process_num
# from path_info import temp_path, result_path
# from util_function import merge_result
# from calculate_return_utils_2 import calculate_return_and_wealth, generate_result_statistics
# from constants import portfolio_num_range, holding_days_list, info_type_list, Constant, transaction_cost_list
#
# wealth_path = os.path.join(temp_path, 'buy_only_cost_draw_wealth')
# return_path = os.path.join(temp_path, 'buy_only_cost_draw_return')
# save_path = os.path.join(result_path, 'buy_only_cost_down')
#
# if not os.path.isdir(wealth_path):
#     os.makedirs(wealth_path)
#
# if not os.path.isdir(return_path):
#     os.makedirs(return_path)
#
# if not os.path.isdir(save_path):
#     os.makedirs(save_path)
#
# if __name__ == '__main__':
#     import multiprocessing
#
#     const = Constant()
#     process_num = get_process_num()
#
#     draw_down_rate = -0.05
#
#     # define some parameters
#     portfolio_info = []
#     for portfolio_num in portfolio_num_range:
#         for holding_days in holding_days_list:
#             for transaction_cost in transaction_cost_list:
#                 portfolio_info.append({const.PORTFOLIO_NUM: portfolio_num, const.HOLDING_DAYS: holding_days,
#                                        const.TRANSACTION_COST: transaction_cost, const.REPORT_RETURN_PATH: return_path,
#                                        const.WEALTH_DATA_PATH: wealth_path, const.DRAWDOWN_RATE: draw_down_rate})
#
#     pool = multiprocessing.Pool(process_num)
#     for info_type in info_type_list:
#         print datetime.datetime.today(), 'info type: {}'.format(info_type)
#
#
#         def change_info_type(x):
#             x[const.INFO_TYPE] = info_type
#             return x
#
#
#         new_portfolio_info = map(change_info_type, portfolio_info)
#
#         pool.map(calculate_return_and_wealth, new_portfolio_info)
#         print datetime.datetime.today(), 'info type {} processed finished'.format(info_type)
#
#     print datetime.datetime.today(), 'all info type processed finished, start generate result'
#     result = merge_result(wealth_path)
#     today_str = datetime.datetime.today().strftime('%Y%m%d')
#     result.to_pickle(os.path.join(save_path,
#                                   '{}_only_buy_cost_{}drawdown_wealth.p'.format(today_str,
#                                                                                 int(abs(100 * draw_down_rate)))))
#
#     statistic_df, best_strategy_df = generate_result_statistics(result)
#     statistic_df.to_pickle(os.path.join(save_path, '{}_statistic_{}.p'.format(today_str,
#                                                                               int(abs(100 * draw_down_rate)))))
#     best_strategy_df.to_pickle(os.path.join(save_path, '{}_best_strategies_{}.p'.format(today_str,
#                                                                                         int(abs(
#                                                                                             100 * draw_down_rate)))))
#     statistic_df.to_csv(os.path.join(save_path, '{}_statistic_{}.csv'.format(today_str,
#                                                                              int(abs(100 * draw_down_rate)))))
#     best_strategy_df.to_csv(os.path.join(save_path, '{}_best_strategies_{}.csv'.format(today_str,
#                                                                                        int(abs(100 * draw_down_rate)))))

import os

from calculate_return_utils_2 import generate_cost_return_info
from constants import stop_loss_rate_range

if __name__ == '__main__':
    transaction_cost = 0.005

    if hasattr(os, 'uname'):

        from xvfbwrapper import Xvfb

        vdisplay = Xvfb(width=1366, height=768)
        vdisplay.start()

        for stop_loss_rate in stop_loss_rate_range:
            generate_cost_return_info(transaction_cost=transaction_cost, stop_loss_rate=stop_loss_rate)

        vdisplay.stop()

    else:
        for stop_loss_rate in stop_loss_rate_range:
            generate_cost_return_info(transaction_cost=transaction_cost, stop_loss_rate=stop_loss_rate)
