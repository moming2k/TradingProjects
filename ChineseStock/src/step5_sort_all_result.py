#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step5_sort_all_result
# @Date: 2017-01-31
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime
import os

import pandas as pd
from xvfbwrapper import Xvfb

from ChineseStock.src.calculate_return_utils.calculate_return_utils_2 import generate_result_statistics
from ChineseStock.src.constants.path_info import result_path
from ChineseStock.src.util_functions.os_related import make_dirs
from ChineseStock.src.util_functions.util_function import get_annualized_return, get_sharpe_ratio, plot_picture, get_max_draw_down

today_str = datetime.datetime.today().strftime('%Y%m%d')

path_list = ['buy_only_no_cost_no_down', 'buy_only_no_cost_down', 'buy_only_cost_no_down', 'buy_only_cost_down']

# sort zero result
dir_path = os.path.join(result_path, path_list[0])
save_path = os.path.join(result_path, 'cost_0_sr_0_old')
picture_save_path = os.path.join(save_path, 'picture')

make_dirs([picture_save_path, save_path])

wealth_df = pd.read_pickle(os.path.join(dir_path, '20170129_only_buy_no_cost_no_drawdown_wealth.p'))
start_date = wealth_df.index[0]
end_date = wealth_df.index[-1]
result_df, best_strategy_df = generate_result_statistics(wealth_df)
return_df = (wealth_df - wealth_df.shift(1)) / wealth_df.shift(1)
return_df.ix[start_date, :] = 0.
sharpe_ratio = get_sharpe_ratio(return_df)
ann_return = get_annualized_return(wealth_df)

wealth_df.to_csv(os.path.join(save_path, '{}cost_0_sr_0_old_wealth.csv'.format(today_str)))
result_df.to_csv(os.path.join(save_path, '{}cost_0_sr_0_old_statistics.csv'.format(today_str)))
best_strategy_df.to_csv(os.path.join(save_path, '{}cost_0_sr_0_old_best.csv'.format(today_str)))

vdisplay = Xvfb(width=1366, height=768)
vdisplay.start()

for method in wealth_df.keys():
    max_draw_down = get_max_draw_down(wealth_df[method])
    text = 'Sharpe ratio: {:.3f}, Annualized return: {:.2f}%'.format(sharpe_ratio[method],
                                                                     ann_return[method] * 100)

    text = '{}, Max drawdown rate: {:.2f}%, SR: {}%'.format(text, max_draw_down * 100,
                                                                        0 * 100)
    text = '{}, Transaction cost: 0%'.format(text)
    plot_picture(wealth_df[method], picture_title=method,
                 picture_save_path=os.path.join(picture_save_path, '{}.png'.format(method)), text=text)


vdisplay.stop()
