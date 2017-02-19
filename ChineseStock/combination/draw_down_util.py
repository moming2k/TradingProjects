#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: draw_down_util
# @Date: 2017-01-24
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd
import numpy as np

from constant import Constant as const
from get_root_path import data_path, buy_only_report_data_path
from util_functions import load_stock_info

trading_day_list = pd.read_pickle(os.path.join(data_path, '__trading_days_list.p'))


def calculate_trade_info(announce_date, ticker_info, market_info, drawdown_rate=None, holding_days=None,
                         sell_date=None):
    """
    This function used to calculate stock trading info, this function will
    :param announce_date: information announce date
    :param ticker_info: stock ticker
    :param market_info: market type, should bd SZ or SH
    :param holding_days: the days of holding
    :param sell_date: sell_date of target stock
    :param drawdown_rate: if this stock's today price is lower than this value, we will sell it.
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

    buy_price = used_stock_data.loc[used_stock_data.first_valid_index(), const.STOCK_ADJPRCWD]
    buy_date = used_stock_data.loc[used_stock_data.first_valid_index(), const.STOCK_DATE]

    # this means there are not enough days to finish this operation
    if holding_days is not None:
        if len(trading_days) == 0:
            return pd.Series(temp_result)
        elif len(trading_days) < holding_days:
            sell_date = trading_days[-1]
        else:
            sell_date = trading_days[holding_days - 1]

    for date in trading_days[1:]:
        stock_info = load_stock_info(date, ticker_info, market_info)
        if stock_info.empty:
            continue

        # print stock_info

        current_price = stock_info.loc[stock_info.first_valid_index(), const.STOCK_ADJPRCWD]
        rate = current_price / buy_price - 1

        if date >= sell_date or (drawdown_rate is not None and rate < drawdown_rate):
            sell_price = current_price
            temp_result[const.REPORT_RETURN_RATE] = sell_price / buy_price - 1
            temp_result[const.REPORT_SELL_DATE] = date
            temp_result[const.REPORT_MARKET_TICKER] = stock_info.loc[stock_info.first_valid_index(),
                                                                     const.STOCK_TICKER]
            temp_result[const.REPORT_MARKET_TYPE] = stock_info.loc[stock_info.first_valid_index(),
                                                                   const.STOCK_MARKET_TYPE]
            temp_result[const.REPORT_BUY_DATE] = buy_date
            temp_result[const.REPORT_BUY_PRICE] = buy_price
            return pd.Series(temp_result)

    return pd.Series(temp_result)


def generate_buy_only_return_df_add_drawback(return_path, holding_days, info_type=None, drawback_rate=None):
    """
    This method only take buy only return into consideration
    :param return_path: the path where should save those return data
    :param holding_days: the holding days of buy wealth
    :param info_type: only keep target info type into consideration, like company, self, or others
    :param drawback_rate: the drawback rate of target info
    :return: the report data frame with return data.
    """
    file_path = os.path.join(return_path, 'buy_only_hdays_{}_return.p'.format(holding_days))
    if os.path.isfile(file_path):
        return pd.read_pickle(file_path)

    report_list = os.listdir(buy_only_report_data_path)

    def process_report_df(row):
        ann_date = row[const.REPORT_ANNOUNCE_DATE]
        ticker = row[const.REPORT_TICKER]

        return calculate_trade_info(announce_date=ann_date, ticker_info=ticker[:6], market_info=ticker[-2:],
                                    holding_days=holding_days, drawdown_rate=drawback_rate)

    result_df_list = []

    for file_name in report_list:
        report_df = pd.read_pickle(os.path.join(buy_only_report_data_path, file_name))
        if info_type == 'company':
            report_df = report_df[report_df[const.REPORT_TYPE] == const.COMPANY]

        elif hasattr(info_type, 'startswith') and info_type.startswith('senior'):
            report_df = report_df[report_df[const.REPORT_TYPE] == const.SENIOR]

            if info_type.endswith('self'):
                report_df = report_df[report_df[const.REPORT_RELATIONSHIP] == const.SELF]

            elif info_type.endswith('brothers'):
                report_df = report_df[report_df[const.REPORT_RELATIONSHIP] == const.BROTHERS]

            elif info_type.endswith('parents'):
                report_df = report_df[report_df[const.REPORT_RELATIONSHIP] != const.BROTHERS]
                report_df = report_df[report_df[const.REPORT_RELATIONSHIP] != const.SELF]
                report_df = report_df[report_df[const.REPORT_RELATIONSHIP] != const.SPOUSE]
                report_df = report_df[report_df[const.REPORT_RELATIONSHIP] != const.OTHERS]
                report_df = report_df[report_df[const.REPORT_RELATIONSHIP] != const.OTHER_RELATIONS]

            elif info_type.endswith('spouse'):
                report_df = report_df[report_df[const.REPORT_RELATIONSHIP] != const.SPOUSE]

        result_df_list.append(report_df.merge(report_df.apply(process_report_df, axis=1), left_index=True,
                                              right_index=True))

    result_df = pd.concat(result_df_list)
    result_df.to_pickle(file_path)
    return result_df
