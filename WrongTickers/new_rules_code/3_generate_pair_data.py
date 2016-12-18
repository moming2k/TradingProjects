#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: 3_generate_pair_data
# @Date: 2016-12-18
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os
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

pair_info_df = pd.read_pickle(os.path.join(temp_path, '20161216', 'sdc_add_source.p'))

pair_4a_info = pair_info_df[['TargetPrimaryTickerSymbol', 'TargetName', '4A_from_first_word']].dropna(
    subset=['4A_from_first_word']
)
pair_2a2b_info = pair_info_df[['TargetPrimaryTickerSymbol', 'TargetName', '2A2B_from_tickers']].dropna(
    subset=['2A2B_from_tickers']
)


def spilt_df(group):
    row = group.irow(0)
    if '2A2B_from_tickers' in row:
        wrong_tickers = row['2A2B_from_tickers'].split(',')
    else:
        wrong_tickers = row['4A_from_first_word'].split(',')

    company_name_right = row['TargetName']
    ticker_right = row['TargetPrimaryTickerSymbol']

    result_df = pd.DataFrame(columns=['ticker_right', 'company_name_right', 'ticker_wrong'])
    i = 0
    for wrong_ticker in wrong_tickers:
        result_df.loc[i] = {'ticker_right': ticker_right, 'company_name_right': company_name_right,
                            'ticker_wrong': wrong_ticker}

        i += 1

    return result_df


pair_4a_df = pair_4a_info.groupby(['TargetPrimaryTickerSymbol', 'TargetName', '4A_from_first_word'],
                                  group_keys=False).apply(spilt_df).reset_index(drop=True)
pair_2a2b_df = pair_2a2b_info.groupby(['TargetPrimaryTickerSymbol', 'TargetName', '2A2B_from_tickers'],
                                      group_keys=False).apply(spilt_df).reset_index(drop=True)


# add sdc_df parameters
sdc_df = pd.read_csv(os.path.join(result_path, 'SDC_CRSP_rename_top5pc.csv'), dtype={'TargetCUSIP': str},
                     index_col=0).drop_duplicates(['TargetName', 'TargetPrimaryTickerSymbol'])
sdc_df['ticker_right'] = sdc_df['TargetPrimaryTickerSymbol']
pair_4a_df = pair_4a_df.merge(sdc_df, on='ticker_right', how='left')
pair_2a2b_df = pair_2a2b_df.merge(sdc_df, on='ticker_right', how='left')

pair_4a_df.to_pickle(os.path.join(today_temp_path, 'pairs_4a_from_first_word'))
pair_2a2b_df.to_pickle(os.path.join(today_temp_path, 'pairs_2a2b_from_tickers'))
