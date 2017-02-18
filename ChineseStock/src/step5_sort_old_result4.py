#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step5_sort_old_result4
# @Date: 2017-02-01
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd
from xvfbwrapper import Xvfb
from constants import Constant as const
from path_info import result_path
from os_related import make_dirs
from calculate_return_utils_2 import generate_result_statistics
from util_function import get_annualized_return, get_sharpe_ratio, plot_picture, get_max_draw_down

today_str = datetime.datetime.today().strftime('%Y%m%d')

path_list = ['buy_only_no_cost_no_down', 'buy_only_no_cost_down', 'buy_only_cost_no_down', 'buy_only_cost_down']

# sort zero result
dir_path = os.path.join(result_path, path_list[3])

file_list = ['20170131_only_buy_cost_1drawdown_wealth.p',
             '20170131_only_buy_cost_2drawdown_wealth.p',
             '20170129_only_buy_cost_3drawdown_wealth.p',
             '20170130_only_buy_cost_4drawdown_wealth.p',
             '20170131_only_buy_cost_5drawdown_wealth.p']

vdisplay = Xvfb(width=1366, height=768)
vdisplay.start()

for stop_loss in range(1, 6):

    print datetime.datetime.today(), 'stop loss {}'.format(stop_loss)

    wealth_df = pd.read_pickle(os.path.join(dir_path, file_list[stop_loss - 1]))

    start_date = wealth_df.index[0]
    end_date = wealth_df.index[-1]
    return_df = (wealth_df - wealth_df.shift(1)) / wealth_df.shift(1)
    return_df.ix[start_date, :] = 0.
    sharpe_ratio = get_sharpe_ratio(return_df)
    ann_return = get_annualized_return(wealth_df)
    save_df_dict = {}

    for cost in [5, 10]:
        save_path = os.path.join(result_path, 'cost_{}_sr_{}_old'.format(cost, stop_loss))
        picture_save_path = os.path.join(save_path, 'picture')

        make_dirs([picture_save_path, save_path])
        save_df_dict[str(cost)] = {'raw_strategy_df': pd.DataFrame(index=wealth_df.index),
                                   'save_path': save_path,
                                   'picture_save_path': picture_save_path}

    for method in wealth_df.keys():
        method_list = method.split('_')
        transaction_cost = method_list[-2][:-4]
        new_method_name = '{}_sl{}'.format('_'.join(method_list[:-1]), stop_loss)

        max_draw_down = get_max_draw_down(wealth_df[method])
        save_df_dict[transaction_cost]['raw_strategy_df'][new_method_name] = wealth_df[method]
        picture_save_path = save_df_dict[transaction_cost]['picture_save_path']
        text = 'Sharpe ratio: {:.3f}, Annualized return: {:.2f}%'.format(sharpe_ratio[method],
                                                                         ann_return[method] * 100)

        text = '{}, Max drawdown rate: {:.2f}%, SR: {}%'.format(text, max_draw_down * 100,
                                                                            stop_loss)
        text = '{}, Transaction cost: {}%'.format(text, float(transaction_cost) / 10)
        plot_picture(wealth_df[method], picture_title=new_method_name,
                     picture_save_path=os.path.join(picture_save_path, '{}.png'.format(new_method_name)), text=text)

    for cost in save_df_dict:
        save_path = save_df_dict[cost]['save_path']
        sub_wealth_df = save_df_dict[cost]['raw_strategy_df']
        sub_wealth_df.to_csv(
            os.path.join(save_path, '{}cost_{}_sr_{}_old_wealth.csv'.format(today_str, cost, stop_loss)))
        sub_wealth_df.to_pickle(
            os.path.join(save_path, '{}cost_{}_sr_{}_old_wealth.p'.format(today_str, cost, stop_loss)))

        sub_statistics_df, sub_best_strategies_df = generate_result_statistics(sub_wealth_df)
        sub_statistics_df.to_csv(
            os.path.join(save_path, '{}cost_{}_sr_{}_old_statistics.csv'.format(today_str, cost, stop_loss)))
        sub_statistics_df.to_pickle(
            os.path.join(save_path, '{}cost_{}_sr_{}_old_statistics.p'.format(today_str, cost, stop_loss)))

        sub_best_strategies_df.to_csv(
            os.path.join(save_path, '{}cost_{}_sr_{}_old_best.csv'.format(today_str, cost, stop_loss)))
        sub_best_strategies_df.to_pickle(
            os.path.join(save_path, '{}cost_{}_sr_{}_old_best.p'.format(today_str, cost, stop_loss)))

vdisplay.stop()
