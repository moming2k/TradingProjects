#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: generate_wrong_ticker_list
# @Date: 2016-12-14
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

from functions import calculate_score

import os
import re
import datetime

import pandas as pd

today_str = datetime.datetime.today().strftime('%Y%m%d')
root_path = '/home/wangzg/Documents/WangYouan/research/Wrong_tickers'

temp_path = os.path.join(root_path, 'temp')
today_temp_path = os.path.join(temp_path, today_str)
data_path = os.path.join(root_path, 'data')
result_path = os.path.join(root_path, 'result_csv')

if not os.path.isdir(today_temp_path):
    os.makedirs(today_temp_path)

all_ticker_series = pd.read_excel(os.path.join(data_path, 'All Tickers_Bloomberg.xlsx'))

sdc_df = pd.read_csv(os.path.join(result_path, 'SDC_CRSP_rename_top5pc.csv'), dtype={'TargetCUSIP': str},
                     index_col=0).drop_duplicates()

all_ticker_series['len'] = all_ticker_series['BAYRY'].apply(len)
all_ticker_series = all_ticker_series[all_ticker_series.len > 2]
all_ticker_series = all_ticker_series[all_ticker_series.len < 5]


# sdc_df['ticker_len'] = sdc_df.TargetPrimaryTickerSymbol.dropna().apply(len)
# sdc_df = sdc_df[sdc_df.ticker_len > 2]


def get_wrong_tickers(right_ticker):
    score = all_ticker_series.BAYRY.apply(lambda x: calculate_score(right_ticker, x))
    return all_ticker_series[score > 11].BAYRY.tolist()


def get_wrong_tickers_from_row_info(row):
    ticker = row['TargetPrimaryTickerSymbol']
    name = row['TargetName']

    if hasattr(name, 'upper'):
        tokens = re.split(r'[^a-zA-Z]+', name)
    else:
        tokens = []

    if not hasattr(ticker, '__len__'):
        ticker = ''

    wrong_ticker_list = []

    # handle initials
    while '' in tokens:
        tokens.remove('')

    upper_tokens = map(lambda x: x.upper(), tokens)
    while 'INC' in upper_tokens:
        upper_tokens.remove('INC')

    while 'HOLDINGS' in upper_tokens:
        upper_tokens.remove('HOLDINGS')

    initial = ''.join(i[0] for i in upper_tokens)
    if len(initial) >= 3:
        wrong_ticker_list.extend(get_wrong_tickers(initial))

    if len(ticker) >= 3:
        wrong_ticker_list.extend(get_wrong_tickers(ticker))

    first_letters = ''.join(upper_tokens)
    if len(first_letters) >= 3:
        wrong_ticker_list.extend(get_wrong_tickers(first_letters[:min(4, len(first_letters))]))

    capitalized_letters = ''.join(re.findall(r'[A-Z]', name))
    if len(capitalized_letters) >= 3:
        wrong_ticker_list.extend(get_wrong_tickers(capitalized_letters))

    while ticker in wrong_ticker_list:
        wrong_ticker_list.remove(ticker)

    return ','.join(list(set(wrong_ticker_list)))


sdc_df['wrong_tickers'] = sdc_df.apply(get_wrong_tickers_from_row_info, axis=1)
sdc_df.to_pickle(os.path.join(today_temp_path, 'sdc_add_wrong_tickers.p'))


# def remove_right_tickers(row):
#     wrong_tickers = row['wrong_tickers']
#     right_ticker = row['TargetPrimaryTickerSymbol']
#     if hasattr(wrong_tickers, 'split'):
#         wrong_tickers_list = wrong_tickers.split(',')
#
#         if hasattr(right_ticker, 'upper'):
#             while right_ticker in wrong_tickers_list:
#                 wrong_tickers_list.remove(right_ticker)
#
#         return ','.join(wrong_tickers_list)
#
#     else:
#         return wrong_tickers
#
# sdc_df['wrong_tickers'] = sdc_df.apply(remove_right_tickers, axis=1)

sdc_df[['TargetName', 'TargetPrimaryTickerSymbol', 'wrong_tickers']].to_csv(
    os.path.join(result_path, '{}_sdc_wrong_tickers.csv'.format(today_str)), index=False)