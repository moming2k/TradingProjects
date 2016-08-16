#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: get_wrong_tickers_from_SDC_target_name(add_source)
# Author: Mark Wang
# Date: 15/8/2016


import re
import os
from multiprocessing import Pool

import pandas
import numpy as np

# load data
all_tickers_series = pandas.read_excel('All Tickers_Bloomberg.xlsx', sheetname='ticker', header=None)[0]

# for handle SDC files
name_dict = {'name': 'TargetName',
             'symbol': 'TargetPrimaryTickerSymbol',
             'DateToday': '  DateAnnounced',
             'DateTomorrow': '  DateAnnouncedTomorrow',
             'DateYesterday': '  DateAnnouncedYesterday',}

# data_df = pandas.read_csv('SDC_CRSP.csv', usecols=['TargetName', 'TargetPrimaryTickerSymbol']).drop_duplicates()

# Used for generate from SDC top5pc csv
data_df = pandas.read_csv('result_csv/SDC_CRSP_rename_top5pc.csv',
                          index_col=0).drop_duplicates()


def get_wrong_ticker_from_row(row):
    company_name = row[name_dict['name']]
    symbol = row[name_dict['symbol']]

    # get acronym and check if it in all_tickers_series
    tokens = re.split(r'[^a-zA-Z]+', company_name)
    while '' in tokens:
        tokens.remove('')
    short_name = ''.join([i[0] for i in tokens]).upper()
    initial_word_wrong_ticker_set = {short_name}
    for i in range(1, len(short_name)):
        initial_word_wrong_ticker_set.add(short_name[:i])
    capitalized_word_wrong_ticker_set = set()
    first_n_letter_wrong_ticker_set = set()

    # get first letter of each word
    first_word = re.findall(r'[a-zA-Z]+', company_name)
    if first_word:
        first_word = ''.join(first_word)
        for i in range(1, min(len(first_word) + 1, 9)):
            first_n_letter_wrong_ticker_set.add(first_word[:(i)].upper())

    # get combination of every capitalized word
    capitalized_letters = re.findall(r'[A-Z]', company_name)
    if capitalized_letters:
        short_name = ''
        for letter in capitalized_letters:
            short_name = '{}{}'.format(short_name, letter)
            capitalized_word_wrong_ticker_set.add(short_name)

    # Remove same name with right ticker
    capitalized_word_wrong_ticker_set.difference_update(initial_word_wrong_ticker_set)
    capitalized_word_wrong_ticker_set.difference_update(first_n_letter_wrong_ticker_set)
    first_n_letter_wrong_ticker_set.difference_update(initial_word_wrong_ticker_set)
    if symbol in initial_word_wrong_ticker_set:
        initial_word_wrong_ticker_set.remove(symbol)

    initial_word_wrong_ticker = '/'.join(
        list(all_tickers_series[all_tickers_series.isin(initial_word_wrong_ticker_set).nonzero()[0]]))
    capitalized_word_wrong_ticker = '/'.join(
        list(all_tickers_series[all_tickers_series.isin(capitalized_word_wrong_ticker_set).nonzero()[0]]))
    first_n_letter_wrong_ticker = '/'.join(
        list(all_tickers_series[all_tickers_series.isin(first_n_letter_wrong_ticker_set).nonzero()[0]]))
    return ';'.join((first_n_letter_wrong_ticker, capitalized_word_wrong_ticker, initial_word_wrong_ticker))


def process_sdc_df(tmp_df):
    return tmp_df.apply(get_wrong_ticker_from_row, axis=1)


def generate_wrong_ticker_dataframe(nonzero_index_list):
    """ Based on nonzero """

    # load wrong ticker info from file
    if os.path.isfile('wrong_ticker.p'):
        wrong_ticker_info = pandas.read_pickle('wrong_ticker.p')
    else:
        return
    result = pandas.DataFrame(columns=['Company Name', 'Ticker', 'WrongTicker', 'From', 'DateToday', 'DateTomorrow',
                                       'DateYesterday'])
    i = 0

    # add those wrong ticker to a new data frame.
    for index in nonzero_index_list:
        wrong_ticker_source = wrong_ticker_info[index].split(';')
        for ticker in wrong_ticker_source[0].split('/'):
            if not ticker:
                continue
            result.loc[i] = ({'Company Name': data_df.ix[index, name_dict['name']],
                              'Ticker': data_df.ix[index, name_dict['symbol']],
                              'DateToday': data_df.ix[index, name_dict['DateToday']],
                              'DateTomorrow': data_df.ix[index, name_dict['DateTomorrow']],
                              'DateYesterday': data_df.ix[index, name_dict['DateYesterday']],
                              'WrongTicker': ticker,
                              'From': "First {} letters from the company name".format(len(ticker))
                              })
            i += 1

        for ticker in wrong_ticker_source[1].split('/'):
            if not ticker:
                continue
            result.loc[i] = ({'Company Name': data_df.ix[index, name_dict['name']],
                              'Ticker': data_df.ix[index, name_dict['symbol']],
                              'DateToday': data_df.ix[index, name_dict['DateToday']],
                              'DateTomorrow': data_df.ix[index, name_dict['DateTomorrow']],
                              'DateYesterday': data_df.ix[index, name_dict['DateYesterday']],
                              'WrongTicker': ticker,
                              'From': "First {} letters from capitalized letters".format(len(ticker))
                              })
            i += 1

        for ticker in wrong_ticker_source[2].split('/'):
            if not ticker:
                continue
            result.loc[i] = ({'Company Name': data_df.ix[index, name_dict['name']],
                              'Ticker': data_df.ix[index, name_dict['symbol']],
                              'DateToday': data_df.ix[index, name_dict['DateToday']],
                              'DateTomorrow': data_df.ix[index, name_dict['DateTomorrow']],
                              'DateYesterday': data_df.ix[index, name_dict['DateYesterday']],
                              'WrongTicker': ticker,
                              'From': "First {} letters from the company name initials".format(len(ticker))
                              })
            i += 1
    return result


if __name__ == "__main__":
    process_num = 19
    pool = Pool(process_num)

    # get all wrong tickers
    split_sdc_df = np.array_split(data_df, process_num)
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
        pandas.concat(split_sdc_results, axis=0, ignore_index=True).drop_duplicates().reset_index(drop=True).to_csv(
            'result_csv/wrong_tickers_from_SDC_target_name.csv')

    if os.path.isfile('wrong_ticker.p'):
        os.remove('wrong_ticker.p')
