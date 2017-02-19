#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: draw_alpha_strategy_histogram
# @Date: 2017-02-17
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import datetime
import os
import re
import shutil

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from ChineseStock.src.util_functions.os_related import get_target_file_name
from ChineseStock.src.util_functions.util_function import draw_histogram, get_max_draw_down, get_sharpe_ratio, get_annualized_return
from constants import Constant as const

result_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen/result/insider_stock_20170214_alpha_strategy_no_neglect_period'


def plot_multiline(data_list, legend_list, picture_title, picture_save_path, text1, text2):
    """ Draw data series info """

    # plot file and save picture
    fig = plt.figure(figsize=(15, 8))

    left = 0.1
    bottom = 0.3
    width = 0.75
    height = 0.60
    ax = fig.add_axes([left, bottom, width, height])
    ax.set_title(picture_title)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.figtext(0.01, 0.01, text1, horizontalalignment='left')
    plt.figtext(0.51, 0.01, text2, horizontalalignment='left')

    date_series = data_list[0].index

    color_list = ['r-', 'b-', 'y-', 'g-']

    for i, data_series in enumerate(data_list):
        # get data series info
        plt.plot(date_series, data_series, color_list[i], label=legend_list[i])

    min_date = date_series[0]
    max_date = date_series[-1]
    plt.gca().set_xlim(min_date, max_date)
    plt.legend(loc=0)
    fig.autofmt_xdate()
    # fig.suptitle(picture_title)

    # print dir(fig)
    fig.savefig(picture_save_path)
    plt.close()


