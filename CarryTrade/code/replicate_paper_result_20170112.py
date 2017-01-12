#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: replicate_paper_result_20170112
# @Date: 2017-01-12
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os, re
from datetime import datetime, time

import pandas as pd
import numpy as np

from constant import developed_currency_list, emerging_currency_list, currency_dict, columns

today_str = datetime.now().strftime('%Y%m%d')


def today(info):
    return '{}_{}'.format(today_str, info)


freq_list = ['1m', '3m', '6m', '12m']

ROOT_PATH = '/home/wangzg/Documents/WangYouan/research/CarryTrade'
DATA_PATH = os.path.join(ROOT_PATH, 'data')
TEMP_PATH = os.path.join(ROOT_PATH, 'temp')
today_temp = os.path.join(TEMP_PATH, today_str)

if not os.path.isdir(today_temp):
    os.makedirs(today_temp)

data_df = pd.read_csv(os.path.join(DATA_PATH, ('20160524_DATA_FX_Dollar_Rates_MID.csv')), index_col=0)
data_df['Date'] = data_df.Date.apply(lambda x: datetime.strptime(x, '%m/%d/%Y'))
data_df = data_df.set_index('Date', drop=True)
data_df.to_pickle(os.path.join(today_temp, '20160524_DATA_FX_Dollar_Rates_MID.p'))


def keep_3_effective_number(num):
    return '{:.3g}'.format(num)


def generate_result_df(report_type, country_type):
    if country_type == 'developed':
        currency_list = developed_currency_list

    else:
        currency_list = emerging_currency_list

    if report_type == 'SPOT':
        prefix = 'MID_SPOT'
    else:
        prefix = 'MID_{}FWD'.format(report_type)

    result_df = pd.DataFrame(columns=columns)

    for currency in currency_list:
        key = '{}_{}'.format(currency, prefix)
        data_column = data_df[key].dropna()
        start_date = data_column.index.min().strftime('%m/%d/%Y')
        end_date = data_column.index.max().strftime('%m/%d/%Y')

        result_df.loc[currency_dict[currency]] = {'Mean(%)': keep_3_effective_number(data_column.mean()),
                                                  'Max': keep_3_effective_number(data_column.max()),
                                                  'Min': keep_3_effective_number(data_column.min()),
                                                  'Std. dev.': keep_3_effective_number(data_column.std()),
                                                  'Sample Period': '{}-{}'.format(start_date, end_date)
                                                  }

    return result_df


for con_type in ['developed', 'emerging']:
    for rep_type in ['SPOT', '1m', '3m', '6m', '12m']:
        result_df = generate_result_df(rep_type, con_type)
        result_df.to_pickle(os.path.join(today_temp, '{}_{}.p'.format(con_type, rep_type)))
        result_df.to_csv(os.path.join(today_temp, '{}_{}.csv'.format(con_type, rep_type)))
        result_df.to_excel(os.path.join(today_temp, '{}_{}.xlsx'.format(con_type, rep_type)))
