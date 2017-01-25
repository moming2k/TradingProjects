#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: portfolio
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

from constants import Constant as const
from util_function import load_stock_info

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
