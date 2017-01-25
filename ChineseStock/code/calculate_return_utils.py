#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: calculate_return_utils
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd
import numpy as np

from constants import Constant as const
from path_info import trading_day_list, buy_only_report_data_path
from util_function import load_stock_info
from portfolio import PortFolio


def calculate_trade_info(announce_date, ticker_info, market_info, holding_days=None, sell_date=None,
                         buy_price_type=const.STOCK_ADJPRCWD, sell_price_type=const.STOCK_ADJPRCWD,
                         after_price_type=const.STOCK_ADJPRCWD):
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


def generate_buy_only_return_df(return_path, holding_days, info_type=None, drawback_rate=None):
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
                                    holding_days=holding_days, buy_price_type=const.STOCK_ADJPRCWD,
                                    sell_price_type=const.STOCK_ADJPRCWD, after_price_type=const.STOCK_ADJPRCWD)

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


def calculate_trade_info_drawdown(announce_date, ticker_info, market_info, drawdown_rate=None, holding_days=None,
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

        return calculate_trade_info_drawdown(announce_date=ann_date, ticker_info=ticker[:6], market_info=ticker[-2:],
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


def calculate_portfolio_return(return_df, portfolio_num):
    portfolio = PortFolio(portfolio_num)
    ann_days = return_df[const.REPORT_ANNOUNCE_DATE].sort_values()

    wealth_df = pd.Series()

    for current_date in trading_day_list:

        info_index = ann_days[ann_days == current_date].index

        for i in info_index:
            short_end_date = return_df.ix[i, const.REPORT_SELL_DATE]
            short_return_rate = return_df.ix[i, const.REPORT_RETURN_RATE]

            buy_date = return_df.ix[i, const.REPORT_BUY_DATE]
            ticker = return_df.ix[i, const.REPORT_MARKET_TICKER]
            market_type = return_df.ix[i, const.REPORT_MARKET_TYPE]
            buy_price = return_df.ix[i, const.REPORT_BUY_PRICE]

            if np.isnan(short_return_rate) or ticker is None:
                continue
            portfolio.short_stocks(short_end_date, short_return_rate, buy_date, buy_price=buy_price,
                                   stock_ticker=ticker, stock_type=market_type)

        wealth_df.loc[current_date] = portfolio.get_current_values(current_date)

    return wealth_df
