#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: generate_top_5_bloomberg_return_csv
# Author: Mark Wang
# Date: 30/7/2016

import re

import pandas as pd

df = pd.read_csv('result_csv/Bloomberg_CRSP(renamed).csv', index_col=0,
                 dtype={'CUSIP': str, 'CUSIP_Today': str, "CUSIP_Tomorrow": str, "CUSIP_Yesterday": str})
df = df[df['EarningsSurprise'] > 0.5]
df['EarningsSurpriseReturn'] = (df['OpenPriceTomorrow'] - df['ClosePriceYesterday']) / df['ClosePriceYesterday']
df = df.sort_values('EarningsSurprise', ascending=False) \
    .sort_values('EarningsSurpriseReturn', ascending=False) \
    .head(int(0.05 * df.shape[0]) + 1).reset_index(drop=True)

name_dict = {'name': 'Company Name',
             'symbol': 'Company Ticker'}


def get_wrong_ticker_from_row(row):
    company_name = row[name_dict['name']]
    symbol = row[name_dict['symbol']].split(' ')[0]

    # get acronym and check if it in all_tickers_series
    tokens = re.split(r'[^a-zA-Z]+', company_name)
    while '' in tokens:
        tokens.remove('')
    short_name = ''.join([i[0] for i in tokens]).upper()
    possible_wrong_ticker_set = {short_name}

    # get first letter of each word
    first_word = re.findall(r'[a-zA-Z]+', company_name)
    if first_word:
        first_word = first_word[0]
        for i in range(0, max(len(first_word), 8)):
            possible_wrong_ticker_set.add(first_word[:(i + 1)].upper())

    # get combination of every capitalized word
    capitalized_letters = re.findall(r'[A-Z]', company_name)
    if capitalized_letters:
        short_name = ''
        for letter in capitalized_letters:
            short_name = '{}{}'.format(short_name, letter)
            possible_wrong_ticker_set.add(short_name)

    # Remove same name with right ticker
    if symbol in possible_wrong_ticker_set:
        possible_wrong_ticker_set.remove(symbol)

    return ','.join(possible_wrong_ticker_set)


# df['WrongTickers'] = df.apply(get_wrong_ticker_from_row, axis=1)

df.to_csv('result_csv/Bloomberg_CRSP_rename_top5pc.csv', encoding='utf8')
