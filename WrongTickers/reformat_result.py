#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: reformat_result
# Author: Mark Wang
# Date: 29/8/2016

import os

import pandas as pd

column = ['Date', 'Company Name', 'CUSIP', 'CUSIP_wrong', 'Ticker', 'WrongTicker', 'WrongTickerSource', 'isEventDate',
          'isEventTomorrow', 'isEventYesterday', 'IBES NUM_real', 'IBES NUM_wrong', 'LogReturn_real', 'LogReturn_wrong',
          'Price_real', 'Price_wrong', 'PriceHigh_real', 'PriceHigh_wrong', 'PriceLow_real', 'PriceLow_wrong',
          'PriceRange_real', 'PriceRange_wrong', 'SimpleReturn_real', 'SimpleReturn_wrong', 'Volume_real',
          'Volume_wrong', 'cshoc_real', 'cshoc_wrong', 'divd_real', 'divd_wrong', 'eps_real', 'eps_wrong', 'exchg_real',
          'exchg_wrong', 'trfd_real', 'trfd_wrong']

file_list = os.listdir('result_csv')

for file in file_list:
    if not file.endswith('SDC.csv') and not file.endswith('Bloomberg.csv'):
        continue

    df = pd.read_csv(os.path.join('result_csv', file), dtype=str, index_col=0)
    new_df = pd.DataFrame()
    for key in column:
        new_df[key] = df[key]

    new_df.to_csv(os.path.join('result_csv', file), encoding='utf8', index=False)
