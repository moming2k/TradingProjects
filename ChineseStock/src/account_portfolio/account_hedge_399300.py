#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: account_hedge_399300
# @Date: 2017-02-19
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import numpy as np
import pandas as pd

from ..constants.constants import Constant
from ..constants.path_info import Path
from ..util_functions.util_function import load_stock_info


class AccountHedge399300(Constant):
    """ This class is each investment account info """

    def __init__(self, amount, stock_price_type=None, transaction_cost=0, price_path=None):
        self.amount = amount

        # stock price of previous day
        self.previous_price = None

        # this parameter are used to determine which price are used to calculate the final result
        self.stock_price_type = self.STOCK_CLOSE_PRICE if stock_price_type is None else stock_price_type

        self.transaction_cost = transaction_cost
        self.price_path = price_path

        # end date use to mark the end date of one investment, if this variable is None means that current account is free.
        self.end_date = None

        # ticker of trade stock
        self.stock_ticker = None
        self.sell_stock_type = None
        self.buy_price = None
        self.hedge_price = None

    def is_free(self, current_date):
        """ Whether this investment account has free money """
        return self.end_date is None or current_date >= self.end_date

    def get_current_value(self, current_date):
        """ Given date info return the value of current date """

        # this means current investment is still in use
        if self.end_date is not None:
            if self.is_free(current_date):

                stock_info = load_stock_info(current_date, self.stock_ticker, price_path=self.price_path)
                sell_price = stock_info.ix[stock_info.first_valid_index(), self.sell_stock_type]
                current_hedge_price = self.load_hedge_price(price_type=self.sell_stock_type,
                                                            current_date=current_date)

                # the final amount is calculated used return rate
                self.amount = self.amount * (sell_price * (1 - self.transaction_cost) / self.buy_price -
                                             current_hedge_price / self.hedge_price + 1)

                # Clear unused data
                self.end_date = None

                amount = self.amount

            else:
                # based on the stock type to load target data
                stock_info = load_stock_info(current_date, self.stock_ticker, price_path=self.price_path)

                # this means no trading on target date, use previous data
                if stock_info.empty:
                    current_price = self.previous_price
                else:
                    current_price = stock_info.loc[stock_info.first_valid_index(), self.stock_price_type]
                    self.previous_price = current_price

                current_hedge_price = self.load_hedge_price(price_type=self.stock_price_type,
                                                            current_date=current_date)

                amount = self.amount * (current_price / self.buy_price - current_hedge_price / self.hedge_price + 1)

        else:
            amount = self.amount

        return amount

    def short_stock(self, buy_date, end_date, stock_ticker, buy_stock_type, sell_stock_type):
        """ use this investment account to buy some stock """
        stock_info = load_stock_info(buy_date, stock_ticker, price_path=self.price_path)
        self.end_date = end_date
        self.stock_ticker = stock_ticker
        self.sell_stock_type = sell_stock_type
        self.amount *= (1 - self.transaction_cost)
        self.buy_price = stock_info.ix[stock_info.first_valid_index(), buy_stock_type]
        self.hedge_price = self.load_hedge_price(price_type=buy_stock_type, current_date=buy_date)
        self.previous_price = stock_info.ix[stock_info.first_valid_index(), self.stock_price_type]

    @staticmethod
    def load_hedge_price(price_type, current_date):
        index_df = pd.read_pickle(Path.SZ_399300_PATH)

        index_df = index_df[index_df.index == current_date]

        if index_df.empty:
            return np.nan

        else:
            return index_df.ix[index_df.first_valid_index(), price_type]