def draw_wealth_pictures(wealth_result, beta_result, picture_save_path, method_name, save_name,
                         stop_loss_rate):
    pic_path = picture_save_path

    line1 = 'Transaction cost 0.2% SR {}%'.format(stop_loss_rate)

    info_list = [line1]

    raw_strategy = wealth_result[method_name]
    beta_strategy = beta_result[method_name]
    alpha_strategy = raw_strategy - beta_strategy + 1

    time_period = ['all', '09_14', '13_16', 'after_15']
    period_list = [(None, None), (datetime.datetime(2009, 1, 1), datetime.datetime(2015, 1, 1)),
                   (datetime.datetime(2013, 1, 1), datetime.datetime(2017, 1, 1)),
                   (datetime.datetime(2015, 1, 1), None),
                   ]

    def generate_line_info(i, date_tuple):
        current_line = 'Date {}'.format(time_period[i])
        result_list = [current_line]
        for prefix in ['Raw', 'Beta', 'Alpha']:

            if prefix == 'Raw':
                data_series = raw_strategy

            elif prefix == 'Beta':
                data_series = beta_strategy

            else:
                data_series = alpha_strategy

            if date_tuple[0] is not None:
                data_series = data_series[data_series.index > date_tuple[0]]

            if date_tuple[1] is not None:
                data_series = data_series[data_series.index < date_tuple[1]]

            sharpe_ratio = get_sharpe_ratio(data_series, df_type=const.WEALTH_DATAFRAME)
            ann_return = get_annualized_return(data_series, df_type=const.WEALTH_DATAFRAME) * 100
            max_draw_down = get_max_draw_down(data_series) * 100

            current_line = '{}: Sharpe Ratio {:.3f}, Annualized Return {:.2f}%, Max Drawdown rate {:.2f}%'.format(
                prefix, sharpe_ratio, ann_return, max_draw_down
            )
            result_list.append(current_line)

        return result_list

    for i, date_tuple in enumerate(period_list[:2]):
        info_list.extend(generate_line_info(i, date_tuple))

    text1 = '\n'.join(info_list)

    info_list = []
    for i, date_tuple in enumerate(period_list[2:]):
        info_list.extend(generate_line_info(i + 2, date_tuple))

    text2 = '\n'.join(info_list)

    plot_multiline([raw_strategy, beta_strategy, alpha_strategy],
                   legend_list=['Raw Strategy', 'Beta Strategy', 'Alpha Strategy'],
                   picture_title=method_name,
                   picture_save_path=os.path.join(pic_path, '{}.png'.format(save_name)),
                   text1=text1, text2=text2)


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

        wealth_file_name = get_target_file_name(current_path, 'sr.', 'p')
        beta_file_name = get_target_file_name(current_path, 'alpha', 'p')

        print current_path
        print wealth_file_name, beta_file_name

        if wealth_file_name is None:
            wealth_file_name = get_target_file_name(current_path, 'stoploss', 'p')

        if wealth_file_name is None or beta_file_name is None:
            continue

        raw_strategy_df = pd.read_pickle(os.path.join(current_path, wealth_file_name))
        beta_strategy_df = pd.read_pickle(os.path.join(current_path, beta_file_name))
        alpha_strategy_df = raw_strategy_df - beta_strategy_df + 1

        sharpe_ratio = get_sharpe_ratio(alpha_strategy_df, df_type=const.WEALTH_DATAFRAME)
        annualized_return = get_annualized_return(alpha_strategy_df, df_type=const.WEALTH_DATAFRAME)

        statistics_df = pd.DataFrame(index=sharpe_ratio.index)
        statistics_df['sharpe_ratio'] = sharpe_ratio
        statistics_df['annualized_return'] = annualized_return
        statistics_df_list.append(statistics_df)

        draw_histogram(sharpe_ratio.dropna(), 'Sharpe Ratio', 'Strategies', 'Histogram of Sharpe Ratio',
                       os.path.join(current_path, 'sharpe_ratio_histogram.png'))

        draw_histogram(annualized_return.dropna(), 'Annualized Return', 'Strategies', 'Histogram of Annualized Return',
                       os.path.join(current_path, 'ann_return_histogram.png'))

        stop_loss_rate = re.findall(r'\d+', wealth_file_name)[-1]

        best_sharpe_name = sharpe_ratio.idxmax()
        best_annualized_return_name = annualized_return.idxmax()
        draw_wealth_pictures(raw_strategy_df, picture_save_path=current_path,
                             method_name=best_sharpe_name, beta_result=beta_strategy_df,
                             save_name='best_sharpe_ratio', stop_loss_rate=stop_loss_rate)
        draw_wealth_pictures(raw_strategy_df, picture_save_path=current_path,
                             method_name=best_annualized_return_name, beta_result=beta_strategy_df,
                             save_name='best_ann_return', stop_loss_rate=stop_loss_rate)
        if annualized_return[best_annualized_return_name] > best_ann_return:
            best_ann_return = annualized_return[best_annualized_return_name]
            best_ann_return_file_path = current_path

        if sharpe_ratio[best_sharpe_name] > best_sharpe_ratio:
            best_sharpe_ratio = sharpe_ratio[best_sharpe_name]
            best_sharpe_ratio_file_path = current_path

    if best_sharpe_ratio_file_path is not None:
        shutil.copy(os.path.join(best_sharpe_ratio_file_path, 'best_sharpe_ratio.png'),
                    os.path.join(result_path, 'best_sharpe_ratio.png'))

    if best_ann_return_file_path is not None:
        shutil.copy(os.path.join(best_ann_return_file_path, 'best_ann_return.png'),
                    os.path.join(result_path, 'best_ann_return.png'))

    merged_sta_df = pd.concat(statistics_df_list, axis=0, ignore_index=False)

    # merged_sta_df.to_csv('test.csv')
    draw_histogram(merged_sta_df['sharpe_ratio'].dropna(), 'Sharpe Ratio', 'Strategies', 'Histogram of Sharpe Ratio',
                   os.path.join(result_path, 'sharpe_ratio_histogram.png'))

    draw_histogram(merged_sta_df['annualized_return'].dropna(), 'Annualized Return', 'Strategies',
                   'Histogram of Annualized Return',
                   os.path.join(result_path, 'ann_return_histogram.png'))

    if os.uname()[0] != 'Darwin':
        vdisplay.stop()
