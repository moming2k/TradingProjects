#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step1_generate_return_data_no_short_all_command
# @Date: 2017-01-06
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

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

if not os.path.isdir(today_path):
    os.makedirs(today_path)

# read data file
stock_data = pd.read_pickle(os.path.join(temp_path, '20170106', 'daily_0516.p'))
report_info = pd.read_excel(os.path.join(data_path, 'insider2007_2016.xlsx'))

# here we only concern this action
useful_report = report_info[report_info[const.REPORT_ACTION] == const.OVERWEIGHT]

# holding days info
holding_days = 66

# get trading days
trading_day_list = stock_data[const.STOCK_DATE].drop_duplicates().sort_values().reset_index(drop=True)


def doing_trading_information(row):
    announce_date = row[const.REPORT_ANNOUNCE_DATE]
    ticker = row[const.REPORT_TICKER]
    market_info = ticker[-2:]
    ticker_info = ticker[:6]

    used_stock_data = stock_data[stock_data[const.STOCK_TICKER] == ticker_info]

    temp_result = {const.REPORT_RETURN_RATE: np.nan, const.REPORT_SELL_DATE: np.nan,
                   const.REPORT_BUY_DATE: np.nan, const.REPORT_MARKET_TYPE: np.nan,
                   const.REPORT_MARKET_TICKER: np.nan, const.REPORT_BUY_PRICE: np.nan}

    if used_stock_data.empty:
        return pd.Series(temp_result)

    # use different data based on market type
    if market_info == 'SZ':
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 1]
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 2]

    else:
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 4]
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 8]
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 16]

    if used_stock_data.empty:
        return pd.Series(temp_result)

    # Get buy day
    trading_days = trading_day_list[trading_day_list > announce_date].tolist()
    if len(trading_days) == 0:
        return pd.Series(temp_result)
    trade_day = trading_days[0]
    buy_info = used_stock_data[used_stock_data[const.STOCK_DATE] == trade_day]
    if buy_info.empty:
        return pd.Series(temp_result)

    buy_price = buy_info.loc[buy_info.first_valid_index(), const.STOCK_OPEN_PRICE]
    buy_date = buy_info.loc[buy_info.first_valid_index(), const.STOCK_DATE]

    # this means there are not enough days to finish this operation
    if len(trading_days) < holding_days:
        return pd.Series(temp_result)

    sell_day = trading_days[holding_days - 1]
    sell_info = used_stock_data[used_stock_data[const.STOCK_DATE] == sell_day]

    # There is no sell info on the end of holding days, we need to find the next trading days
    if sell_info.empty:
        for day in trading_days[holding_days:]:
            sell_info = used_stock_data[used_stock_data[const.STOCK_DATE] == day]
            if not sell_info.empty:

                # here use open price
                sell_price = sell_info.loc[sell_info.first_valid_index(), const.STOCK_OPEN_PRICE]
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
        sell_price = sell_info.loc[sell_info.first_valid_index(), const.STOCK_CLOSE_PRICE]
        temp_result['return'] = sell_price / buy_price - 1
        temp_result['sell_date'] = sell_info.loc[sell_info.first_valid_index(), const.STOCK_DATE]
        temp_result[const.REPORT_MARKET_TICKER] = sell_info.loc[sell_info.first_valid_index(),
                                                                const.STOCK_TICKER]
        temp_result[const.REPORT_MARKET_TYPE] = sell_info.loc[sell_info.first_valid_index(),
                                                              const.STOCK_MARKET_TYPE]
        temp_result[const.REPORT_BUY_DATE] = buy_date
        temp_result[const.REPORT_BUY_PRICE] = buy_price
        return pd.Series(temp_result)


result_df = useful_report.merge(useful_report.apply(doing_trading_information, axis=1), left_index=True,
                                right_index=True)
result_df.to_pickle(os.path.join(today_path, 'insider_add_return_hday_{}_ow_only.p'.format(holding_days)))
