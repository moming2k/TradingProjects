#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step7_plot_picture
# @Date: 2017-02-03
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd

from path_info import result_path
from util_function import plot_picture, get_max_draw_down, get_sharpe_ratio, get_annualized_return
from os_related import make_dirs
from constants import Constant as const

for stop_loss in range(1, 6):
    stop_loss_path = os.path.join(result_path, 'cost_2_sr_{}_new'.format(stop_loss))
    if not os.path.isdir(stop_loss_path):
        continue

    file_list = os.listdir(stop_loss_path)

    for file_name in file_list:
        if 'stoploss' in file_name and file_name.endswith('.p'):
            break

    else:
        continue

    wealth_df = pd.read_pickle(os.path.join(stop_loss_path, file_name))
    wealth_df = wealth_df.drop([datetime.datetime(2017, 7, 19)])
    wealth_df.loc[datetime.datetime(2013, 7, 19), :] = 10000.
    wealth_df = wealth_df.sort_index()
    picture_save_path = os.path.join(stop_loss_path, 'picture')
    make_dirs([picture_save_path])

    sharpe_ratio = get_sharpe_ratio(wealth_df, df_type=const.WEALTH_DATAFRAME, working_days=const.working_days)
    ann_return = get_annualized_return(wealth_df, df_type=const.WEALTH_DATAFRAME)

    for method in wealth_df.keys():
        if sharpe_ratio[method] < 1.:
            continue

        max_draw_down = get_max_draw_down(wealth_df[method])
        text = 'Sharpe ratio: {:.3f}, Annualized return: {:.2f}%'.format(sharpe_ratio[method], ann_return[method] * 100)

        text = '{}, Max drawdown rate: {:.2f}%, SR: {}%'.format(text, max_draw_down * 100, stop_loss)
        text = '{}, Transaction cost: 0.2%'.format(text)
        plot_picture(wealth_df[method], method, os.path.join(picture_save_path, '{}.png'.format(method)), text)
