#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: get_wrong_tickers_from_Bloomberg_file(add_source)
# Author: Mark Wang
# Date: 15/8/2016

import os
import re

import pathos
import pandas
import numpy as np

# from add_info_to_wrong_ticker import *

# load data
all_tickers_series = pandas.read_excel('All Tickers_Bloomberg.xlsx', sheetname='ticker', header=None)[0]

# for handle SDC files
name_dict = {'Company Name': 'Company Name',
             'Ticker': 'Company Ticker',
             'DateToday': 'DateToday',
             'DateTomorrow': 'DateTomorrow',
             'DateYesterday': 'DateYesterday',
             "CUSIP": 'CUSIP'
             }

# Used for generate from SDC top5pc csv
data_df = pandas.read_csv('result_csv/Bloomberg_CRSP_rename_top5pc.csv', dtype={'CUSIP': str},
                          index_col=0)

data_df['Company Ticker'] = data_df['Company Ticker'].apply(lambda x: str(x).split(' ')[0])


def get_wrong_ticker_from_row(row):
    company_name = row[name_dict['Company Name']]
    symbol = row[name_dict['Ticker']].split(' ')[0]

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

    columns = ['Company Name', 'Ticker', 'WrongTicker', 'WrongTickerSource', 'DateToday', 'DateTomorrow',
               'DateYesterday', 'CUSIP']
    for key in data_df.keys():
        if key not in columns:
            columns.append(key)

    result = pandas.DataFrame(columns=columns)
    i = 0

    # add those wrong ticker to a new data frame.
    for index in nonzero_index_list:
        wrong_ticker_source = wrong_ticker_info[index].split(';')
        row = data_df.ix[index]
        info_list = []
        for ticker in wrong_ticker_source[0].split('/'):
            if not ticker:
                continue
            info_list.append({'WrongTicker': ticker,
                              'WrongTickerSource': "First {} letters from the company name".format(len(ticker))
                              })

        for ticker in wrong_ticker_source[1].split('/'):
            if not ticker:
                continue
            info_list.append({'WrongTicker': ticker,
                              'WrongTickerSource': "First {} letters from capitalized letters".format(len(ticker))
                              })

        for ticker in wrong_ticker_source[2].split('/'):
            if not ticker:
                continue
            info_list.append({'WrongTicker': ticker,
                              'WrongTickerSource': "First {} letters from the company name initials".format(len(ticker))
                              })

        for info_dict in info_list:
            for key in name_dict:
                info_dict[key] = row[name_dict[key]]
            info_dict.update(row)
            result.loc[i] = info_dict

            i += 1

    return result


if __name__ == "__main__":
    process_num = 19
    pool = pathos.multiprocessing.ProcessingPool(process_num)

    # get all wrong tickers
    split_dfs = np.array_split(data_df, process_num)
    split_results = pool.map(process_sdc_df, split_dfs)
    wrong_tickers = pandas.concat(split_results, axis=0)
    wrong_tickers.to_pickle('wrong_ticker.p')

    # Reformat wrong tickers and save them to files
    wrong_ticker_len_info = wrong_tickers.apply(len)
    non_zero_index_list = wrong_ticker_len_info[wrong_ticker_len_info > 0].index
    process_num = min(len(non_zero_index_list), process_num)
    if process_num != 0:
        split_non_zero_index_list = np.array_split(non_zero_index_list, process_num)
        split_results = pool.map(generate_wrong_ticker_dataframe, split_non_zero_index_list)
        pandas.concat(split_results, axis=0, ignore_index=True).drop_duplicates().reset_index(drop=True).to_csv(
            'result_csv/wrong_tickers_from_Bloomberg_large_ES.csv', encoding='utf8')

    if os.path.isfile('wrong_ticker.p'):
        os.remove('wrong_ticker.p')
