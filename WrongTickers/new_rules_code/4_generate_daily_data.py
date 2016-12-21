#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: 4_generate_daily_data
# @Date: 2016-12-18
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd
import numpy as np
from pandas.tseries.offsets import CustomBusinessDay
from pandas.tseries.holiday import USFederalHolidayCalendar

from constants import *

days = 30

# today_str = datetime.datetime.today().strftime('%Y%m%d')
today_str = '20161218'
root_path = '/home/wangzg/Documents/WangYouan/research/Wrong_tickers'

temp_path = os.path.join(root_path, 'temp')
today_temp_path = os.path.join(temp_path, today_str)
data_path = os.path.join(root_path, 'data')
result_path = os.path.join(root_path, 'result_csv')
stock_data_path = os.path.join(root_path, 'Stock_data')

if not os.path.isdir(today_temp_path):
    os.makedirs(today_temp_path)

ibes_df = pd.read_csv(os.path.join(result_path, 'IBES_EPS_NUMSET_COUNT.csv'),
                      usecols=['CUSIP', 'OFTIC', 'YEAR', 'NUMEST'],
                      dtype={'CUSIP': str, "YEAR": int, 'NUMEST': int})

bkvlps_df = pd.read_csv(os.path.join(stock_data_path, 'BKVLPS.csv'),
                        usecols=['fyear', 'cusip', 'bkvlps', 'tic'],
                        dtype={'fyear': str, 'cusip': str},
                        )

volatility_df = pd.read_csv(os.path.join(stock_data_path, 'daily_stock_volatility.csv'))
volume_df = pd.read_csv(os.path.join(stock_data_path, 'daily_volume.csv'))
return_df = pd.read_csv(os.path.join(stock_data_path, 'daily_market_return.csv'))

bday_us = CustomBusinessDay(calendar=USFederalHolidayCalendar())


def get_information_in_CRSP(cusip, ticker, start_date, end_date, info_type):
    date_col_name = 'date'
    if info_type == VOLUME:
        ticker_path = os.path.join(stock_data_path, info_type.lower(), '{}_VOL.csv'.format(ticker))
        cusip_path = os.path.join(stock_data_path, "{}_cusip".format(info_type.lower()), '{}_VOL.csv'.format(ticker))
        use_cols = [date_col_name, 'VOL']
        data_type = {date_col_name: str}

    elif info_type == PRICE:
        ticker_path = os.path.join(stock_data_path, info_type.lower(), '{}_PRC.csv'.format(ticker))
        cusip_path = os.path.join(stock_data_path, "{}_cusip".format(info_type.lower()), '{}_PRC.csv'.format(ticker))
        use_cols = [date_col_name, 'PRC']
        data_type = {date_col_name: str}

    elif info_type == PRICE_RANGE:
        ticker_path = os.path.join(stock_data_path, 'highlow', '{}_HL.csv'.format(ticker))
        cusip_path = os.path.join(stock_data_path, "highlow_cusip", '{}_HL.csv'.format(ticker))
        use_cols = [date_col_name, 'BIDLO', 'ASKHI']
        data_type = {date_col_name: str}

    elif info_type == COMPUSTAT:
        ticker_path = os.path.join(stock_data_path, info_type.lower(), '{}_COMPU.csv'.format(ticker))
        cusip_path = os.path.join(stock_data_path, "{}_cusip".format(info_type.lower()), '{}_COMPU.csv'.format(ticker))
        date_col_name = 'datadate'
        use_cols = [date_col_name, 'divd', 'cshoc', 'eps', 'trfd', 'exchg']
        data_type = {date_col_name: str}

    elif info_type == LOG_RETURN:
        ticker_path = os.path.join(stock_data_path, 'logReturn', '{}_LR.csv'.format(ticker))
        cusip_path = "not exist"
        use_cols = [date_col_name, 'LR']
        data_type = {date_col_name: str}

    elif info_type == SIMPLE_RETURN:
        ticker_path = os.path.join(stock_data_path, 'simpleReturn', '{}_SR.csv'.format(ticker))
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


def get_two_years_data(group):
    row = group.iloc[0]
    real_ticker = row[TICKER_REAL]
    real_cusip = row[CUSIP_REAL]
    date_today = row[DATE_TODAY]
    source = row[WRONG_TICKER_SOURCE]
    company_name = row[COMPANY_NAME]
    wrong_ticker = row[TICKER_WRONG]
    wrong_cusip = row[CUSIP_WRONG]

    date_yesterday = date_today - bday_us
    date_tomorrow = date_today + bday_us

    start_date = date_today - bday_us * days
    end_date = date_today + bday_us * days
    real_df = get_range_info(real_cusip, real_ticker, start_date, end_date)
    if real_df.empty:
        return pd.DataFrame()

    real_ibes_date = {date_today.year: get_ibes_info(real_cusip, real_ticker, date_today.year),
                      date_today.year - 1: get_ibes_info(real_cusip, real_ticker, date_today.year - 1),
                      date_today.year + 1: get_ibes_info(real_cusip, real_ticker, date_today.year + 1),
                      }

    if PRICE_HIGH in real_df.keys() and PRICE_LOW in real_df.keys():
        real_df[PRICE_RANGE] = real_df[PRICE_HIGH] - real_df[PRICE_LOW]
    wrong_df = get_range_info(cusip=wrong_cusip, ticker=wrong_ticker,
                              start_date=start_date, end_date=end_date)

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
    return temp_df


