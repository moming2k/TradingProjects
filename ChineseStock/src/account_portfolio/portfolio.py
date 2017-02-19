#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: portfolio
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

from ChineseStock.src.constants import Constant as const
from ChineseStock.src.util_functions.util_function import load_stock_info


class Investment(object):
    """ This class is each investment account info """

    # end date use to mark the end date of one investment, if this variable is None means that current account is free.
    end_date = None

    # ticker of trade stock
    stock_ticker = None

    # 1 2 Shanghai A B, 4 8 Shenzhen A B, 16 GEM
    sell_stock_type = None
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
        if self.end_date is not None:
            if self.is_free(current_date):

                stock_info = load_stock_info(current_date, self.stock_ticker, price_path=self.price_path)
                sell_price = stock_info.ix[stock_info.first_valid_index(), self.sell_stock_type]

                # the final amount is calculated used return rate
                self.amount = self.amount * sell_price * (1 - self.transaction_cost) / self.buy_price

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

                amount = self.amount * current_price / self.buy_price

        else:
            amount = self.amount

        return amount

    def short_stock(self, buy_date, end_date, stock_ticker, buy_stock_type, sell_stock_type):
        """ use this investment account to buy some stock """
        self.end_date = end_date
        stock_info = load_stock_info(buy_date, stock_ticker, price_path=self.price_path)
        self.buy_price = stock_info.ix[stock_info.first_valid_index(), buy_stock_type]
        self.sell_stock_type = sell_stock_type
        self.stock_ticker = stock_ticker
        self.previous_price = self.buy_price
        self.amount *= (1 - self.transaction_cost)


class PortFolio(object):
    """ This is a simple portfolio class all investment should be equal """

    def __init__(self, total_num=10, total_value=10000., transaction_cost=0, price_path=None):
        every_amount = total_value / total_num
        self.account_list = []
        for i in range(total_num):
            new_account = Investment(every_amount, transaction_cost=transaction_cost, price_path=price_path)
            self.account_list.append(new_account)

    def get_current_values(self, current_date):
        """ get current investment value """
        amount = 0
        for account in self.account_list:
            amount += account.get_current_value(current_date)

        return amount

    def short_stocks(self, buy_date, end_date, stock_ticker, buy_stock_type, sell_stock_type):
        """ If there is a free account, buy target stock, else do nothing """
        account_index = self.__get_free_account(buy_date)

        if account_index is None:
            return

        self.account_list[account_index].short_stock(buy_date, end_date, stock_ticker,
                                                     buy_stock_type, sell_stock_type)

    def __get_free_account(self, current_date):
        """ get the index of free account """
        for i, account in enumerate(self.account_list):
            if account.is_free(current_date):
                account.get_current_value(current_date)
                return i

        return None
