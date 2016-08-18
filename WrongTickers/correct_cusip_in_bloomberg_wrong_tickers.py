#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: correct_cusip_in_bloomberg_wrong_tickers
# Author: Mark Wang
# Date: 18/8/2016


import pathos.multiprocessing as multitask
import pandas as pd
import numpy as np

# load cusip info
vol_df = pd.read_csv('Stock_data/Volume.csv', usecols=['date', 'TICKER', 'CUSIP'], dtype={'CUSIP': str, 'date': str})
vol_df['date'] = vol_df['date'].apply(lambda x: x[:4])


def process_bloomberg_df(df):
    for index in df.index:
        row = df.ix[index]
        wrong_ticker = row['WrongTicker']
        announce_date = row['DateToday'][:4]

        same_ticker = vol_df[vol_df['TICKER'] == wrong_ticker]
        if not same_ticker.empty:
            same_date = same_ticker[same_ticker['date'] == announce_date]
            if not same_date.empty:
                df.ix[index, 'CUSIP_wrong'] = same_date.ix[same_date.index[0], 'CUSIP']

    return df


def process_sdc_df(df):
    for index in df.index:
        row = df.ix[index]
        ticker = row['Ticker']
        wrong_ticker = row['WrongTicker']
        announce_date = row['DateToday'][:4]
        same_ticker = vol_df[vol_df['TICKER'] == ticker]
        if not same_ticker.empty:
            same_date = same_ticker[same_ticker['date'] == announce_date]
            if not same_date.empty:
                df.ix[index, 'CUSIP'] = same_date.ix[same_date.index[0], 'CUSIP']

        same_ticker = vol_df[vol_df['TICKER'] == wrong_ticker]
        if not same_ticker.empty:
            same_date = same_ticker[same_ticker['date'] == announce_date]
            if not same_date.empty:
                df.ix[index, 'CUSIP_wrong'] = same_date.ix[same_date.index[0], 'CUSIP']

    return df


# initial process info
process_num = 16
pool = multitask.ProcessingPool(process_num)

# process bloomberg file
df = pd.read_csv('result_csv/wrong_tickers_from_Bloomberg_large_ES.csv', dtype={'CUSIP': str})
df.loc[:, 'CUSIP_wrong'] = None

split_dfs = np.array_split(df, process_num)
result_dfs = pool.map(process_bloomberg_df, split_dfs)

df = pd.concat(result_dfs, axis=0)
df.to_csv('result_csv/wrong_tickers_from_Bloomberg_large_ES.csv', encoding='utf8')

del df

df = pd.read_csv('result_csv/wrong_tickers_from_SDC_target_name.csv', dtype={'CUSIP': str})
for key in ['  DateAnnounced', '  DateAnnouncedYesterday', '  DateAnnouncedTomorrow']:
    del df[key]

keys = df.keys()

for key in df.keys():
    if key.startswith(' ') or key.endswith(' '):
        new_key = key.strip()
        df[new_key] = df[key]
        del df[key]

    if key.endswith('_'):
        new_key = key[:-1]
        df[new_key] = df[key]
        del df[key]
df.loc[:, 'CUSIP_wrong'] = None

split_dfs = np.array_split(df, process_num)
result_dfs = pool.map(process_sdc_df, split_dfs)

df = pd.concat(result_dfs, axis=0)
df.to_csv('result_csv/wrong_tickers_from_SDC_target_name.csv', encoding='utf8')

del df
del vol_df