def get_bkvlps_from_row_info(row):
    year = row[DATE][:4]
    wrong_ticker = row[TICKER_WRONG]
    wrong_cusip = row[CUSIP_WRONG]
    sub_df = bkvlps_df[bkvlps_df['fyear'] == year]
    if sub_df.empty:
        return np.nan
    target_list = sub_df[sub_df['cusip'] == wrong_cusip].bkvlps.tolist()
    if target_list:
        return target_list[0]

    target_list = sub_df[sub_df['tic'] == wrong_ticker].bkvlps.tolist()
    if target_list:
        return target_list[0]

    else:
        return np.nan


if __name__ == '__main__':
    pair_2a2b_useful_df = pd.read_pickle(os.path.join(today_temp_path, 'pair_2a_2b_useful.p'))
    pair_4a_useful_df = pd.read_pickle(os.path.join(today_temp_path, 'pair_4a_useful.p'))

    # pair_2a2b_useful_df[DATE_TODAY] = pair_2a2b_useful_df[DATE_TODAY].apply(
    #     lambda x: datetime.datetime.strptime(x, '%Y-%m-%d')
    # )
    #
    # pair_4a_useful_df[DATE_TODAY] = pair_4a_useful_df[DATE_TODAY].apply(
    #     lambda x: datetime.datetime.strptime(x, '%Y-%m-%d')
    # )

    pair_4a_daily = pair_4a_useful_df.groupby(CUSIP_REAL, group_keys=False).apply(
        get_two_years_data).reset_index(drop=True)
    pair_2a2b_daily = pair_2a2b_useful_df.groupby(CUSIP_REAL, group_keys=False).apply(
        get_two_years_data).reset_index(drop=True)

    pair_4a_daily.to_pickle(os.path.join(today_temp_path, 'pair_4a_{}_daily.p'.format(days)))
    pair_2a2b_daily.to_pickle(os.path.join(today_temp_path, 'pair_2a2b_{}_daily.p'.format(days)))

    data_df = pair_2a2b_daily
    data_df[DATE] = data_df[DATE].apply(lambda x: x.strftime('%Y-%m-%d') if hasattr(x, 'strftime') else x)
    data_df[DAILY_MARKET_RETURN] = data_df[DATE].apply(
        lambda x: return_df.loc[x, DAILY_MARKET_RETURN] if x in return_df.index else np.nan)
    data_df[DAILY_MARKET_TRADING_VOL] = data_df[DATE].apply(
        lambda x: volume_df.loc[x, DAILY_MARKET_TRADING_VOL] if x in volume_df.index else np.nan)
    data_df[DAILY_VOLATILITY] = data_df[DATE].apply(
        lambda x: volatility_df.loc[x, DAILY_VOLATILITY] if x in volatility_df.index else np.nan)
    data_df['{}_{}'.format(BOOK_VALUE_PER_SHARE, WRONG)] = data_df.apply(get_bkvlps_from_row_info, axis=1)
    data_df.to_pickle(os.path.join(today_temp_path, 'pair_2a2b_days_{}_add_market_data.p'.format(days)))

    data_df = pair_4a_daily
    data_df[DATE] = data_df[DATE].apply(lambda x: x.strftime('%Y-%m-%d') if hasattr(x, 'strftime') else x)
    data_df[DAILY_MARKET_RETURN] = data_df[DATE].apply(
        lambda x: return_df.loc[x, DAILY_MARKET_RETURN] if x in return_df.index else np.nan)
    data_df[DAILY_MARKET_TRADING_VOL] = data_df[DATE].apply(
        lambda x: volume_df.loc[x, DAILY_MARKET_TRADING_VOL] if x in volume_df.index else np.nan)
    data_df[DAILY_VOLATILITY] = data_df[DATE].apply(
        lambda x: volatility_df.loc[x, DAILY_VOLATILITY] if x in volatility_df.index else np.nan)
    data_df['{}_{}'.format(BOOK_VALUE_PER_SHARE, WRONG)] = data_df.apply(get_bkvlps_from_row_info, axis=1)
    data_df.to_pickle(os.path.join(today_temp_path, 'pair_4a_days_{}_add_market_data.p'.format(days)))
