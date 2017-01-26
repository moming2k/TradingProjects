#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step1_generate_no_cost_no_down_wealth_dataframe
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

from os_related import get_process_num
from path_info import temp_path, result_path
from util_function import merge_result
from calculate_return_utils import generate_buy_only_return_df, calculate_portfolio_return
from constants import portfolio_num_range, holding_days_list, info_type_list, Constant

import os
import datetime

from os_related import get_process_num
from path_info import temp_path, result_path
from util_function import merge_result
from calculate_return_utils_2 import calculate_return_and_wealth
from constants import portfolio_num_range, holding_days_list, info_type_list, Constant

wealth_path = os.path.join(temp_path, 'buy_only_no_cost_no_draw_wealth')
return_path = os.path.join(temp_path, 'buy_only_no_cost_no_draw_return')

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
            portfolio_info.append({const.PORTFOLIO_NUM: portfolio_num, const.HOLDING_DAYS: holding_days,
                                   const.REPORT_RETURN_PATH: return_path,
                                   const.WEALTH_DATA_PATH: wealth_path})

    pool = multiprocessing.Pool(process_num)
    for info_type in ['exe_parents', 'exe_self', 'exe_spouse']:
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
    result.to_pickle(os.path.join(result_path,
                                  '{}_only_buy_no_cost_no_drawdown_wealth.p'.format(today_str)))

    return_df = (result.shift(1) - result) / result
    return_df.to_pickle(os.path.join(result_path,
                                     '{}_only_buy_no_cost_no_drawdown_wealth.p'.format(today_str)))
