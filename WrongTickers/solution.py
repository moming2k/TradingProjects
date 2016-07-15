#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: solution
# Author: Mark Wang
# Date: 15/7/2016

import re
import os
from multiprocessing import Pool

import pandas
import numpy as np

# load data
all_tickers = pandas.read_excel('All Tickers_Bloomberg.xlsx', sheetname='ticker', header=None)[0]
sdc_info = pandas.read_csv('SDC_CRSP.csv', usecols=['TargetName', 'TargetPrimaryTickerSymbol']).drop_duplicates()


def get_wrong_ticker(row):
    company_name = row['TargetName']
    symbol = row['TargetPrimaryTickerSymbol']

    # get acronym and check if it in all_tickers
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

    return '/'.join(list(all_tickers[all_tickers.isin(possible_wrong_ticker_set).nonzero()[0]]))


def process_df(tmp_df):
    return tmp_df.apply(get_wrong_ticker, axis=1)


def merge_tickers(nonzero_index):
    # load wrong ticker info from file
    if os.path.isfile('wrong_ticker.p'):
        wrong_ticker_info = pandas.read_pickle('wrong_ticker.p')
    else:
        return
    result = pandas.DataFrame(columns=['TargetName', 'TargetPrimaryTickerSymbol', 'WrongTicker'])
    i = 0

    # add those wrong ticker to a new data frame.
    for index in nonzero_index:
        for ticker in wrong_ticker_info[index].split('/'):
            result.loc[i] = ({'TargetName': sdc_info.ix[index, 'TargetName'],
                              'TargetPrimaryTickerSymbol': sdc_info.ix[index, 'TargetPrimaryTickerSymbol'],
                              'WrongTicker': ticker
                              })
            i += 1
    return result


if __name__ == "__main__":
    process_num = 19
    pool = Pool(process_num)

    # get all wrong tickers
    split_dfs = np.array_split(sdc_info, process_num)
    process_result = pool.map(process_df, split_dfs)
    wrong_tickers = pandas.concat(process_result, axis=0)
    wrong_tickers.to_pickle('wrong_ticker.p')

    # Reformat wrong tickers and save them to files
    len_info = wrong_tickers.apply(len)
    non_zero_index = len_info[len_info > 0].index
    process_num = min(len(non_zero_index), process_num)
    if process_num != 0:
        split_non_zero_indexs = np.array_split(non_zero_index, process_num)
        process_result = pool.map(merge_tickers, split_non_zero_indexs)
        result = pandas.concat(process_result, axis=0, ignore_index=True)

        result.to_csv('output.csv')
