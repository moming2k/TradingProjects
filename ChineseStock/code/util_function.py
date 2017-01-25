#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: util_function
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from constants import Constant
from path_info import stock_price_path

const = Constant()


def load_stock_info(trade_date, ticker, market_type):
    """
    Load stock info
    :param trade_date: datetime type
    :param ticker: '000001'
    :param market_type: SZ of SH
    :return: stock data info
    """
    if not os.path.isfile(os.path.join(stock_price_path, '{}.p'.format(trade_date.strftime('%Y%m%d')))):
        return pd.DataFrame()
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


def merge_result(result_path):
    file_list = os.listdir(result_path)

    df = pd.DataFrame()

    for file_name in file_list:
        if not file_name.endswith('.p'):
            continue

        column_name = file_name[:-2]
        new_column = pd.read_pickle(os.path.join(result_path, file_name))
        new_column *= (10000.0 / new_column[0])
        df[column_name] = new_column

    return df
