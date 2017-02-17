#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: draw_alpha_strategy_histogram
# @Date: 2017-02-17
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os
import re
import shutil
import datetime

import pandas as pd

from os_related import get_target_file_name
from constants import Constant as const
from util_function import plot_multiline, draw_histogram, get_max_draw_down, get_sharpe_ratio, get_annualized_return

result_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen/result/insider_stock_20170214_alpha_strategy_no_neglect_period'


def draw_wealth_pictures(wealth_result, alpha_result, picture_save_path, method_name, save_name,
                         stop_loss_rate, statistics_df=None):
    pic_path = picture_save_path

    line1 = 'Transaction cost 0.2% SR {}%'.format(stop_loss_rate)

    info_list = [line1]

    data_list = [wealth_result, wealth_result[wealth_result.index < datetime.datetime(2015, 1, 1)],
                 wealth_result[wealth_result.index > datetime.datetime(2015, 1, 1)]]

    time_period = ['all', 'before_2015', 'after_2015']

    for i, i_wealth in enumerate(data_list):
        sharpe_ratio = get_sharpe_ratio(i_wealth[method_name], df_type=const.WEALTH_DATAFRAME)
        ann_return = get_annualized_return(i_wealth[method_name], df_type=const.WEALTH_DATAFRAME)
        max_draw_down = get_max_draw_down(i_wealth[method_name])
        line = 'Data {}: Sharpe ratio {:.3f}, Annualized return {:.2f}%, Max drawdown rate {:.2f}%'.format(
            time_period[i], sharpe_ratio, ann_return, max_draw_down
        )
        info_list.append(line)

    text = '\n'.join(info_list)

    plot_multiline([wealth_result[method_name], alpha_result[method_name],
                    wealth_result[method_name] - alpha_result[method_name]],
                   legend_list=['Raw Strategy', 'Beta Strategy', 'Alpha Strategy'],
                   picture_title=method_name,
                   picture_save_path=os.path.join(pic_path, '{}.png'.format(save_name)),
                   text=text)


if __name__ == '__main__':
    best_sharpe_ratio = 0.0
    best_sharpe_ratio_file_path = None
    best_ann_return = 0.0
    best_ann_return_file_path = None

    statistics_df_list = []

    dir_list = os.listdir(result_path)

    if os.uname()[0] != 'Darwin':
        from xvfbwrapper import Xvfb

        vdisplay = Xvfb(width=1366, height=768)
        vdisplay.start()

    for dir_name in dir_list:
        current_path = os.path.join(result_path, dir_name)
        if not os.path.isdir(current_path):
            continue

        statistics_file_name = get_target_file_name(current_path, 'statistic', 'p')
        wealth_file_name = get_target_file_name(current_path, 'sr.', 'p')
        alpha_file_name = get_target_file_name(current_path, 'alpha', 'p')

        print current_path
        print statistics_file_name, wealth_file_name, alpha_file_name

        if wealth_file_name is None:
            wealth_file_name = get_target_file_name(current_path, 'stoploss', 'p')

        if statistics_file_name is None or wealth_file_name is None or alpha_file_name is None:
            continue

        statistics_df = pd.read_pickle(os.path.join(current_path, statistics_file_name))
        statistics_df_t = statistics_df.transpose()
        statistics_df_list.append(statistics_df_t)

        wealth_df = pd.read_pickle(os.path.join(current_path, wealth_file_name))
        alpha_df = pd.read_pickle(os.path.join(current_path, alpha_file_name))

        draw_histogram(statistics_df_t['sharpe_ratio'], 'Sharpe Ratio', 'Strategies', 'Histogram of Sharpe Ratio',
                       os.path.join(current_path, 'sharpe_ratio_histogram.png'))

        draw_histogram(statistics_df_t['annualized_return'], 'Annualized Return', 'Strategies',
                       'Histogram of Annualized Return',
                       os.path.join(current_path, 'ann_return_histogram.png'))

        stop_loss_rate = re.findall(r'\d+', wealth_file_name)[-1]

        best_sharpe_name = statistics_df_t.sharpe_ratio.idxmax()
        best_annualized_return_name = statistics_df_t.annualized_return.idxmax()
        draw_wealth_pictures(wealth_df, statistics_df=statistics_df, picture_save_path=current_path,
                             method_name=best_sharpe_name, alpha_result=alpha_df,
                             save_name='best_sharpe_ratio', stop_loss_rate=stop_loss_rate)
        draw_wealth_pictures(wealth_df, statistics_df=statistics_df, picture_save_path=current_path,
                             method_name=best_annualized_return_name, alpha_result=alpha_df,
                             save_name='best_ann_return', stop_loss_rate=stop_loss_rate)
        if statistics_df.ix['annualized_return', best_annualized_return_name] > best_ann_return:
            best_ann_return = statistics_df.ix['annualized_return', best_annualized_return_name]
            best_ann_return_file_path = current_path

        if statistics_df.ix['sharpe_ratio', best_sharpe_name] > best_sharpe_ratio:
            best_sharpe_ratio = statistics_df.ix['sharpe_ratio', best_sharpe_name]
            best_sharpe_ratio_file_path = current_path

    if best_sharpe_ratio_file_path is not None:
        shutil.copy(os.path.join(best_sharpe_ratio_file_path, 'best_sharpe_ratio.png'),
                    os.path.join(result_path, 'best_sharpe_ratio.png'))

    if best_ann_return_file_path is not None:
        shutil.copy(os.path.join(best_ann_return_file_path, 'best_ann_return.png'),
                    os.path.join(result_path, 'best_ann_return.png'))

    merged_sta_df = pd.concat(statistics_df_list, axis=0, ignore_index=False)

    draw_histogram(merged_sta_df['sharpe_ratio'], 'Sharpe Ratio', 'Strategies', 'Histogram of Sharpe Ratio',
                   os.path.join(result_path, 'sharpe_ratio_histogram.png'))

    draw_histogram(merged_sta_df['annualized_return'], 'Annualized Return', 'Strategies',
                   'Histogram of Annualized Return',
                   os.path.join(result_path, 'ann_return_histogram.png'))

    if os.uname()[0] != 'Darwin':
        vdisplay.stop()
