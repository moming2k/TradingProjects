#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step15_max_abs_drawdown
# @Date: 2017-01-24
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import pandas as pd

from path_info import *
from util_function import plot_date_picture

df_15 = pd.read_pickle(os.path.join(return_data_path, '20160919_1m_updated_15_curr.p'))
df_48 = pd.read_pickle(os.path.join(return_data_path, '20160919_1m_updated_48_curr.p'))

key_15 = '15_currs_15_liquid_5_parts_1m'
key_48 = '48_currs_48_liquid_5_parts_1m'


def generate_wealth(return_series, review_month=6, max_drawdown=0.05):
    wealth_series = (return_series + 1).cumprod()

    new_return_series = return_series.copy()

    buy_flag = True
    for i in range(review_month, wealth_series.shape[0]):
        if buy_flag:
            current_return = wealth_series[i] / wealth_series[i - review_month: i].max() - 1
            if current_return <= -max_drawdown:
                buy_flag = False
                new_return_series[i] = 0
        else:
            current_return = wealth_series[i] / wealth_series[i - review_month: i].min() - 1
            if current_return >= max_drawdown:
                buy_flag = True
            else:
                new_return_series[i] = 0

    return new_return_series


iterables = [[6, 12, 24], ['5%', '10%']]
multiple_index = pd.MultiIndex.from_product(iterables, names=['review_month', 'drawdown_rate'])


def generate_return_table_and_draw_picture(save_path, series, title):
    result_df = pd.DataFrame(index=multiple_index, columns=['return', 'sharpe'])
    plot_date_picture(series.index, series, title, os.path.join(save_path, 'original.png'))
    for rev_mon in [6, 12, 24]:
        for max_drawback in [0.05, 0.1]:
            new_return = generate_wealth(return_series=series, review_month=rev_mon, max_drawdown=max_drawback)

            new_wealth = (new_return + 1).cumprod()

            plot_date_picture(new_return.index, new_return, '{}, {}r, {}drawdown'.format(title, rev_mon, max_drawback),
                              os.path.join(save_path, 'review_{}_drawdown_rate_{}.png'.format(rev_mon, max_drawback)))

            annualized_return = new_wealth[-1] ** (1 / 32.) - 1
            annualized_sharpe = new_return.mean() / new_return.std() * 12 ** 0.5

            result_df.loc[(rev_mon, '{}%'.format(int(100 * max_drawback)))] = {'return': annualized_return,
                                                                               'sharpe': annualized_sharpe}

    result_df.to_pickle(os.path.join(save_path, 'result.p'))
    return result_df


drawdown_15_path = os.path.join(picture_save_path, 'drawdown_15')
drawdown_48_path = os.path.join(picture_save_path, 'drawdown_48')

if not os.path.isdir(drawdown_15_path):
    os.makedirs(drawdown_15_path)

if not os.path.isdir(drawdown_48_path):
    os.makedirs(drawdown_48_path)

generate_return_table_and_draw_picture(drawdown_48_path, series=df_48[key_48],
                                       title='48l, 5p, 1m')
generate_return_table_and_draw_picture(drawdown_15_path, series=df_15[key_15],
                                       title='15l, 5p, 1m')
