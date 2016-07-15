#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: solution
# Author: Mark Wang
# Date: 15/7/2016

import re
from multiprocessing import Pool

import pandas
import numpy as np

all_tickers = pandas.read_excel('All Tickers_Bloomberg.xlsx', sheetname='ticker', header=None)[0]
wrong_tickers = None

def get_wrong_ticker(row):
    company_name = row['TargetName']
    symbol = row['TargetPrimaryTickerSymbol']

    # get acronym and check if it in all_tickers
    tokens = re.split(r'[^a-zA-Z]+', company_name)
    while '' in tokens:
        tokens.remove('')
    short_name = ''.join([i[0] for i in tokens]).upper()
    possible_wrong_ticker_set = {short_name}

    # get first word
    first_word = re.findall(r'[a-zA-Z]+', company_name)
    if first_word:
        first_word = first_word[0]
        for i in range(0, max(len(first_word), 8)):
            possible_wrong_ticker_set.add(first_word[:(i + 1)].upper())

    # Remove same name with right ticker
    if symbol in possible_wrong_ticker_set:
        possible_wrong_ticker_set.remove(symbol)

    return '/'.join(list(all_tickers[all_tickers.isin(possible_wrong_ticker_set).nonzero()[0]]))


def process_df(tmp_df):
    return tmp_df.apply(get_wrong_ticker, axis=1)


def merge_tickers(nonzero_index):
    if wrong_tickers is None:
        return
    result = pandas.DataFrame(columns=['TargetName', 'TargetPrimaryTickerSymbol', 'WrongTicker'])
    i = 0
    for index in nonzero_index:
        for ticker in wrong_tickers[index].split('/'):
            # print df.ix[index, 'TargetName'], df.ix[index, 'TargetPrimaryTickerSymbol'], wrong_ticker
            result.loc[i] = ({'TargetName': df.ix[index, 'TargetName'],
                              'TargetPrimaryTickerSymbol': df.ix[index, 'TargetPrimaryTickerSymbol'],
                              'WrongTicker': ticker
                              })
            i += 1
    return result


if __name__ == "__main__":
    # while True:
    process_num = 4
    pool = Pool(process_num)
    sdc_info = pandas.read_csv('SDC_CRSP.csv', usecols=['TargetName', 'TargetPrimaryTickerSymbol'])
    df = sdc_info.drop_duplicates().sample(20)
    # df.to_pickle('temp2.p')
    # df = pandas.read_pickle('temp2.p')

    split_dfs = np.array_split(df, process_num)
    process_result = pool.map(process_df, split_dfs)
    global wrong_tickers
    wrong_tickers = pandas.concat(process_result, axis=0)

    # wrong_tickers = df.apply(get_wrong_ticker, axis=1)
    len_info = wrong_tickers.apply(len)
    non_zero_index = len_info[len_info > 0].index
    process_num = min(len(non_zero_index), process_num)
    if process_num != 0:
        split_non_zero_indexs = np.array_split(non_zero_index, process_num)
        process_result = pool.map(merge_tickers, split_non_zero_indexs)
        for result in process_result:
            print process_result
        result = pandas.concat(process_result, axis=0, ignore_index=True)

        # result = pandas.DataFrame(columns=['TargetName', 'TargetPrimaryTickerSymbol', 'WrongTicker'])
        # i = 0
        # for index in non_zero_index:
        #     for wrong_ticker in wrong_tickers[index].split('/'):
        #         # print df.ix[index, 'TargetName'], df.ix[index, 'TargetPrimaryTickerSymbol'], wrong_ticker
        #         result.loc[i] = ({'TargetName': df.ix[index, 'TargetName'],
        #                           'TargetPrimaryTickerSymbol': df.ix[index, 'TargetPrimaryTickerSymbol'],
        #                           'WrongTicker': wrong_ticker
        #                           })
        #         i += 1

        result.to_csv('output.csv')
