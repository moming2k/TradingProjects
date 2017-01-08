#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step2_calculate_portforlio_return
# @Date: 2017-01-06
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd
import numpy as np

from constant import Constant

const = Constant()

today_str = datetime.datetime.today().strftime('%Y%m%d')
root_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'
data_path = os.path.join(root_path, 'data')
temp_path = os.path.join(root_path, 'temp')
today_path = os.path.join(temp_path, today_str)

if not os.path.isdir(today_path):
    os.makedirs(today_path)

return_df = pd.read_pickle(os.path.join(temp_path, '20170107', 'insider_add_return_hday_22_ow_only.p'))
stock_data = pd.read_pickle(os.path.join(temp_path, '20170106', 'daily_0516.p'))
trading_days = pd.read_pickle(os.path.join(temp_path, '20170108', 'trading_days_list.p'))


class Investment(object):
    end_date = None
    amount = 1000
    return_rate = None
    stock_ticker = None
    stock_type = None
    buy_price = None

    def __init__(self, amount):
        self.amount = amount

    def is_free(self, current_date):
        return self.end_date is None or current_date >= self.end_date

    def get_current_value(self, current_date):
        if self.return_rate is not None:
            if self.is_free(current_date):
                self.end_date = None
                self.amount = self.amount * (1 + self.return_rate)
                self.return_rate = None
                self.buy_price = None
                self.stock_type = None
                self.buy_price = None
                amount = self.amount
            else:
                stock_info = stock_data[stock_data[const.STOCK_TICKER] == self.stock_ticker]
                stock_info = stock_info[stock_info[const.STOCK_MARKET_TYPE] == self.stock_type]
                if stock_info.empty:
                    amount = self.amount
                else:
                    current_price = stock_info.loc[stock_info.first_valid_index(), const.STOCK_CLOSE_PRICE]
                    amount = self.amount * current_price / self.buy_price

        else:
            amount = self.amount

        return amount

    def short_stock(self, return_rate, end_date, buy_price, stock_type, stock_ticker):
        self.end_date = end_date
        self.return_rate = return_rate
        self.buy_price = buy_price
        self.stock_type = stock_type
        self.stock_ticker = stock_ticker


class PortFolio(object):
    def __init__(self, total_num=10, total_value=10000):
        every_amount = total_value / total_num
        self.account_list = []
        for i in range(total_num):
            new_account = Investment(every_amount)
            self.account_list.append(new_account)

    def get_current_values(self, current_date):
        amount = 0
        for account in self.account_list:
            amount += account.get_current_value(current_date)

        return amount

    def get_extra_account(self, current_date):
        for i, account in enumerate(self.account_list):
            if account.is_free(current_date):
                account.get_current_value(current_date)
                return i

        return None

    def short_stocks(self, end_date, stock_return, current_date, buy_price, stock_ticker, stock_type):
        account_index = self.get_extra_account(current_date)

        if account_index is None:
            return

        self.account_list[account_index].short_stock(stock_return, end_date, buy_price, stock_type, stock_ticker)


def get_useful_info(ticker, announce_date):
    market_info = ticker[-2:]
    ticker_info = ticker[:6]
    used_stock_data = stock_data[stock_data[const.STOCK_TICKER] == ticker_info]
    if market_info == 'SZ':
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 1]
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 2]

    else:
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 4]
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 8]
        used_stock_data = used_stock_data[used_stock_data[const.STOCK_MARKET_TYPE] != 16]

    trade_day = trading_days[trading_days > announce_date].tolist()[0]
    buy_info = used_stock_data[used_stock_data[const.STOCK_DATE] == trade_day]
    if buy_info.empty:
        return None, None, None, None

    index = buy_info.first_valid_index()
    return ticker_info, buy_info.ix[index, const.STOCK_MARKET_TYPE], buy_info.ix[index, const.STOCK_DATE], buy_info.ix[
        index, const.STOCK_OPEN_PRICE]


if __name__ == '__main__':
    portfolio = PortFolio(10, 10000)
    ann_days = return_df[const.REPORT_ANNOUNCE_DATE].sort_values()
    current_date = ann_days.min()
    end_date = ann_days.max()

    wealth_df = pd.Series()

    for current_date in trading_days:

        info_index = ann_days[ann_days == current_date].index

        for i in info_index:
            short_end_date = return_df.ix[i, const.REPORT_SELL_DATE]
            short_return_rate = return_df.ix[i, const.REPORT_RETURN_RATE]

            ticker, market_type, buy_date, buy_price = get_useful_info(return_df.ix[i, const.REPORT_TICKER],
                                                                       current_date)
            if np.isnan(short_return_rate) or ticker is None:
                continue
            portfolio.short_stocks(short_end_date, short_return_rate, buy_date, buy_price=buy_price,
                                   stock_ticker=ticker, stock_type=market_type)

        wealth_df.loc[current_date] = portfolio.get_current_values(current_date)
        current_date += datetime.timedelta(days=1)

    wealth_df.to_pickle(os.path.join(today_path, '{}_wealth_hdays_22.p'.format(today_str)))
    wealth_df.to_csv(os.path.join(today_path, '{}_wealth_hdays_22.csv'.format(today_str)))
