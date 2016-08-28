#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: get_two_years_SDC_daily_data
# Author: Mark Wang
# Date: 27/8/2016

import datetime
import os
import re
from dateutil.relativedelta import relativedelta

import pandas as pd
import numpy as np
import pathos

from constants import *

file_path = 'result_csv/wrong_tickers_from_SDC_target_name(UpdatedIBES).csv'
df = pd.read_csv(file_path, usecols=[CUSIP_REAL, CUSIP_WRONG, DATE_TODAY, DATE_YESTERDAY,
                                     DATE_TOMORROW, COMPANY_NAME, TICKER_WRONG, TICKER_REAL,
                                     WRONG_TICKER_SOURCE])
df[DATE_TODAY] = df[DATE_TODAY].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
df[DATE_YESTERDAY] = df[DATE_YESTERDAY].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
df[DATE_TOMORROW] = df[DATE_TOMORROW].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
ticker_group = df.groupby(TICKER_REAL)

ibes_df = pd.read_csv('result_csv/IBES_EPS_NUMSET_COUNT.csv', usecols=['CUSIP', 'OFTIC', 'YEAR', 'NUMEST'],
                      dtype={'CUSIP': str, "YEAR": int, 'NUMEST': int})


def get_information_in_CRSP(cusip, ticker, start_date, end_date, info_type):
    date_col_name = 'date'
    if info_type == VOLUME:
        ticker_path = os.path.join('Stock_data', info_type.lower(), '{}_VOL.csv'.format(ticker))
        cusip_path = os.path.join('Stock_data', "{}_cusip".format(info_type.lower()), '{}_VOL.csv'.format(ticker))
        use_cols = [date_col_name, 'VOL']
        data_type = {date_col_name: str}

    elif info_type == PRICE:
        ticker_path = os.path.join('Stock_data', info_type.lower(), '{}_PRC.csv'.format(ticker))
        cusip_path = os.path.join('Stock_data', "{}_cusip".format(info_type.lower()), '{}_PRC.csv'.format(ticker))
        use_cols = [date_col_name, 'PRC']
        data_type = {date_col_name: str}

    elif info_type == PRICE_RANGE:
        ticker_path = os.path.join('Stock_data', 'highlow', '{}_HL.csv'.format(ticker))
        cusip_path = os.path.join('Stock_data', "highlow_cusip", '{}_HL.csv'.format(ticker))
        use_cols = [date_col_name, 'BIDLO', 'ASKHI']
        data_type = {date_col_name: str}

    elif info_type == COMPUSTAT:
        ticker_path = os.path.join('Stock_data', info_type.lower(), '{}_COMPU.csv'.format(ticker))
        cusip_path = os.path.join('Stock_data', "{}_cusip".format(info_type.lower()), '{}_COMPU.csv'.format(ticker))
        date_col_name = 'datadate'
        use_cols = [date_col_name, 'divd', 'cshoc', 'eps', 'trfd', 'exchg']
        data_type = {date_col_name: str}

    elif info_type == LOG_RETURN:
        ticker_path = os.path.join('Stock_data', 'logReturn', '{}_LR.csv'.format(ticker))
        cusip_path = "not exist"
        use_cols = [date_col_name, 'LR']
        data_type = {date_col_name: str}

    elif info_type == SIMPLE_RETURN:
        ticker_path = os.path.join('Stock_data', 'simpleReturn', '{}_SR.csv'.format(ticker))
        cusip_path = "not exist"
        use_cols = [date_col_name, 'SR']
        data_type = {date_col_name: str}

    else:
        raise ValueError('Unknow info type {}'.format(info_type))

    if os.path.isfile(cusip_path):
        data_df = pd.read_csv(cusip_path, usecols=use_cols, dtype=data_type)

    elif os.path.isfile(ticker_path):
        data_df = pd.read_csv(ticker_path, usecols=use_cols, dtype=data_type)

    else:
        return pd.DataFrame()

    if date_col_name != 'date':
        data_df['date'] = data_df[date_col_name]
        del data_df[date_col_name]
        date_col_name = 'date'

    data_df[date_col_name] = data_df[date_col_name].apply(lambda x: datetime.datetime.strptime(x, "%Y%m%d"))
    sub_df = data_df[data_df[date_col_name] >= start_date]
    sub_df = sub_df[sub_df[date_col_name] <= end_date]
    sub_df.set_index(date_col_name, inplace=True)

    if info_type in {LOG_RETURN, SIMPLE_RETURN, PRICE, VOLUME}:
        info_dict = {LOG_RETURN: 'LR',
                     SIMPLE_RETURN: 'SR',
                     PRICE: 'PRC',
                     VOLUME: 'VOL'}
        sub_df[info_type] = sub_df[info_dict[info_type]]
        del sub_df[info_dict[info_type]]
    elif info_type == PRICE_RANGE:
        sub_df[PRICE_HIGH] = sub_df['ASKHI']
        sub_df[PRICE_LOW] = sub_df['BIDLO']
        del sub_df['ASKHI']
        del sub_df['BIDLO']

    return sub_df[~sub_df.index.duplicated(keep='last')]


