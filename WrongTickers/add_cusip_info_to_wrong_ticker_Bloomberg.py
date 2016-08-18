#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_cusip_info_to_wrong_ticker_Bloomberg
# Author: Mark Wang
# Date: 15/8/2016

import pathos

from add_info_to_wrong_ticker import *

vol_df = pd.read_csv('Stock_data/Volume.csv', dtype={'CUSIP': str, 'date': str, 'TICKER': str},
                     usecols=['date', 'TICKER', 'CUSIP', 'VOL'])


def get_cusip_from_ticker_date(ticker, today, yesterday, tomorrow):
    df = vol_df[vol_df['TICKER'] == ticker]
    if df.empty:
        return np.nan
    today = ''.join(today.split('-'))
    yesterday = ''.join(yesterday.split('-'))
    tomorrow = ''.join(tomorrow.split('-'))
    real_df = df[df['date'] == today]
    if real_df.empty:
        real_df = df[df['date'] == yesterday]

    if real_df.empty:
        real_df = df[df['date'] == tomorrow]

    if real_df.empty:
        real_df = df

    return real_df.ix[real_df.index[0], 'CUSIP']


def get_volume_from_volume_date(ticker, date):
    df = vol_df[vol_df['TICKER'] == ticker]
    date = ''.join(date.split('-'))
    df = df[df['date'] == date]
    if df.empty:
        return np.nan

    vol = df.ix[df.index[0], 'VOL']
    if not vol or np.isnan(vol):
        return np.nan
    else:
        return int(vol)


def add_cusip_and_real_volume(row):
    today = row['DateToday']
    tomorrow = row['DateTomorrow']
    yesterday = row['DateYesterday']
    wrong_ticker = row['WrongTicker']
    real_ticker = row['Ticker']

    result = {'cusip_real': get_cusip_from_ticker_date(real_ticker, today, tomorrow, yesterday),
              'cusip_wrong': get_cusip_from_ticker_date(wrong_ticker, today, tomorrow, yesterday),
              # 'Volume_real': get_volume_from_volume_date(real_ticker, today),
              # 'VolumeTomorrow_real': get_volume_from_volume_date(real_ticker, tomorrow),
              # 'VolumeYesterday_real': get_volume_from_volume_date(real_ticker, yesterday),
              }

    return pd.Series(result)


def process_df(data_df):
    return pd.concat([data_df, data_df.apply(add_cusip_and_real_volume, axis=1)], axis=1)


if __name__ == "__main__":
    # print 'Start to handle bloomberg'
    # add_original_file_info('result_csv/wrong_tickers_from_Bloomberg_large_ES.csv', 'Bloomberg')

    process_num = 15
    pool = pathos.multiprocessing.ProcessingPool(processes=process_num)

    print "Read SDC file from path"
    bloomberg_df = pd.read_csv('result_csv/wrong_tickers_from_Bloomberg_large_ES.csv', index_col=0)

    print "Split file"
    split_df = np.array_split(bloomberg_df, process_num)
    result_dfs = pool.map(process_df, split_df)
    bloomberg_df = pd.concat(result_dfs, axis=0)
    # bloomberg_df = process_bloomberg_df(bloomberg_df)
    bloomberg_df.to_csv('result_csv/wrong_tickers_from_Bloomberg_large_ES.csv', encoding='utf8')
