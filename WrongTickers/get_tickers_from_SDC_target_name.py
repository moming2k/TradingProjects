#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: get_tickers_from_SDC_target_name
# Author: Mark Wang
# Date: 15/7/2016

import re
import os
from multiprocessing import Pool

import pandas
import numpy as np

# load data
all_tickers_series = pandas.read_excel('All Tickers_Bloomberg.xlsx', sheetname='ticker', header=None)[0]

# sdc_df = pandas.read_csv('SDC_CRSP.csv', usecols=['TargetName', 'TargetPrimaryTickerSymbol']).drop_duplicates()

# Used for generate from top5pc csv
sdc_df = pandas.read_csv('result_csv/SDC_CRSP_rename_top5pc.csv',
                         usecols=['TargetName', 'TargetPrimaryTickerSymbol']).drop_duplicates()


def get_wrong_ticker_from_row(row):
    company_name = row['TargetName']
    symbol = row['TargetPrimaryTickerSymbol']

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

    return '/'.join(list(all_tickers_series[all_tickers_series.isin(possible_wrong_ticker_set).nonzero()[0]]))


def process_sdc_df(tmp_df):
    return tmp_df.apply(get_wrong_ticker_from_row, axis=1)


def generate_wrong_ticker_dataframe(nonzero_index_list):
    """ Based on nonzero """

    # load wrong ticker info from file
    if os.path.isfile('wrong_ticker.p'):
        wrong_ticker_info = pandas.read_pickle('wrong_ticker.p')
    else:
        return
    result = pandas.DataFrame(columns=['TargetName', 'TargetPrimaryTickerSymbol', 'WrongTicker'])
    i = 0

    # add those wrong ticker to a new data frame.
    for index in nonzero_index_list:
        for ticker in wrong_ticker_info[index].split('/'):
            result.loc[i] = ({'TargetName': sdc_df.ix[index, 'TargetName'],
                              'TargetPrimaryTickerSymbol': sdc_df.ix[index, 'TargetPrimaryTickerSymbol'],
                              'WrongTicker': ticker
                              })
            i += 1
    return result


if __name__ == "__main__":
    process_num = 19
    pool = Pool(process_num)

    # get all wrong tickers
    split_sdc_df = np.array_split(sdc_df, process_num)
    split_sdc_results = pool.map(process_sdc_df, split_sdc_df)
    wrong_tickers = pandas.concat(split_sdc_results, axis=0)
    wrong_tickers.to_pickle('wrong_ticker.p')

    # Reformat wrong tickers and save them to files
    wrong_ticker_len_info = wrong_tickers.apply(len)
    non_zero_index_list = wrong_ticker_len_info[wrong_ticker_len_info > 0].index
    process_num = min(len(non_zero_index_list), process_num)
    if process_num != 0:
        split_non_zero_index_list = np.array_split(non_zero_index_list, process_num)
        split_sdc_results = pool.map(generate_wrong_ticker_dataframe, split_non_zero_index_list)
        wrong_ticker_dataframe = pandas.concat(split_sdc_results, axis=0, ignore_index=True)

        wrong_ticker_dataframe.to_csv('result_csv/wrong_tickers_from_SDC_target_name.csv')