def get_range_info(cusip, ticker, start_date, end_date):
    result_df = pd.DataFrame()
    for info in [LOG_RETURN, PRICE_RANGE, SIMPLE_RETURN, PRICE, VOLUME, COMPUSTAT]:
        result_df = result_df.join(get_information_in_CRSP(cusip=cusip, ticker=ticker, start_date=start_date,
                                                           end_date=end_date, info_type=info),
                                   how='outer')

    return result_df


def get_ibes_info(cusip, ticker, year):
    sub_df = ibes_df[ibes_df['CUSIP'] == cusip]
    if sub_df.empty:
        sub_df = ibes_df[ibes_df['OFTIC'] == ticker]

    sub_df = sub_df[sub_df['YEAR'] == year]
    if sub_df.empty:
        return 0
    else:
        return sub_df.ix[sub_df.index[0], 'NUMEST']


def merge_real_and_wrong_ticker_data(real, wrong):
    real_keys = real.keys()
    for key in real_keys:
        if key == 'date' or REAL in key:
            continue
        new_key = '{}_{}'.format(key, REAL)
        real[new_key] = real[key]
        del real[key]

    wrong_keys = wrong.keys()
    for key in wrong_keys:
        if key == 'date' or WRONG in key:
            continue
        new_key = '{}_{}'.format(key, WRONG)
        wrong[new_key] = wrong[key]
        del wrong[key]

    return pd.concat([real, wrong], axis=1)


