#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: test_function
# @Date: 2017-01-13
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import re

import pandas as pd
import numpy as np

from constant import Constant as const
from get_root_path import get_root_path

root_path = get_root_path()
temp_path = os.path.join(root_path, 'temp')
data_path = os.path.join(root_path, 'data')
stock_price_path = os.path.join(data_path, 'stock_price')
trading_day_list = pd.read_pickle(os.path.join(data_path, 'trading_days_list.p'))
buy_only_report_data_path = os.path.join(data_path, 'report_info_buy_only')


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


def generate_wealth_df(wealth_path, prefix):
    file_list = os.listdir(wealth_path)

    df = pd.DataFrame()

    for file_name in file_list:
        if not file_name.endswith('.p'):
            continue

        number = re.findall(r'\d+', file_name)
        column_name = '{}_{}portion_{}d'.format(prefix, number[0], number[1])
        new_column = pd.read_pickle(os.path.join(wealth_path, file_name))
        new_column = new_column * (10000.0 / new_column[0])
        df[column_name] = new_column

    return df


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
    """
    This method only take buy only return into consideration
    :param return_path: the path where should save those return data
    :param holding_days: the holding days of buy wealth
    :param info_type: only keep target info type into consideration, like company, self, or others
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


class Investment(object):
    """ This class is each investment account info """

    # end date use to mark the end date of one investment, if this variable is None means that current account is free.
    end_date = None

    # the final return rate of target stock
    return_rate = None

    # ticker of trade stock
    stock_ticker = None

    # 1 2 Shanghai A B, 4 8 Shenzhen A B, 16 GEM
    stock_type = None
    buy_price = None

    def __init__(self, amount, stock_price_type=const.STOCK_ADJPRCWD):
        self.amount = amount

        # stock price of previous day
        self.previous_price = None

        # this parameter are used to determine which price are used to calculate the final result
        self.stock_price_type = stock_price_type

    def is_free(self, current_date):
        """ Whether this investment account has free money """
        return self.end_date is None or current_date >= self.end_date

    def get_current_value(self, current_date):
        """ Given date info return the value of current date """

        # this means current investment is still in use
        if self.return_rate is not None:
            if self.is_free(current_date):

                # the final amount is calculated used return rate
                self.amount = self.amount * (1 + self.return_rate)

                # Clear unused data
                self.end_date = None
                self.return_rate = None
                self.buy_price = None
                self.stock_type = None
                self.buy_price = None
                self.previous_price = None

                amount = self.amount

            else:
                # based on the stock type to load target data
                if int(self.stock_type) in [1, 2]:
                    stock_info = load_stock_info(current_date, self.stock_ticker, 'SH')
                else:
                    stock_info = load_stock_info(current_date, self.stock_ticker, 'SZ')

                # this means no trading on target date, use previous data
                if stock_info.empty:
                    current_price = self.previous_price
                else:
                    current_price = stock_info.loc[stock_info.first_valid_index(), self.stock_price_type]
                    self.previous_price = current_price

                amount = self.amount * current_price / self.buy_price

        else:
            amount = self.amount

        return amount

    def short_stock(self, return_rate, end_date, buy_price, stock_type, stock_ticker):
        """ use this investment account to buy some stock """
        self.end_date = end_date
        self.return_rate = return_rate
        self.buy_price = buy_price
        self.stock_type = stock_type
        self.stock_ticker = stock_ticker
        self.previous_price = buy_price


class PortFolio(object):
    """ This is a simple portfolio class all investment should be equal """

    def __init__(self, total_num=10, total_value=10000.):
        every_amount = total_value / total_num
        self.account_list = []
        for i in range(total_num):
            new_account = Investment(every_amount)
            self.account_list.append(new_account)

    def get_current_values(self, current_date):
        """ get current investment value """
        amount = 0
        for account in self.account_list:
            amount += account.get_current_value(current_date)

        return amount

    def short_stocks(self, end_date, stock_return, current_date, buy_price, stock_ticker, stock_type):
        """ If there is a free account, buy target stock, else do nothing """
        account_index = self.__get_free_account(current_date)

        if account_index is None:
            return

        self.account_list[account_index].short_stock(stock_return, end_date, buy_price, stock_type, stock_ticker)

    def __get_free_account(self, current_date):
        """ get the index of free account """
        for i, account in enumerate(self.account_list):
            if account.is_free(current_date):
                account.get_current_value(current_date)
                return i

        return None
