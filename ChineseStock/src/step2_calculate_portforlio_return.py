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

return_df = pd.read_pickle(os.path.join(temp_path, '2017-01-07', 'insider_add_return.p'))


class Investment(object):
    end_date = None
    amount = 1000
    return_rate = None

    def __init__(self, amount):
        self.amount = amount

    def is_free(self, current_date):
        return self.end_date is None or current_date > self.end_date

    def get_current_value(self, current_date):
        if self.return_rate is not None and self.is_free(current_date):
            self.end_date = None
            self.amount = self.amount * (1 + self.return_rate)
            self.return_rate = None

        return self.amount

    def short_stock(self, return_rate, end_date):
        self.end_date = end_date
        self.return_rate = return_rate


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

    def short_stocks(self, end_date, stock_return, current_date):
        account_index = self.get_extra_account(current_date)

        if account_index is None:
            return

        self.account_list[account_index].short_stock(stock_return, end_date)


if __name__ == '__main__':
    portfolio = PortFolio(10, 10000)
    ann_days = return_df[const.REPORT_ANNOUNCE_DATE].sort_values()
    current_date = ann_days.min()
    end_date = ann_days.max()

    wealth_df = pd.Series()
    while current_date <= end_date:

        info_index = ann_days[ann_days == current_date].index

        for i in info_index:
            short_end_date = return_df.ix[i, const.REPORT_SELL_DATE]
            short_return_rate = return_df.ix[i, const.REPORT_RETURN_RATE]
            if np.isnan(short_return_rate):
                continue
            portfolio.short_stocks(short_end_date, short_return_rate, current_date)

        wealth_df.loc[current_date] = portfolio.get_current_values(current_date)
        current_date += datetime.timedelta(days=1)

    wealth_df.to_pickle(os.path.join(today_path, '{}_wealth_hdays_22.p'.format(today_str)))
    wealth_df.to_csv(os.path.join(today_path, '{}_wealth_hdays_22.csv'.format(today_str)))
