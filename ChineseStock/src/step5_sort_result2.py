#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step5_sort_result2
# @Date: 2017-01-31
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime
import os

import pandas as pd
from xvfbwrapper import Xvfb

from calculate_return_utils.calculate_return_utils_2 import generate_result_statistics
from constants.path_info import result_path
from util_functions.os_related import make_dirs
from util_functions.util_function import get_annualized_return, get_sharpe_ratio, plot_picture, get_max_draw_down

today_str = datetime.datetime.today().strftime('%Y%m%d')

path_list = ['buy_only_no_cost_no_down', 'buy_only_no_cost_down', 'buy_only_cost_no_down', 'buy_only_cost_down']

# sort zero result
dir_path = os.path.join(result_path, path_list[1])
save_path_prefix = os.path.join(result_path, 'cost_0_sr_')

save_path_list = []
save_df_dict = {}

wealth_df = pd.read_pickle(os.path.join(dir_path, '20170128_only_buy_no_cost_drawdown.p'))

start_date = wealth_df.index[0]
end_date = wealth_df.index[-1]
return_df = (wealth_df - wealth_df.shift(1)) / wealth_df.shift(1)
return_df.ix[start_date, :] = 0.
sharpe_ratio = get_sharpe_ratio(return_df)
ann_return = get_annualized_return(wealth_df)

for i in range(1, 6):
    save_path = os.path.join('{}{}_old'.format(save_path_prefix, i))
    picture_save_path = os.path.join(save_path, 'picture')

    make_dirs([picture_save_path, save_path])
    save_path_list.append([save_path, picture_save_path])
    save_df_dict[str(i)] = {'raw_strategy_df': pd.DataFrame(index=wealth_df.index),
                            'save_path': save_path,
                            'picture_save_path': picture_save_path}

vdisplay = Xvfb(width=1366, height=768)
vdisplay.start()

for method in wealth_df.keys():
    key_infos = method.split('_')[:-1]
    stop_loss = method.split('_')[-1][:1]
    if stop_loss == '0':
        continue

    key_infos.append('sl{}'.format(stop_loss))
    new_column_name = '_'.join(key_infos)
    max_draw_down = get_max_draw_down(wealth_df[method])
    save_df_dict[stop_loss]['raw_strategy_df'][new_column_name] = wealth_df[method]
    picture_save_path = save_df_dict[stop_loss]['picture_save_path']
    text = 'Sharpe ratio: {:.3f}, Annualized return: {:.2f}%'.format(sharpe_ratio[method],
                                                                     ann_return[method] * 100)

    text = '{}, Max drawdown rate: {:.2f}%, SR: {}%'.format(text, max_draw_down * 100,
                                                                        stop_loss)
    text = '{}, Transaction cost: 0%'.format(text)
    plot_picture(wealth_df[method], picture_title=new_column_name,
                 picture_save_path=os.path.join(picture_save_path, '{}.png'.format(new_column_name)), text=text)

for stop_loss in save_df_dict:
    save_path = save_df_dict[stop_loss]['save_path']
    sub_wealth_df = save_df_dict[stop_loss]['raw_strategy_df']
    if sub_wealth_df.empty:
        print stop_loss
        continue
    sub_wealth_df.to_csv(
        os.path.join(save_path, '{}cost_0_sr_{}_old_wealth.csv'.format(today_str, stop_loss)))
    sub_wealth_df.to_pickle(
        os.path.join(save_path, '{}cost_0_sr_{}_old_wealth.p'.format(today_str, stop_loss)))

    sub_statistics_df, sub_best_strategies_df = generate_result_statistics(sub_wealth_df)
    sub_statistics_df.to_csv(
        os.path.join(save_path, '{}cost_0_sr_{}_old_statistics.csv'.format(today_str, stop_loss)))
    sub_statistics_df.to_pickle(
        os.path.join(save_path, '{}cost_0_sr_{}_old_statistics.p'.format(today_str, stop_loss)))

    sub_best_strategies_df.to_csv(
        os.path.join(save_path, '{}cost_0_sr_{}_old_best.csv'.format(today_str, stop_loss)))
    sub_best_strategies_df.to_pickle(
        os.path.join(save_path, '{}cost_0_sr_{}_old_best.p'.format(today_str, stop_loss)))

vdisplay.stop()