def get_two_years_data(ticker_name):
    sub_df = ticker_group.get_group(ticker_name)
    sub_index = sub_df.index
    real_ticker = sub_df.ix[sub_index[0], TICKER_REAL]
    real_cusip = sub_df.ix[sub_index[0], CUSIP_REAL]
    date_today = sub_df.ix[sub_index[0], DATE_TODAY]
    date_tomorrow = sub_df.ix[sub_index[0], DATE_TOMORROW]
    date_yesterday = sub_df.ix[sub_index[0], DATE_YESTERDAY]
    source = sub_df.ix[sub_index[0], WRONG_TICKER_SOURCE]
    company_name = sub_df.ix[sub_index[0], COMPANY_NAME]

    start_date = date_today - relativedelta(years=1)
    end_date = date_today + relativedelta(years=1)
    real_df = get_range_info(real_cusip, real_ticker, start_date, end_date)
    result_list = []
    if real_df.empty:
        return pd.DataFrame()

    real_ibes_date = {date_today.year: get_ibes_info(real_cusip, real_ticker, date_today.year),
                      date_today.year - 1: get_ibes_info(real_cusip, real_ticker, date_today.year - 1),
                      date_today.year + 1: get_ibes_info(real_cusip, real_ticker, date_today.year + 1),
                      }

    if PRICE_HIGH in real_df.keys() and PRICE_LOW in real_df.keys():
        real_df[PRICE_RANGE] = real_df[PRICE_HIGH] - real_df[PRICE_LOW]
    for index in sub_index:
        wrong_ticker = sub_df.ix[index, TICKER_WRONG]
        wrong_cusip = sub_df.ix[index, CUSIP_WRONG]
        wrong_df = get_range_info(cusip=wrong_cusip, ticker=wrong_ticker,
                                  start_date=start_date, end_date=end_date)
        if wrong_df.empty:
            continue

        if PRICE_HIGH in wrong_df.keys() and PRICE_LOW in wrong_df.keys():
            wrong_df[PRICE_RANGE] = wrong_df[PRICE_HIGH] - wrong_df[PRICE_LOW]

        wrong_ibes_date = {date_today.year: get_ibes_info(wrong_cusip, wrong_ticker, date_today.year),
                           date_today.year - 1: get_ibes_info(wrong_cusip, wrong_ticker, date_today.year - 1),
                           date_today.year + 1: get_ibes_info(wrong_cusip, wrong_ticker, date_today.year + 1),
                           }
        temp_df = merge_real_and_wrong_ticker_data(real_df, wrong_df)
        temp_df.loc[:, TICKER_WRONG] = wrong_ticker
        temp_df.loc[:, TICKER_REAL] = real_ticker
        temp_df.loc[:, CUSIP_WRONG] = wrong_cusip
        temp_df.loc[:, CUSIP_REAL] = real_cusip
        temp_df.loc[:, WRONG_TICKER_SOURCE] = source
        temp_df.loc[:, COMPANY_NAME] = company_name
        temp_df.loc[:, IS_EVENT_DATE] = 0
        temp_df.loc[:, IS_EVENT_TOMORROW] = 0
        temp_df.loc[:, IS_EVENT_YESTERDAY] = 0
        index = (temp_df.index == date_today).nonzero()[0]
        if (temp_df.index == date_today).any():
            temp_df.ix[index[0], IS_EVENT_DATE] = 1

        index = (temp_df.index == date_tomorrow).nonzero()[0]
        if (temp_df.index == date_tomorrow).any():
            temp_df.ix[index[0], IS_EVENT_TOMORROW] = 1

        index = (temp_df.index == date_yesterday).nonzero()[0]
        if (temp_df.index == date_yesterday).any():
            temp_df.ix[index[0], IS_EVENT_YESTERDAY] = 1

        temp_df[DATE] = temp_df.index
        temp_df["{}_{}".format(IBES_NUM, REAL)] = temp_df[DATE].apply(lambda x: real_ibes_date[x.year])
        temp_df["{}_{}".format(IBES_NUM, WRONG)] = temp_df[DATE].apply(lambda x: wrong_ibes_date[x.year])
        result_list.append(temp_df)

    if result_list:
        if len(result_list) > 1:
            return pd.concat(result_list, axis=0, ignore_index=True)
        else:
            return result_list[0]
    else:
        return pd.DataFrame()


if __name__ == "__main__":
    ticker_values = ticker_group.groups.keys()

    process_num = 16
    pool = pathos.multiprocessing.ProcessingPool(process_num)


    def process_df(values):
        list_df = []
        for ticker in values:
            list_df.append(get_two_years_data(ticker))

        return pd.concat(list_df, ignore_index=True, axis=0)


    split_values = np.array_split(ticker_values, process_num)
    result_dfs = pool.map(process_df, split_values)
    result_df = pd.concat(result_dfs, ignore_index=True, axis=0)
    # result_df = process_df(ticker_values)
    result_df.to_csv('result_csv/wrong_ticker_whole_daily_data_SDC.csv', encoding='utf8')
    # result_df['TickerNum'] = result_df[WRONG_TICKER_SOURCE].apply(lambda x: re.findall(r'\d+', x)[0])
    source = result_df[WRONG_TICKER_SOURCE].apply(lambda x: x.split(' ')[-1])
    sub_df1 = result_df[source == 'initials']
    sub_df1.to_csv('result_csv/wrong_ticker_initial_daily_data_SDC.csv', encoding='utf8')
    ticker_num = sub_df1[WRONG_TICKER_SOURCE].apply(lambda x: int(re.findall(r'\d+', x)[0]))
    sub_df1 = sub_df1[ticker_num > 2]
    sub_df1.to_csv('result_csv/wrong_ticker_initial_over2_daily_data_SDC.csv', encoding='utf8')

    sub_df1 = result_df[source == 'letters']
    sub_df1.to_csv('result_csv/wrong_ticker_capital_daily_data_SDC.csv', encoding='utf8')

    sub_df1 = result_df[source == 'name']
    sub_df1.to_csv('result_csv/wrong_ticker_first_word_daily_data_SDC.csv', encoding='utf8')
