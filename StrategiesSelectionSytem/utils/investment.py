#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: investment
# @Date: 2017-02-04
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


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

    def __init__(self, amount, stock_price_type=const.STOCK_ADJPRCWD, transaction_cost=0, price_path=None):
        self.amount = amount

        # stock price of previous day
        self.previous_price = None

        # this parameter are used to determine which price are used to calculate the final result
        self.stock_price_type = stock_price_type

        self.transaction_cost = transaction_cost
        self.price_path = price_path

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
                if int(self.stock_type) in [1, 2]:
                    stock_info = load_stock_info(current_date, self.stock_ticker, 'SH', price_path=self.price_path)
                else:
                    stock_info = load_stock_info(current_date, self.stock_ticker, 'SZ', price_path=self.price_path)

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
        self.amount *= (1 - self.transaction_cost)
