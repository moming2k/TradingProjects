#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step14_add_drawback
# @Date: 2017-01-23
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import pandas as pd

from path_info import *
from util_function import plot_date_picture

df_15 = pd.read_pickle(os.path.join(return_data_path, '20160919_1m_updated_15_curr.p'))
df_48 = pd.read_pickle(os.path.join(return_data_path, '20160919_1m_updated_48_curr.p'))

key_15 = '15_currs_15_liquid_5_parts_1m'
key_48 = '48_currs_48_liquid_5_parts_1m'


def generate_wealth(return_series, date_sep=6, max_drawback=0.05):
    wealth_series = (return_series + 1).cumprod()

    new_return_series = return_series.copy()

    buy_flag = True
    for i in range(date_sep, wealth_series.shape[0]):
        if buy_flag:
            current_return = wealth_series[i] / wealth_series[i - date_sep] - 1
            if current_return <= -max_drawback:
                buy_flag = False
                new_return_series[i] = 0
        else:
            current_return = wealth_series[i] / wealth_series[i - date_sep] - 1
            if current_return >= max_drawback:
                buy_flag = True
            else:
                new_return_series[i] = 0

    return new_return_series


iterables = [[6, 12, 24], ['5%', '10%']]
multiple_index = pd.MultiIndex.from_product(iterables, names=['review_month', 'drawback_rate'])


def generate_return_table_and_draw_picture(save_path, series, title):
    result_df = pd.DataFrame(index=multiple_index, columns=['return', 'sharpe'])
    plot_date_picture(series.index, series, title, os.path.join(save_path, 'original.png'))
    for sep in [6, 12, 24]:
        for max_drawback in [0.05, 0.1]:
            new_return = generate_wealth(return_series=series, date_sep=sep, max_drawback=max_drawback)

            new_wealth = (new_return + 1).cumprod()

            plot_date_picture(new_return.index, new_return, '{}, {}r, {}drawback'.format(title, sep, max_drawback),
                              os.path.join(save_path, 'sep_{}_max_drawback_{}.png'.format(sep, max_drawback)))

            annualized_return = new_wealth[-1] ** (1 / 32.) - 1
            annualized_sharpe = new_return.mean() / new_return.std() * 12 ** 0.5

            result_df.loc[(sep, '{}%'.format(int(100 * max_drawback)))] = {'return': annualized_return,
                                                                           'sharpe': annualized_sharpe}

    result_df.to_pickle(os.path.join(save_path, 'result.p'))
    return result_df


generate_return_table_and_draw_picture(os.path.join(picture_save_path, '48'), series=df_48[key_48], title='48l, 5p, 1m')
generate_return_table_and_draw_picture(os.path.join(picture_save_path, '15'), series=df_15[key_15], title='15l, 5p, 1m')
