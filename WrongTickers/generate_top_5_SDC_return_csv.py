#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: wrong_tickers_of_top5_return
# Author: Mark Wang
# Date: 30/7/2016

import re

import pandas as pd

# get top 5% mna target return records
df = pd.read_csv('result_csv/SDC_CRSP(renamed).csv', index_col=0)
df = df[df['TargetSharePrice1DayPriortoAnnouncement'] > 0.0]
df['MnATargetReturn'] = (df['TargetClosingPrice1DayAfterAnnDate'] - df['TargetSharePrice1DayPriortoAnnouncement']) / \
                        df['TargetSharePrice1DayPriortoAnnouncement']

df = df.sort_values('MnATargetReturn', ascending=False).head(int(0.05 * df.shape[0]) + 1).reset_index(drop=True)

# Generate wrong ticker row
all_tickers_series = pd.read_excel('All Tickers_Bloomberg.xlsx', sheetname='ticker', header=None)[0]

name_dict = {'name': 'TargetName',
             'symbol': 'TargetPrimaryTickerSymbol'}


def get_wrong_ticker_from_row(row):
    company_name = row[name_dict['name']]
    symbol = row[name_dict['symbol']]

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

df['WrongTickers'] = df.apply(get_wrong_ticker_from_row, axis=1)

df.to_csv('result_csv/SDC_CRSP_rename_top5pc.csv', encoding='utf8')