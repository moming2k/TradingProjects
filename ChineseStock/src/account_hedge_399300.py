#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: account_hedge_399300
# @Date: 2017-02-19
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

from constants import Constant
from util_function import load_stock_info


class AccountHedge399300(Constant):
    """ This class is each investment account info """

    def __init__(self, amount, stock_price_type=None, transaction_cost=0, price_path=None):
        self.amount = amount

        # stock price of previous day
        self.previous_price = None

        # this parameter are used to determine which price are used to calculate the final result
        self.stock_price_type = self.STOCK_ADJPRCWD if stock_price_type is None else stock_price_type

        self.transaction_cost = transaction_cost
        self.price_path = price_path

        # end date use to mark the end date of one investment, if this variable is None means that current account is free.
        self.end_date = None

        # the final return rate of target stock
        self.return_rate = None

        # ticker of trade stock
        self.stock_ticker = None

        # 1 2 Shanghai A B, 4 8 Shenzhen A B, 16 GEM
        self.stock_type = None
        self.buy_price = None
        self.short_index_price = None

    def is_free(self, current_date):
        """ Whether this investment account has free money """
        return self.end_date is None or current_date >= self.end_date

    def get_current_value(self, current_date):
        """ Given date info return the value of current date """

        # this means current investment is still in use
        if self.return_rate is not None:
            if self.is_free(current_date):

                # the final amount is calculated used return rate
                self.amount = self.amount * (1 + self.return_rate) * (1 - self.transaction_cost)

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
                stock_info = load_stock_info(current_date, self.stock_ticker, price_path=self.price_path)

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

    def short_stock(self, return_rate, end_date, buy_price, stock_type=None, stock_ticker=None):
        """ use this investment account to buy some stock """
        self.end_date = end_date
        self.return_rate = return_rate
        self.buy_price = buy_price
        self.stock_ticker = stock_ticker
        self.previous_price = buy_price
        self.amount *= (1 - self.transaction_cost)
