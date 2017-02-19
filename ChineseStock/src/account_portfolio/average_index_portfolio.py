#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: average_index_portfolio
# @Date: 2017-02-16
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import numpy as np

from ..constants.constants import Constant as const


class IndexAccount(object):
    def __init__(self, price_df, wealth_type):
        self.sell_date = None
        self.sell_type = None
        self.hold_amount = None
        self.buy_price = None
        self.price_df = price_df
        self.wealth_type = wealth_type

    def is_free(self, current_date):
        return self.sell_date is None or current_date >= self.sell_date

    def get_price(self, query_date, price_type):
        if query_date in self.price_df.index:
            return self.price_df.ix[query_date, price_type]
        else:
            return np.nan

    def hold_index(self, buy_type, buy_date, sell_type, sell_date, hold_amount):
        if not self.is_free(buy_date):
            raise ValueError('Current Account is not free')

        self.buy_price = self.get_price(buy_date, buy_type)
        self.hold_amount = hold_amount
        self.sell_date = sell_date
        self.sell_type = sell_type

    def get_values(self, query_date):
        if self.sell_date is None:
            return self.hold_amount

        if query_date == self.sell_date:
            current_price = self.get_price(query_date, self.sell_type)
            current_amount = self.hold_amount / self.buy_price * current_price
            self.hold_amount = current_amount
            self.sell_date = None

        elif query_date < self.sell_date:
            current_price = self.get_price(query_date, self.wealth_type)
            current_amount = self.hold_amount / self.buy_price * current_price

        else:
            raise Exception('Account still has value after it should be sell')

        return current_amount


class AverageIndexPortfolio(object):
    def __init__(self, index_price_info, portfolio_num=10, initial_amount=10000., wealth_stock_type=None):
        self.free_amount = initial_amount
        self.free_account_num = portfolio_num
        self.wealth_stock_type = wealth_stock_type if wealth_stock_type is not None else const.STOCK_CLOSE_PRICE
        self.price_info = index_price_info
        self.holding_account_list = []

    def short_index(self, short_date, short_type, re_buy_date, re_buy_tpye):
        if self.free_account_num > 0:
            buy_amount = self.free_amount / float(self.free_account_num)
            self.free_amount -= buy_amount
            self.free_account_num -= 1

            new_account = IndexAccount(price_df=self.price_info, wealth_type=self.wealth_stock_type)
            new_account.hold_index(buy_type=short_type, buy_date=short_date, sell_date=re_buy_date,
                                   sell_type=re_buy_tpye, hold_amount=buy_amount)
            self.holding_account_list.append(new_account)

    def get_current_values(self, query_date):
        current_amount = self.free_amount

        new_account_list = []
        for account in self.holding_account_list:
            if account.is_free(query_date):
                self.free_amount += account.get_values(query_date)
                self.free_account_num += 1

            else:
                new_account_list.append(account)

            current_amount += account.get_values(query_date)

        self.holding_account_list = new_account_list
        return current_amount
