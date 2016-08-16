#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_info_to_wrong_ticker
# Author: Mark Wang
# Date: 15/8/2016

import os

import numpy as np
import pandas as pd


def get_information_from_saved_file(row_info, info_type='volume', date_type='today'):
    if date_type == 'today':
        date = row_info['DateToday']
    elif date_type == 'tomorrow':
        date = row_info['DateTomorrow']
    else:
        date = row_info['DateYesterday']

    date = ''.join(date.split('-'))
    ticker = row_info['WrongTicker']
    try:
        if info_type == 'volume':
            path = os.path.join('Stock_data', 'volume', '{}_VOL.csv'.format(ticker))
            if not os.path.isfile(path):
                return np.nan
            df = pd.read_csv(path, usecols=['date', 'VOL'], dtype={'date': str, 'VOL': float})
            df = df[df['date'] == date]
            if df.empty:
                return np.nan
            else:
                if not np.isnan(df.ix[df.index[0], 'VOL']):
                    return int(df.ix[df.index[0], 'VOL'])
                else:
                    return np.nan

        elif info_type == 'price':
            path = os.path.join('Stock_data', 'price', '{}_PRC.csv'.format(ticker))
            if not os.path.isfile(path):
                return np.nan
            df = pd.read_csv(path, usecols=['date', 'PRC'], dtype={'date': str, 'PRC': float})
            df = df[df['date'] == date]
            if df.empty:
                return np.nan
            else:
                return df.ix[df.index[0], 'PRC']

        elif info_type == 'log_return':
            path = os.path.join('Stock_data', 'logReturn', '{}_LR.csv'.format(ticker))
            if not os.path.isfile(path):
                return np.nan
            df = pd.read_csv(path, header=None, names=['date', 'LR'])
            df['date'] = df['date'].apply(lambda x: ''.join(x.split('-')))
            df = df[df['date'] == date]
            if df.empty:
                return np.nan
            else:
                return df.ix[df.index[0], 'LR']

        elif info_type == 'simple_return':
            path = os.path.join('Stock_data', 'simpleReturn', '{}_SR.csv'.format(ticker))
            if not os.path.isfile(path):
                return np.nan
            df = pd.read_csv(path, header=None, names=['date', 'SR'])
            df['date'] = df['date'].apply(lambda x: ''.join(x.split('-')))
            df = df[df['date'] == date]
            if df.empty:
                return np.nan
            else:
                return df.ix[df.index[0], 'SR']

        elif info_type == 'price_high':
            path = os.path.join('Stock_data', 'highlow', '{}_HL.csv'.format(ticker))
            if not os.path.isfile(path):
                return np.nan
            df = pd.read_csv(path, usecols=['date', 'ASKHI'], dtype={'date': str, 'ASKHI': float})
            df = df[df['date'] == date]
            if df.empty:
                return np.nan
            else:
                return df.ix[df.index[0], 'ASKHI']

        elif info_type == 'price_low':
            path = os.path.join('Stock_data', 'highlow', '{}_HL.csv'.format(ticker))
            if not os.path.isfile(path):
                return np.nan
            df = pd.read_csv(path, usecols=['date', 'BIDLO'], dtype={'date': str, 'BIDLO': float})
            df = df[df['date'] == date]
            if df.empty:
                return np.nan
            else:
                return df.ix[df.index[0], 'BIDLO']

        else:
            return np.nan
    except Exception, err:
        raise Exception('Ticker {}, info: {}, err: {}'.format(ticker, info_type, err))


def get_today_volume(row):
    return get_information_from_saved_file(row_info=row, info_type='volume', date_type='today')


def get_yesterday_volume(row):
    return get_information_from_saved_file(row_info=row, info_type='volume', date_type='yesterday')


def get_tomorrow_volume(row):
    return get_information_from_saved_file(row_info=row, info_type='volume', date_type='tomorrow')


def get_today_price(row):
    return get_information_from_saved_file(row_info=row, info_type='price', date_type='today')


def get_yesterday_price(row):
    return get_information_from_saved_file(row_info=row, info_type='price', date_type='yesterday')


def get_tomorrow_price(row):
    return get_information_from_saved_file(row_info=row, info_type='price', date_type='tomorrow')


def get_today_log_return(row):
    return get_information_from_saved_file(row_info=row, info_type='log_return', date_type='today')


def get_yesterday_log_return(row):
    return get_information_from_saved_file(row_info=row, info_type='log_return', date_type='yesterday')


def get_tomorrow_log_return(row):
    return get_information_from_saved_file(row_info=row, info_type='log_return', date_type='tomorrow')


def fill_in_missing_info(csv_path):
    target_df = pd.read_csv(csv_path, index_col=0)

    target_df['Volume'] = target_df.apply(axis=1, func=get_today_volume)
    target_df['VolumeTomorrow'] = target_df.apply(axis=1, func=get_tomorrow_volume)
    target_df['VolumeYesterday'] = target_df.apply(axis=1, func=get_yesterday_volume)

    target_df['Price'] = target_df.apply(axis=1, func=get_today_price)
    target_df['PriceTomorrow'] = target_df.apply(axis=1, func=get_tomorrow_price)
    target_df['PriceYesterday'] = target_df.apply(axis=1, func=get_yesterday_price)

    target_df['LogReturn'] = target_df.apply(
        axis=1, func=lambda x: get_information_from_saved_file(x, 'log_return', 'today'))
    target_df['LogReturnTomorrow'] = target_df.apply(
        axis=1, func=lambda x: get_information_from_saved_file(x, 'log_return', 'tomorrow'))
    target_df['LogReturnYesterday'] = target_df.apply(
        axis=1, func=lambda x: get_information_from_saved_file(x, 'log_return', 'yesterday'))

    target_df['SimpleReturn'] = target_df.apply(
        axis=1, func=lambda x: get_information_from_saved_file(x, 'simple_return', 'today'))
    target_df['SimpleReturnTomorrow'] = target_df.apply(
        axis=1, func=lambda x: get_information_from_saved_file(x, 'simple_return', 'tomorrow'))
    target_df['SimpleReturnYesterday'] = target_df.apply(
        axis=1, func=lambda x: get_information_from_saved_file(x, 'simple_return', 'yesterday'))

    target_df['PriceHigh'] = target_df.apply(
        axis=1, func=lambda x: get_information_from_saved_file(x, 'price_high', 'today'))
    target_df['PriceHighYesterday'] = target_df.apply(
        axis=1, func=lambda x: get_information_from_saved_file(x, 'price_high', 'yesterday'))
    target_df['PriceHighTomorrow'] = target_df.apply(
        axis=1, func=lambda x: get_information_from_saved_file(x, 'price_high', 'tomorrow'))

    target_df['PriceLow'] = target_df.apply(
        axis=1, func=lambda x: get_information_from_saved_file(x, 'price_low', 'today'))
    target_df['PriceLowYesterday'] = target_df.apply(
        axis=1, func=lambda x: get_information_from_saved_file(x, 'price_low', 'yesterday'))
    target_df['PriceLowTomorrow'] = target_df.apply(
        axis=1, func=lambda x: get_information_from_saved_file(x, 'price_low', 'tomorrow'))
    target_df.to_csv(csv_path, encoding='utf8')


if __name__ == "__main__":
    print 'Start to handle bloomberg'
    fill_in_missing_info('result_csv/wrong_tickers_from_Bloomberg_large_ES.csv')
    print 'Start to handle SDC'
    fill_in_missing_info('result_csv/wrong_tickers_from_SDC_target_name.csv')
