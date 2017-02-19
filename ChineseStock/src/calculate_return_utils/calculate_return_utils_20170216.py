#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: calculate_return_utils_20170216
# @Date: 2017-02-16
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import numpy as np
import pandas as pd

from ..account_portfolio.average_portfolio import AveragePortfolio
from ..account_portfolio.average_index_portfolio import AverageIndexPortfolio
from ..util_functions.util_function import load_stock_info
from calculate_return_utils_20170214 import CalculateReturnUtils20170214


class CalculateReturnUtils20170216(CalculateReturnUtils20170214):
    """ This file I add alpha test to structure and no neglect period """

    def __init__(self, trading_list_path=None):
        if trading_list_path is None:
            trading_list_path = self.TRADING_DAYS_20170216_PATH
        CalculateReturnUtils20170214.__init__(self, trading_list_path)
        # self.neglect_period = [datetime.datetime(1015, 7, 8), datetime.datetime(1016, 2, 1)]

    def calculate_portfolio_return(self, report_df, portfolio_num, transaction_cost=0):
        portfolio = AveragePortfolio(portfolio_num, total_value=self.initial_wealth,
                                     transaction_cost=transaction_cost, price_type=self.STOCK_CLOSE_PRICE)
        index_portfolio = AverageIndexPortfolio(portfolio_num=portfolio_num, initial_amount=self.initial_wealth,
                                                index_price_info=pd.read_pickle(self.SZ_399300_PATH),
                                                wealth_stock_type=self.STOCK_CLOSE_PRICE)
        buy_date_list = report_df[self.REPORT_BUY_DATE].sort_values()
        wealth_series = pd.Series()
        beta_strategies_series = pd.Series()

        for current_date in self.trading_days_list:

            info_index = buy_date_list[buy_date_list == current_date].index

            for i in info_index:
                short_end_date = report_df.ix[i, self.REPORT_SELL_DATE]

                buy_date = report_df.ix[i, self.REPORT_BUY_DATE]
                ticker = report_df.ix[i, self.REPORT_MARKET_TICKER]
                # market_type = return_df.ix[i, const.REPORT_MARKET_TYPE]
                buy_price_type = report_df.ix[i, self.REPORT_BUY_TYPE]
                sell_price_type = report_df.ix[i, self.REPORT_SELL_TYPE]

                if np.isnan(short_end_date) or ticker is None:
                    continue
                portfolio.short_stocks(buy_date=buy_date, end_date=short_end_date, buy_stock_type=buy_price_type,
                                       sell_stock_type=sell_price_type, stock_ticker=ticker)
                index_portfolio.short_index(short_date=current_date, short_type=buy_price_type,
                                            re_buy_date=short_end_date,
                                            re_buy_tpye=sell_price_type)

            wealth_series.loc[current_date] = portfolio.get_current_values(current_date)
            beta_strategies_series.loc[current_date] = index_portfolio.get_current_values(current_date)

        return wealth_series, beta_strategies_series

    def calculate_return_and_wealth(self, info):
        portfolio_num = info[self.PORTFOLIO_NUM]
        holding_days = info[self.HOLDING_DAYS]
        info_type = info[self.INFO_TYPE]
        return_path = info[self.REPORT_RETURN_PATH]
        wealth_path = info[self.WEALTH_DATA_PATH]
        report_path = info[self.REPORT_PATH]

        file_name = '{}_{}p_{}d'.format(info_type, portfolio_num, holding_days)

        if self.TRANSACTION_COST in info:
            transaction_cost = info[self.TRANSACTION_COST]
            file_name = '{}_{}cost'.format(file_name, int(transaction_cost * 1000))
        else:
            transaction_cost = 0

        if self.STOPLOSS_RATE in info:
            stoploss_rate = info[self.STOPLOSS_RATE]
            file_name = '{}_{}sr'.format(file_name, int(abs(stoploss_rate) * 100))
        else:
            stoploss_rate = None

        try:

            report_df = self.generate_buy_only_return_df(return_path, holding_days, info_type=info_type,
                                                         stoploss_rate=stoploss_rate, report_path=report_path)
        except Exception, err:
            import traceback
            traceback.print_exc()

            print info
            print 'Exception happened when report df'

            raise Exception(err)

        try:

            wealth_series, beta_strategies = self.calculate_portfolio_return(report_df, portfolio_num,
                                                                             transaction_cost=transaction_cost)
            wealth_series.to_pickle(os.path.join(wealth_path, '{}.p'.format(file_name)))
            beta_strategies.to_pickle(os.path.join(wealth_path, '{}_beta.p'.format(file_name)))

        except Exception, err:
            import traceback
            traceback.print_exc()

            print info
            print 'Exception happened when handle wealth series'

            raise Exception(err)

        return wealth_series

    def calculate_trade_info(self, announce_date, ticker_info, stoploss_rate, holding_days,
                             buy_price_type=None, sell_price_type=None, after_price_type=None,
                             stock_price_path=None):
        """
        This function used to calculate stock trading info, this function will neglect report info period during
         2015.7.8 to 2016.2.1 and will sell stock when current open stock price lower than the highest stock price,
         we will short this stock before hand
        :param announce_date: information announce date
        :param ticker_info: stock ticker
        :param holding_days: the days of holding
        :param sell_date: sell_date of target stock
        :param stoploss_rate: if this stock's today price is lower than this value, we will sell it.
        :return: a dict of temp result
        """

        temp_result = {self.REPORT_RETURN_RATE: np.nan, self.REPORT_SELL_DATE: np.nan,
                       self.REPORT_BUY_DATE: np.nan, self.REPORT_MARKET_TYPE: np.nan,
                       self.REPORT_MARKET_TICKER: np.nan, self.REPORT_BUY_PRICE: np.nan,
                       self.REPORT_SELL_TYPE: np.nan, self.REPORT_BUY_TYPE: np.nan,
                       }

        # Offer default parameter
        if buy_price_type is None:
            buy_price_type = self.STOCK_OPEN_PRICE

        if sell_price_type is None:
            sell_price_type = self.STOCK_CLOSE_PRICE

        if after_price_type is None:
            after_price_type = self.STOCK_OPEN_PRICE

        if stock_price_path is None:
            stock_price_path = self.STOCK_PRICE_20170214_PATH

        # Get buy day
        trading_days = self.trading_days_list[self.trading_days_list > announce_date].tolist()
        if len(trading_days) == 0:
            return pd.Series(temp_result)
        trade_day = trading_days[0]

        used_stock_data = load_stock_info(trade_day, ticker_info, price_path=stock_price_path)
        if used_stock_data.empty:
            return pd.Series(temp_result)

        buy_price = used_stock_data.loc[used_stock_data.first_valid_index(), buy_price_type]
        buy_date = used_stock_data.loc[used_stock_data.first_valid_index(), self.STOCK_DATE]
        highest_price = used_stock_data.loc[used_stock_data.first_valid_index(), self.STOCK_HIGH_PRICE]

        # During this period Report on Chinese stock is useless
        # if self.neglect_period[1] >= buy_date >= self.neglect_period[0]:
        #     return pd.Series(temp_result)

        # this means there are not enough days to finish this operation
        if len(trading_days) == 0:
            return pd.Series(temp_result)
        elif len(trading_days) < holding_days:
            sell_date = trading_days[-1]
        else:
            sell_date = trading_days[holding_days - 1]

        for date in trading_days[1:]:
            stock_info = load_stock_info(date, ticker_info, price_path=stock_price_path)
            if stock_info.empty:
                continue

            row = stock_info.loc[stock_info.first_valid_index()]

            current_price = row[self.STOCK_OPEN_PRICE]
            rate = current_price / highest_price - 1

            # if date > sell_date or self.neglect_period[1] >= date >= self.neglect_period[0]:
            if date > sell_date:
                sell_price = row[after_price_type]
                temp_result[self.REPORT_RETURN_RATE] = sell_price / buy_price - 1
                temp_result[self.REPORT_SELL_DATE] = date
                temp_result[self.REPORT_MARKET_TICKER] = row[self.STOCK_TICKER]
                temp_result[self.REPORT_BUY_DATE] = buy_date
                temp_result[self.REPORT_BUY_PRICE] = buy_price
                temp_result[self.REPORT_SELL_TYPE] = after_price_type
                temp_result[self.REPORT_BUY_TYPE] = buy_price_type
                return pd.Series(temp_result)

            elif date == sell_date or (stoploss_rate is not None and rate < stoploss_rate):
                sell_price = row[sell_price_type]
                temp_result[self.REPORT_RETURN_RATE] = sell_price / buy_price - 1
                temp_result[self.REPORT_SELL_DATE] = date
                temp_result[self.REPORT_MARKET_TICKER] = row[self.STOCK_TICKER]
                temp_result[self.REPORT_BUY_DATE] = buy_date
                temp_result[self.REPORT_BUY_PRICE] = buy_price
                temp_result[self.REPORT_SELL_TYPE] = sell_price_type
                temp_result[self.REPORT_BUY_TYPE] = buy_price_type
                return pd.Series(temp_result)

            highest_price = max(highest_price, row[self.STOCK_HIGH_PRICE])

        return pd.Series(temp_result)
