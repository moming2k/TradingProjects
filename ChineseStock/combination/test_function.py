#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: test_function
# @Date: 2017-01-13
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd
import numpy as np

from constant import Constant as const

root_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'
stock_price_path = os.path.join(root_path, 'stock_price')
temp_path = os.path.join(root_path, 'temp')
trading_day_list = pd.read_pickle(os.path.join(temp_path, '20170108', 'trading_days_list.p'))


def load_stock_info(trade_date, ticker, market_type):
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


def calculate_trade_info(announce_date, ticker_info, market_info, holding_days=None, sell_date=None,
                         buy_price_type=const.STOCK_OPEN_PRICE, sell_price_type=const.STOCK_CLOSE_PRICE,
                         after_price_type=const.STOCK_OPEN_PRICE):
    """
    This function used to calculate stock trading info
    :param announce_date: information announce date
    :param ticker_info: stock ticker
    :param market_info: market type, should bd SZ or SH
    :param holding_days: the days of holding
    :param buy_price_type: use which price as buy
    :param sell_price_type: use which price as sell
    :param after_price_type: if target date is not trading day, use which price to sell
    :param sell_date: sell_date of target stock
    :return: a dict of temp result
    """

    if sell_date is None and holding_days is None:
        raise Exception('Neither sell_date or holding_days has value')
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

    buy_price = used_stock_data.loc[used_stock_data.first_valid_index(), buy_price_type]
    buy_date = used_stock_data.loc[used_stock_data.first_valid_index(), const.STOCK_DATE]

    # this means there are not enough days to finish this operation

    if holding_days is not None:
        if len(trading_days) < holding_days:
            return pd.Series(temp_result)

        sell_date = trading_days[holding_days - 1]

    sell_info = load_stock_info(sell_date, ticker_info, market_info)

    remain_days = trading_day_list[trading_day_list > sell_date]

    # There is no sell info on the end of holding days, we need to find the next trading days
    if sell_info.empty:
        for day in remain_days:
            sell_info = load_stock_info(day, ticker_info, market_info)
            if not sell_info.empty:
                # here use open price
                sell_price = sell_info.loc[sell_info.first_valid_index(), after_price_type]
                temp_result[const.REPORT_RETURN_RATE] = sell_price / buy_price - 1
                temp_result[const.REPORT_SELL_DATE] = day
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
        sell_price = sell_info.loc[sell_info.first_valid_index(), sell_price_type]
        temp_result[const.REPORT_RETURN_RATE] = sell_price / buy_price - 1
        temp_result[const.REPORT_SELL_DATE] = sell_info.loc[sell_info.first_valid_index(), const.STOCK_DATE]
        temp_result[const.REPORT_MARKET_TICKER] = sell_info.loc[sell_info.first_valid_index(),
                                                                const.STOCK_TICKER]
        temp_result[const.REPORT_MARKET_TYPE] = sell_info.loc[sell_info.first_valid_index(),
                                                              const.STOCK_MARKET_TYPE]
        temp_result[const.REPORT_BUY_DATE] = buy_date
        temp_result[const.REPORT_BUY_PRICE] = buy_price
        return pd.Series(temp_result)


def generate_buy_only_return_df(return_path, holding_days, info_type=None):
    file_path = os.path.join(return_path, 'buy_only_hdays_{}_return.p'.format(holding_days))
    if os.path.isfile(file_path):
        return pd.read_pickle(file_path)





def calculate_portfolio_return(return_df, portfolio_num):
    pass
