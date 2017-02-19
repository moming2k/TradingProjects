#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: step3_calculate_return_data_nd
# Author: warn
# Date: warn

import os
import datetime

import pandas as pd
import numpy as np

from constant import Constant

const = Constant()

# Define some folder path
today_str = datetime.datetime.today().strftime('%Y%m%d')
root_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'
data_path = os.path.join(root_path, 'data')
temp_path = os.path.join(root_path, 'temp')
today_path = os.path.join(temp_path, today_str)
stock_price_path = os.path.join(root_path, 'stock_price')

if not os.path.isdir(today_path):
    os.makedirs(today_path)

# read data file
trading_day_list = pd.read_pickle(os.path.join(temp_path, '20170108', '__trading_days_list.p'))

holding_days = 22


def load_stock_info(trade_date, ticker, market_type):
    trade_day_stock_df = pd.read_pickle(os.path.join(stock_price_path, '{}.p'.format(trade_date.strftime('%Y%m%d'))))
    used_stock_data = trade_day_stock_df[trade_day_stock_df[const.STOCK_TICKER] == ticker]

    # use different data based on market type
    if market_type == 'SZ':
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 1]
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 2]

    else:
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 4]
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 8]
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 16]

    return used_stock_data


def calculate_trade_info(row):
    announce_date = row[const.REPORT_ANNOUNCE_DATE]
    ticker = row[const.REPORT_TICKER]
    market_info = ticker[-2:]
    ticker_info = ticker[:6]

    temp_result = {const.REPORT_RETURN_RATE: np.nan, const.REPORT_SELL_DATE: np.nan,
                   const.REPORT_BUY_DATE: np.nan, const.REPORT_MARKET_TYPE: np.nan,
                   const.REPORT_MARKET_TICKER: np.nan, const.REPORT_BUY_PRICE: np.nan}

    # Get buy day
    trading_days = trading_day_list[trading_day_list > announce_date].tolist()
    if len(trading_days) == 0:
        return pd.Series(temp_result)
    trade_day = trading_days[0]

    used_stock_data = load_stock_info(trade_day, ticker_info, market_info)
    if used_stock_data.empty:
        return pd.Series(temp_result)

    buy_price = used_stock_data.loc[used_stock_data.first_valid_index(), const.STOCK_ADJPRCND]
    buy_date = used_stock_data.loc[used_stock_data.first_valid_index(), const.STOCK_DATE]

    # this means there are not enough days to finish this operation
    if len(trading_days) < holding_days:
        return pd.Series(temp_result)

    sell_day = trading_days[holding_days - 1]
    sell_info = load_stock_info(sell_day, ticker_info, market_info)

    # There is no sell info on the end of holding days, we need to find the next trading days
    if sell_info.empty:
        for day in trading_days[holding_days:]:
            sell_info = load_stock_info(day, ticker_info, market_info)
            if not sell_info.empty:
                # here use open price
                sell_price = sell_info.loc[sell_info.first_valid_index(), const.STOCK_ADJPRCND]
                temp_result['return'] = sell_price / buy_price - 1
                temp_result['sell_date'] = day
                temp_result[const.REPORT_MARKET_TICKER] = sell_info.loc[sell_info.first_valid_index(),
                                                                        const.STOCK_TICKER]
                temp_result[const.REPORT_MARKET_TYPE] = sell_info.loc[sell_info.first_valid_index(),
                                                                      const.STOCK_MARKET_TYPE]
                temp_result[const.REPORT_BUY_DATE] = buy_date
                temp_result[const.REPORT_BUY_PRICE] = buy_price
                return pd.Series(temp_result)

        return pd.Series(temp_result)

    else:

        # use close price
        sell_price = sell_info.loc[sell_info.first_valid_index(), const.STOCK_ADJPRCND]
        temp_result['return'] = sell_price / buy_price - 1
        temp_result['sell_date'] = sell_info.loc[sell_info.first_valid_index(), const.STOCK_DATE]
        temp_result[const.REPORT_MARKET_TICKER] = sell_info.loc[sell_info.first_valid_index(),
                                                                const.STOCK_TICKER]
        temp_result[const.REPORT_MARKET_TYPE] = sell_info.loc[sell_info.first_valid_index(),
                                                              const.STOCK_MARKET_TYPE]
        temp_result[const.REPORT_BUY_DATE] = buy_date
        temp_result[const.REPORT_BUY_PRICE] = buy_price
        return pd.Series(temp_result)


if __name__ == '__main__':
    import pathos

    process_num = 10
    pool = pathos.multiprocessing.ProcessingPool(process_num)

    report_info = pd.read_excel(os.path.join(data_path, 'insider2007_2016.xlsx'))
    spilt_dfs = np.array_split(report_info, process_num)


    def process_df(df):
        return df.merge(df.apply(calculate_trade_info, axis=1), left_index=True,
                        right_index=True)


    result_dfs = pool.map(process_df, spilt_dfs)
    result_df = pd.concat(result_dfs, axis=0)

    result_df.to_pickle(os.path.join(today_path, '{}_nd_hday_{}.p'.format(today_str, holding_days)))
    result_df.to_csv(os.path.join(today_path, '{}_nd_hday_{}.csv'.format(today_str, holding_days)), encoding='utf8')
