#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: draw_one_picture
# @Date: 2017-02-12
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime
import os

import pandas as pd

from util_functions.util_function import plot_picture, get_max_draw_down, date_as_float

temp_path = '/Users/warn/PycharmProjects/QuestionFromProfWang/ChineseStock/result'
file_name = 'insider_stock_20170214_alpha_strategy_no_neglect_period'

if __name__ == '__main__':
    # from xvfbwrapper import Xvfb
    #
    # vdisplay = Xvfb(width=1366, height=768)
    # vdisplay.start()
    # data_series = pd.read_pickle(os.path.join(temp_path, 'si_own_cd_insider', 'cost_2_sr_1_wealth',
    #                                           '{}.p'.format(file_name)))

    data_series = pd.read_pickle(os.path.join(temp_path, 'si_plandate', 'cost_2_sr_5', '20170212_5sr.p'))[file_name]
    return_df = (data_series - data_series.shift(1)) / data_series.shift(1)
    sharpe_ratio = return_df.mean() / return_df.std() * (251 ** 0.5)
    max_draw_down = get_max_draw_down(data_series)

    start_date = data_series.first_valid_index()
    end_date = data_series.last_valid_index()
    ann_return = (data_series.ix[end_date] / data_series.ix[start_date]) ** (
        1 / (date_as_float(end_date) - date_as_float(start_date))) - 1

    text = 'Sharpe ratio: {:.3f}, Annualized return: {:.2f}%'.format(sharpe_ratio,
                                                                     ann_return * 100)

    text = '{}, Max drawdown rate: {:.2f}%, SR: {}%'.format(text, max_draw_down * 100,
                                                            5)
    text = '{}, Transaction cost: 0.2%'.format(text)

    plot_picture(data_series=data_series, picture_title=file_name,
                 picture_save_path=os.path.join(temp_path, '{}.png'.format(file_name)),
                 text=text)

    data_series = data_series[data_series.index < datetime.datetime(2015, 1, 1)]
    return_df = (data_series - data_series.shift(1)) / data_series.shift(1)
    sharpe_ratio = return_df.mean() / return_df.std() * (252 ** 0.5)
    max_draw_down = get_max_draw_down(data_series)

    start_date = data_series.first_valid_index()
    end_date = data_series.last_valid_index()
    ann_return = (data_series.ix[end_date] / data_series.ix[start_date]) ** (
        1 / (date_as_float(end_date) - date_as_float(start_date))) - 1

    text = 'Sharpe ratio: {:.3f}, Annualized return: {:.2f}%'.format(sharpe_ratio,
                                                                     ann_return * 100)

    text = '{}, Max drawdown rate: {:.2f}%, SR: {}%'.format(text, max_draw_down * 100,
                                                            5)
    text = '{}, Transaction cost: 0.2%'.format(text)

    plot_picture(data_series=data_series, picture_title=file_name,
                 picture_save_path=os.path.join(temp_path, '{}_before_2015.png'.format(file_name)),
                 text=text)
    # vdisplay.stop()
