#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: calculate_return_utils_2
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd
import numpy as np

from portfolio import PortFolio
from constants import Constant as const
from calculate_return_utils import filter_df, load_stock_info, trading_day_list
from path_info import buy_only_report_data_path


def generate_buy_only_return_df(return_path, holding_days, info_type=None, drawback_rate=None):
    """
    This method only take buy only return into consideration
    :param return_path: the path where should save those return data
    :param holding_days: the holding days of buy wealth
    :param info_type: only keep target info type into consideration, like company, self, or others
    :param drawback_rate: the drawback rate of target info
    :return: the report data frame with return data.
    """
    # print return_path
    # print holding_days
    # print info_type
    # print drawback_rate
    file_path = os.path.join(return_path, 'buy_only_hdays_{}_return.p'.format(holding_days))
    if os.path.isfile(file_path):
        return filter_df(pd.read_pickle(file_path), info_type)

    report_list = os.listdir(buy_only_report_data_path)

    def process_report_df(row):
        ann_date = row[const.REPORT_ANNOUNCE_DATE]
        ticker = row[const.REPORT_TICKER]

        return calculate_trade_info(announce_date=ann_date, ticker_info=ticker[:6], market_info=ticker[-2:],
                                    holding_days=holding_days, drawdown_rate=drawback_rate)

    result_df_list = []

    for file_name in report_list:
        report_df = filter_df(pd.read_pickle(os.path.join(buy_only_report_data_path, file_name)), info_type)
        result_df_list.append(report_df.merge(report_df.apply(process_report_df, axis=1), left_index=True,
                                              right_index=True))

    result_df = pd.concat(result_df_list)
    result_df.to_pickle(file_path)
    return result_df


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


def calculate_portfolio_return(return_df, portfolio_num, transaction_cost=0):
    portfolio = PortFolio(portfolio_num, transaction_cost=transaction_cost)
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


def calculate_return_and_wealth(info):
    portfolio_num = info[const.PORTFOLIO_NUM]
    holding_days = info[const.HOLDING_DAYS]
    info_type = info[const.INFO_TYPE]
    return_path = info[const.REPORT_RETURN_PATH]
    wealth_path = info[const.WEALTH_DATA_PATH]

    file_name = '{}_{}p_{}d'.format(info_type, portfolio_num, holding_days)

    try:
        if const.TRANSACTION_COST in info:
            transaction_cost = info[const.TRANSACTION_COST]
            file_name = '{}_{}cost'.format(file_name, int(transaction_cost * 1000))
        else:
            transaction_cost = 0

        if const.DRAWDOWN_RATE in info:
            drawdown_rate = info[const.DRAWDOWN_RATE]
            file_name = '{}_{}down'.format(file_name, int(abs(drawdown_rate) * 100))
        else:
            drawdown_rate = None

        return_df = generate_buy_only_return_df(return_path, holding_days, info_type=info_type,
                                                drawback_rate=drawdown_rate)

        try:
            wealth_df = calculate_portfolio_return(return_df, portfolio_num, transaction_cost=transaction_cost)

        except Exception, err:
            print 'Error happend during generate wealth df'
            raise Exception(err)

        wealth_df.to_pickle(os.path.join(wealth_path, '{}.p'.format(file_name)))
    except Exception, err:
        import traceback
        traceback.print_exc()

        print info

        raise Exception(err)

    return wealth_df
