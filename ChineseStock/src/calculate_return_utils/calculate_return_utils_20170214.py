#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: calculate_return_utils_20170214
# @Date: 2017-02-14
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os

import numpy as np
import pandas as pd

from ..account_portfolio.average_portfolio import AveragePortfolio
from ..constants import Constant
from ..constants.path_info import Path
from ..util_functions.util_function import load_stock_info


class CalculateReturnUtils20170214(Constant, Path):
    def __init__(self, trading_list_path=None, stock_price_path=None):
        if trading_list_path is None:
            trading_list_path = self.TRADING_DAYS_20170214_PATH

        self._trading_days_list = pd.read_pickle(trading_list_path)
        self._stock_price_path = self.STOCK_PRICE_20170214_PATH if stock_price_path is None else stock_price_path
        self._temp_result = {self.REPORT_RETURN_RATE: None, self.REPORT_SELL_DATE: None,
                             self.REPORT_BUY_DATE: None, self.REPORT_MARKET_TYPE: None,
                             self.REPORT_MARKET_TICKER: None, self.REPORT_BUY_PRICE: None,
                             self.REPORT_SELL_TYPE: None, self.REPORT_BUY_TYPE: None,
                             }

    def filter_df(self, df, info_type=None):
        result_df = df.copy()
        if info_type == 'company':
            result_df = result_df[result_df[self.REPORT_TYPE] == self.COMPANY]

        elif hasattr(info_type, 'startswith') and info_type.startswith('exe'):
            result_df = result_df[result_df[self.REPORT_TYPE] == self.SENIOR]

            if info_type.endswith('self'):
                result_df = result_df[result_df[self.REPORT_RELATIONSHIP] == self.SELF]

            elif info_type.endswith('brothers'):
                result_df = result_df[result_df[self.REPORT_RELATIONSHIP] == self.BROTHERS]

            elif info_type.endswith('parents'):
                parents_df = result_df[result_df[self.REPORT_RELATIONSHIP] == self.PARENTS]
                father_df = result_df[result_df[self.REPORT_RELATIONSHIP] == self.FATHER]
                mother_df = result_df[result_df[self.REPORT_RELATIONSHIP] == self.MOTHER]
                result_df = pd.concat([parents_df, father_df, mother_df])

            elif info_type.endswith('spouse'):
                result_df = result_df[result_df[self.REPORT_RELATIONSHIP] == self.SPOUSE]

        return result_df

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

        temp_result = self._temp_result.copy()

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
        trading_days = self._trading_days_list[self._trading_days_list > announce_date].tolist()
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
        if self.neglect_period[1] >= buy_date >= self.neglect_period[0]:
            return pd.Series(temp_result)

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

            if date > sell_date or self.neglect_period[1] >= date >= self.neglect_period[0]:
                sell_price = row[after_price_type]
                temp_result[self.REPORT_RETURN_RATE] = sell_price / buy_price - 1
                temp_result[self.REPORT_SELL_DATE] = date
                temp_result[self.REPORT_MARKET_TICKER] = row[self.STOCK_TICKER]
                temp_result[self.REPORT_BUY_DATE] = buy_date
                temp_result[self.REPORT_BUY_PRICE] = buy_price
                return pd.Series(temp_result)

            elif date == sell_date or (stoploss_rate is not None and rate < stoploss_rate):
                sell_price = row[sell_price_type]
                temp_result[self.REPORT_RETURN_RATE] = sell_price / buy_price - 1
                temp_result[self.REPORT_SELL_DATE] = date
                temp_result[self.REPORT_MARKET_TICKER] = row[self.STOCK_TICKER]
                temp_result[self.REPORT_BUY_DATE] = buy_date
                temp_result[self.REPORT_BUY_PRICE] = buy_price
                return pd.Series(temp_result)

            highest_price = max(highest_price, row[self.STOCK_HIGH_PRICE])

        return pd.Series(temp_result)

    def generate_buy_only_return_df(self, return_path, holding_days, info_type=None, stoploss_rate=None,
                                    report_path=None):
        """
        This method only take buy only return into consideration
        :param return_path: the path where should save those return data
        :param holding_days: the holding days of buy wealth
        :param info_type: only keep target info type into consideration, like company, self, or others
        :param stoploss_rate: the drawback rate of target info
        :return: the report data frame with return data.
        """
        # print return_path
        # print holding_days
        # print info_type
        # print stoploss_rate
        if info_type is None:
            info_type = self.ALL

        if report_path is None:
            report_path = self.REPORT_20170214_PATH

        file_path = os.path.join(return_path, 'hdays_{}_report.p'.format(holding_days))
        if os.path.isfile(file_path):
            report_df = self.filter_df(pd.read_pickle(file_path), info_type)
            return report_df

        report_list = os.listdir(report_path)

        def process_report_df(row):
            ann_date = row[self.REPORT_ANNOUNCE_DATE]
            ticker = row[self.REPORT_TICKER]

            return self.calculate_trade_info(announce_date=ann_date, ticker_info=ticker[:6],
                                             holding_days=holding_days, stoploss_rate=stoploss_rate,
                                             buy_price_type=self.STOCK_OPEN_PRICE,
                                             sell_price_type=self.STOCK_CLOSE_PRICE,
                                             after_price_type=self.STOCK_OPEN_PRICE)

        result_df_list = []

        for file_name in report_list:
            report_df = self.filter_df(pd.read_pickle(os.path.join(report_path, file_name)), info_type)
            if self.REPORT_MARKET_TICKER in report_df.keys():
                report_df[self.REPORT_TICKER] = report_df[self.REPORT_MARKET_TICKER]
                del report_df[self.REPORT_MARKET_TICKER]
            tmp_df = report_df.merge(report_df.apply(process_report_df, axis=1), left_index=True,
                                     right_index=True)
            if self.REPORT_TICKER in tmp_df.keys():
                del tmp_df[self.REPORT_TICKER]
            if not tmp_df.empty:
                result_df_list.append(tmp_df)

        result_df = pd.concat(result_df_list).reset_index(drop=True)
        if info_type == self.ALL:
            result_df.to_pickle(file_path)
        return result_df

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

            wealth_series = self.calculate_portfolio_return(report_df, portfolio_num, transaction_cost=transaction_cost)
            wealth_series.to_pickle(os.path.join(wealth_path, '{}.p'.format(file_name)))

        except Exception, err:
            import traceback
            traceback.print_exc()

            print info
            print 'Exception happened when handle wealth series'

            raise Exception(err)

        return wealth_series

    def calculate_portfolio_return(self, report_df, portfolio_num, transaction_cost=0):
        portfolio = AveragePortfolio(portfolio_num, total_value=self.initial_wealth,
                                     transaction_cost=transaction_cost, price_type=self.STOCK_CLOSE_PRICE)
        buy_date_list = report_df[self.REPORT_BUY_DATE].sort_values()

        wealth_series = pd.Series()

        for current_date in self._trading_days_list:

            info_index = buy_date_list[buy_date_list == current_date].index

            for i in info_index:
                short_end_date = report_df.ix[i, self.REPORT_SELL_DATE]

                buy_date = report_df.ix[i, self.REPORT_BUY_DATE]
                ticker = report_df.ix[i, self.REPORT_MARKET_TICKER]
                # market_type = return_df.ix[i, const.REPORT_MARKET_TYPE]
                buy_price_type = report_df.ix[i, self.REPORT_BUY_TYPE]
                sell_price_type = report_df.ix[i, self.REPORT_SELL_TYPE]

                if buy_price_type is None or ticker is None:
                    continue
                portfolio.short_stocks(buy_date=buy_date, end_date=short_end_date, buy_stock_type=buy_price_type,
                                       sell_stock_type=sell_price_type, stock_ticker=ticker)

            wealth_series.loc[current_date] = portfolio.get_current_values(current_date)

        return wealth_series
