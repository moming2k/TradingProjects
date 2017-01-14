#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: get_forward_discount_spot_rate
# @Date: 2017-01-13
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os
import datetime

import pandas as pd

from constant import developed_currency_list, emerging_currency_list, currency_dict, columns

freq_list = ['1m', '3m', '6m', '12m']

ROOT_PATH = '/home/wangzg/Documents/WangYouan/research/CarryTrade'
DATA_PATH = os.path.join(ROOT_PATH, 'data')
TEMP_PATH = os.path.join(ROOT_PATH, 'temp')

today_temp = os.path.join(TEMP_PATH, datetime.date.today().strftime('%Y%m%d'))

if not os.path.isdir(today_temp):
    os.makedirs(today_temp)

data_df = pd.read_pickle(os.path.join(TEMP_PATH, '20170112', '20160524_DATA_FX_Dollar_Rates_MID.p'))


def keep_3_effective_number(num):
    return '{:.3g}'.format(num)


# the following method is used to generate forward discount result
def generate_fd_result_df(report_type, country_type):
    if country_type == 'developed':
        currency_list = developed_currency_list

    else:
        currency_list = emerging_currency_list

    prefix = 'MID_{}FWD'.format(report_type)

    result_df = pd.DataFrame(columns=columns)

    for currency in currency_list:
        key = '{}_{}'.format(currency, prefix)
        spot_key = '{}_MID_SPOT'.format(currency)
        temp_df = data_df[[key, spot_key]].dropna(subset=[key])

        data_column = (temp_df[key] - temp_df[spot_key]) / temp_df[spot_key]

        start_date = data_df[key].dropna().index.min().strftime('%m/%d/%Y')
        end_date = data_df[key].dropna().index.max().strftime('%m/%d/%Y')

        result_df.loc[currency_dict[currency]] = {'Mean(%)': keep_3_effective_number(data_column.mean()),
                                                  'Max': keep_3_effective_number(data_column.max()),
                                                  'Min': keep_3_effective_number(data_column.min()),
                                                  'Std. dev.': keep_3_effective_number(data_column.std()),
                                                  'Sample Period': '{}-{}'.format(start_date, end_date)
                                                  }

    return result_df


for con_type in ['developed', 'emerging']:
    for rep_type in ['1m', '3m', '6m', '12m']:
        result_df = generate_fd_result_df(rep_type, con_type)
        result_df.to_pickle(os.path.join(today_temp, 'forward_discount_{}_{}.p'.format(con_type, rep_type)))
        result_df.to_csv(os.path.join(today_temp, 'forward_discount_{}_{}.csv'.format(con_type, rep_type)))
        result_df.to_excel(os.path.join(today_temp, 'forward_discount_{}_{}.xlsx'.format(con_type, rep_type)))


# the following method are used to generate spot rate change data
def generate_spot_result_df(shift_num, country_type):
    if country_type == 'developed':
        currency_list = developed_currency_list

    else:
        currency_list = emerging_currency_list

    prefix = 'MID_SPOT'

    result_df = pd.DataFrame(columns=columns)

    for currency in currency_list:
        key = '{}_{}'.format(currency, prefix)
        temp_column = data_df[key].dropna()
        shift_column = temp_column.shift(shift_num).rename('{}_{}'.format(currency, shift_num))
        data_column = (shift_column - temp_column) / temp_column
        data_column = data_column.dropna()

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
    for rep_type in [1, 3, 6, 12]:
        result_df = generate_spot_result_df(rep_type, con_type)
        result_df.to_pickle(os.path.join(today_temp, 'spot_rate_change_{}_{}.p'.format(con_type, rep_type)))
        result_df.to_csv(os.path.join(today_temp, 'spot_rate_change_{}_{}.csv'.format(con_type, rep_type)))
        result_df.to_excel(os.path.join(today_temp, 'spot_rate_change_{}_{}.xlsx'.format(con_type, rep_type)))
