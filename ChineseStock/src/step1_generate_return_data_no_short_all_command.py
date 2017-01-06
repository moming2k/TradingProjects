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

today_str = datetime.datetime.today().strftime('%Y-%m-%d')
root_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'
data_path = os.path.join(root_path, 'data')
temp_path = os.path.join(root_path, 'temp')
today_path = os.path.join(temp_path, today_str)
stock_data = pd.read_pickle(os.path.join(temp_path, '20170106', 'daily_0516.p'))

report_info = pd.read_excel(os.path.join(data_path, 'insider2007_2016.xlsx'))

# here we only concern this action
useful_report = report_info[report_info[const.REPORT_ACTION] == const.OVERWEIGHT]

holding_days = 22

trading_day_list = stock_data[const.STOCK_DATE].drop_duplicates().sort_values().reset_index(drop=True)


def doing_trading_information(row):
    announce_date = row[const.REPORT_ANNOUNCE_DATE]
    ticker = row[const.REPORT_TICKER]
    market_info = ticker[-2:]
    ticker_info = ticker[:6]

    used_stock_data = stock_data[stock_data[const.STOCK_TICKER] == ticker_info]

    if used_stock_data.empty:
        return np.nan

    if market_info == 'SZ':
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 1]
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 2]

    else:
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 4]
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 8]
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 16]

    if used_stock_data.empty:
        return np.nan

    trading_days = trading_day_list[trading_day_list > announce_date].tolist()
    if len(trading_days) == 0:
        return np.nan
    trade_day = trading_days[0]
    buy_info = used_stock_data[used_stock_data[const.STOCK_DATE] == trade_day]
    if buy_info.empty:
        return np.nan

    buy_price = buy_info.loc[buy_info.first_valid_index(), const.STOCK_OPEN_PRICE]

    if len(trading_days) < holding_days:
        return np.nan
    sell_day = trading_days[holding_days - 1]
    sell_info = used_stock_data[used_stock_data[const.STOCK_DATE] == sell_day]
    if sell_info.empty:
        for day in trading_days[holding_days:]:
            sell_info = used_stock_data[used_stock_data[const.STOCK_DATE] == day]
            if not sell_info.empty:
                sell_price = sell_info.loc[sell_info.first_valid_index(), const.STOCK_OPEN_PRICE]
                return sell_price / buy_price - 1

        return np.nan

    else:
        sell_price = sell_info.loc[sell_info.first_valid_index(), const.STOCK_CLOSE_PRICE]
        return sell_price / buy_price - 1


useful_report['return'] = useful_report.apply(doing_trading_information, axis=1)
useful_report.to_pickle(os.path.join(today_path, 'insider_add_return.p'))
