#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step14_generate_si_anndate
# @Date: 2017-02-12
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os
import datetime
import multiprocessing

from os_related import get_process_num, make_dirs
from path_info import temp_path, result_path, data_path
from constants import holding_days_list, portfolio_num_range
from constants import Constant as const
from calculate_return_utils_20170117_data import generate_result_statistics, generate_buy_only_return_df, \
    calculate_portfolio_return
from util_function import print_info, merge_result, plot_picture, get_max_draw_down

transaction_cost = 0.002
suffix = 'si_anndate'
report_path = os.path.join(data_path, 'report_data_20170205', 'si_anndate')


def calculate_return_and_wealth(info):
    portfolio_num = info[const.PORTFOLIO_NUM]
    holding_days = info[const.HOLDING_DAYS]
    info_type = info[const.INFO_TYPE]
    return_path = info[const.REPORT_RETURN_PATH]
    wealth_path = info[const.WEALTH_DATA_PATH]

    file_name = '{}_{}p_{}d'.format(info_type, portfolio_num, holding_days)

    try:
        if const.TRANSACTION_COST in info:
            transaction_cost = info[const.TRANSACTION_COST]
            file_name = '{}_{}cost'.format(file_name, int(transaction_cost * 1000))
        else:
            transaction_cost = 0

        if const.STOPLOSS_RATE in info:
            stoploss_rate = info[const.STOPLOSS_RATE]
            file_name = '{}_{}stoploss'.format(file_name, int(abs(stoploss_rate) * 100))
        else:
            stoploss_rate = None

        report_df = generate_buy_only_return_df(return_path, holding_days, info_type=info_type,
                                                drawback_rate=stoploss_rate, report_path=report_path)

        try:
            wealth_df = calculate_portfolio_return(report_df, portfolio_num, transaction_cost=transaction_cost)

        except Exception, err:
            print 'Error happend during generate wealth own_report_df'
            raise Exception(err)

        wealth_df.to_pickle(os.path.join(wealth_path, '{}.p'.format(file_name)))
    except Exception, err:
        import traceback
        traceback.print_exc()

        print info

        raise Exception(err)

    return wealth_df


def based_on_stop_loss_rate_generate_result(stop_loss_rate, folder_suffix):
    process_num = get_process_num()

    stop_loss_str = str(int(100 * abs(stop_loss_rate)))
    transaction_cost_str = str(int(1000 * transaction_cost))

    wealth_path = os.path.join(temp_path, 'cost_{}_stop_loss_{}_{}_wealth'.format(transaction_cost_str, stop_loss_str,
                                                                                  folder_suffix))
    save_path = os.path.join(result_path, folder_suffix, 'cost_{}_stop_loss_{}'.format(transaction_cost_str,
                                                                                       stop_loss_str))
    report_path = os.path.join(temp_path, 'cost_{}_stop_loss_{}_{}_report'.format(transaction_cost_str, stop_loss_str,
                                                                                  folder_suffix))
    picture_save_path = os.path.join(save_path, 'picture')
    better_picture_save_path = os.path.join(save_path, 'picture_1_5')
    best_picture_save_path = os.path.join(save_path, 'picture_2')

    make_dirs(
        [wealth_path, save_path, report_path, picture_save_path, better_picture_save_path, best_picture_save_path])

    # define some parameters
    portfolio_info = []
    for portfolio_num in portfolio_num_range:
        for holding_days in holding_days_list:
            portfolio_info.append({const.PORTFOLIO_NUM: portfolio_num, const.HOLDING_DAYS: holding_days,
                                   const.TRANSACTION_COST: transaction_cost, const.REPORT_RETURN_PATH: report_path,
                                   const.WEALTH_DATA_PATH: wealth_path, const.STOPLOSS_RATE: stop_loss_rate})

    pool = multiprocessing.Pool(process_num)
    for info_type in ['all']:
        print_info('info type: {}'.format(info_type))

        def change_info_type(x):
            x[const.INFO_TYPE] = info_type
            return x

        new_portfolio_info = map(change_info_type, portfolio_info)

        pool.map(calculate_return_and_wealth, new_portfolio_info)
        print_info('info type {} processed finished'.format(info_type))

    print_info('all info type processed finished, start generate result')
    wealth_result = merge_result(wealth_path)
    today_str = datetime.datetime.today().strftime('%Y%m%d')
    wealth_result.to_pickle(os.path.join(save_path,
                                         '{}_stoploss_{}.p'.format(today_str, stop_loss_str)))
    wealth_result.to_csv(os.path.join(save_path,
                                      '{}_stoploss_{}.csv'.format(today_str, stop_loss_str)))

    statistic_df, best_strategy_df, sharpe_ratio, ann_return = generate_result_statistics(wealth_result)
    statistic_df.to_pickle(os.path.join(save_path, '{}_statistic_{}.p'.format(today_str, stop_loss_str)))
    best_strategy_df.to_pickle(os.path.join(save_path, '{}_best_strategies_{}.p'.format(today_str, stop_loss_str)))
    statistic_df.to_csv(os.path.join(save_path, '{}_statistic_{}.csv'.format(today_str, stop_loss_str)))
    best_strategy_df.to_csv(os.path.join(save_path, '{}_best_strategies_{}.csv'.format(today_str, stop_loss_str)))

    pool.close()

    for method in wealth_result.keys():
        if sharpe_ratio[method] > 2:
            pic_path = best_picture_save_path
        elif sharpe_ratio[method] > 1.5:
            pic_path = better_picture_save_path
        else:
            pic_path = picture_save_path

        max_draw_down = get_max_draw_down(wealth_result[method])
        text = 'Sharpe ratio: {:.3f}, Annualized return: {:.2f}%'.format(sharpe_ratio[method],
                                                                         ann_return[method] * 100)

        text = '{}, Max drawdown rate: {:.2f}%, stop loss rate: {}%'.format(text, max_draw_down * 100,
                                                                            stop_loss_rate * 100)
        text = '{}, Transaction cost: 0.2%'.format(text)
        plot_picture(wealth_result[method], method, os.path.join(pic_path, '{}.png'.format(method)), text)


if __name__ == '__main__':

    import numpy as np

    if hasattr(os, 'uname'):

        from xvfbwrapper import Xvfb

        vdisplay = Xvfb(width=1366, height=768)
        vdisplay.start()

        for stop_loss_rate in np.arange(-0.05, 0.001, 0.01):
            based_on_stop_loss_rate_generate_result(stop_loss_rate, suffix)

        vdisplay.stop()

    else:

        for stop_loss_rate in np.arange(-0.05, 0.001, 0.01):
            based_on_stop_loss_rate_generate_result(stop_loss_rate, suffix)
