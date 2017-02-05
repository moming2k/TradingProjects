#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: update_wrong_ticker_and_ibes_count_file
# Author: Mark Wang
# Date: 22/8/2016


import numpy as np
import pandas as pd
import pathos.multiprocessing as multiprocessing

from constants import *

ibes_month_df = pd.read_csv('IBES_EPS_NUMEST_FIRM_MONTH.csv', usecols=['NUMEST', 'STATPERS', 'OFTIC', 'CUSIP'],
                            dtype={'CUSIP': str, 'STATPERS': str})
ibes_month_df = ibes_month_df[ibes_month_df['STATPERS'].apply(lambda x: x[-4:-2]) == '01']
ibes_month_df['YEAR'] = ibes_month_df['STATPERS'].apply(lambda x: x[:4])


def get_ibes_num(cusip, ticker, year):
    df = ibes_month_df[ibes_month_df['CUSIP'] == cusip]
    df = df[df['YEAR'] == year]
    if df.empty:
        df = ibes_month_df[ibes_month_df['OFTIC'] == ticker]
        df = df[df['YEAR'] == year]

    if df.empty:
        return 0
    else:
        return df.ix[df.index[0], u'NUMEST']


def update_wrong_tickers(df_path, pool_number):
    pool = multiprocessing.ProcessingPool(pool_number)
    df = pd.read_csv(df_path, index_col=0, dtype={CUSIP_REAL: str, CUSIP_WRONG: str})

    split_dfs = np.array_split(df, pool_number)

    def update_df(df):
        for index in df.index:
            real_ticker = df.ix[index, TICKER_REAL]
            wrong_ticker = df.ix[index, TICKER_WRONG]
            real_cusip = df.ix[index, CUSIP_REAL]
            wrong_cusip = df.ix[index, CUSIP_WRONG]
            year = df.ix[index, DATE_TODAY][:4]
            df.ix[index, "IBESNumber_real"] = get_ibes_num(real_cusip, real_ticker, year)
            df.ix[index, 'IBESNumber_wrong'] = get_ibes_num(wrong_cusip, wrong_ticker, year)

        return df

    result_dfs = pool.map(update_df, split_dfs)
    result_df = pd.concat(result_dfs, axis=0)
    # cd_result_df = update_df(own_report_df)
    new_path = df_path.replace('.csv', '(UpdatedIBES).csv')
    result_df.to_csv(new_path, encoding='utf8')


if __name__ == '__main__':
    process_number = 16
    update_wrong_tickers('result_csv/wrong_tickers_from_SDC_target_name.csv', process_number)
    update_wrong_tickers('result_csv/wrong_tickers_from_Bloomberg_large_ES.csv', process_number)
    ibes_month_df.to_csv('result_csv/IBES_EPS_NUMSET_COUNT.csv', encoding='utf8')
