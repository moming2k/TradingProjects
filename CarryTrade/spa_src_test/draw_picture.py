#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: draw_picture
# Author: Mark Wang
# Date: 26/9/2016

import os
import datetime

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

FORMER_RESULT_PATH = '/Users/warn/Documents/RAForWangZG/CarryTrade/csv_results/xlsx_results'
CSV_RESULT_PATH = '/Users/warn/Documents/RAForWangZG/CarryTrade/csv_results'
PICTURE_SAVE_PATH = os.path.join(os.path.curdir, 'output_picture_4')
if not os.path.isdir(PICTURE_SAVE_PATH):
    os.makedirs(PICTURE_SAVE_PATH)

FILE_NAME_DICT = {'48': {'1m': '20160919_1m_updated_48_curr_add_learning.csv',
                         '3m': '20160919_3m_updated_48_curr_add_learning.csv',
                         '6m': '20160919_6m_updated_48_curr_add_learning.csv',
                         '12m': '20160919_12m_updated_48_curr_add_learning.csv',
                         },
                  '15': {'1m': '20160919_1m_updated_15_curr_add_learning.csv',
                         '3m': '20160919_3m_updated_15_curr_add_learning.csv',
                         '6m': '20160919_6m_updated_15_curr_add_learning.csv',
                         '12m': '20160919_12m_updated_15_curr_add_learning.csv',
                         },
                  }

START_INDEX_DICT = {'1m': [97, 193, 290],
                    '3m': [32, 64, 96],
                    '6m': [16, 32, 48],
                    '12m': [8, 16, 24],
                    '1m_8': [48, 97, 145, 193, 241, 290, 338],
                    '3m_8': [16, 32, 48, 64, 80, 96, 112]
                    }


# START_INDEX_DICT_8 = {'1m': [48, 97, 145, 193, 241, 290, 338],
#                       '3m': [16, 32, 48, 64, 80, 96, 112]
#                       }


def plot_date_picture(date_list, data_series, method_type, picture_title):
    # get data series info
    data_series = data_series.shift(1) + 1
    data_series[0] = 1
    for i in range(1, len(data_series)):
        data_series[i] = data_series[i - 1] * data_series[i]

    # plot file and save picture
    plt.clf()
    fig = plt.figure(figsize=(15, 6))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.plot(date_list, data_series, 'ro-')
    min_date = date_list[0]
    max_date = date_list[-1]
    plt.gca().set_xlim(min_date, max_date)
    fig.autofmt_xdate()
    fig.suptitle(picture_title)
    for i in START_INDEX_DICT[method_type]:
        plt.axvline(date_list[i], color='b')
    fig.savefig(os.path.join(PICTURE_SAVE_PATH, '{}.png'.format(picture_title)))


def draw_4_divisions_pictures():
    div_4_max_df = pd.read_excel(os.path.join(FORMER_RESULT_PATH, 'max_info_statistics.xlsx'), sheetname='division 4')

    for method_index in div_4_max_df.index:
        method_name = div_4_max_df.ix[method_index, 'method']
        if os.path.isfile(os.path.join(PICTURE_SAVE_PATH, '{}.png'.format(method_name))):
            continue
        method_info_list = method_name.split('_')
        data_df = pd.read_csv(os.path.join(CSV_RESULT_PATH, FILE_NAME_DICT[method_info_list[0]][method_info_list[-1]]),
                              index_col=0)

        date_info = map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'), data_df.index)
        plot_date_picture(date_list=date_info, data_series=data_df[method_name], method_type=method_info_list[-1],
                          picture_title=method_name)


def draw_8_divisions_pictures():
    div_8_max_df = pd.read_excel(os.path.join(FORMER_RESULT_PATH, 'max_info_statistics.xlsx'), sheetname='division 8')

    for method_index in div_8_max_df.index:
        method_name = div_8_max_df.ix[method_index, 'method']
        if os.path.isfile(os.path.join(PICTURE_SAVE_PATH, '{}.png'.format(method_name))):
            continue
        method_info_list = method_name.split('_')
        data_df = pd.read_csv(FILE_NAME_DICT[method_info_list[0]][method_info_list[-1]], index_col=0)

        date_info = map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'), data_df.index)
        plot_date_picture(date_list=date_info, data_series=data_df[method_name],
                          method_type='{}_8'.format(method_info_list[-1]), picture_title=method_name)


if __name__ == '__main__':
    draw_4_divisions_pictures()
