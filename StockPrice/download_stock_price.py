#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: download_stock_price
# Author: Mark Wang
# Date: 21/11/2016

import time
import urllib
import urllib2
import datetime
from StringIO import StringIO

import pandas as pd


def get(url, data_list=None, max_try=3):
    if data_list:
        url = "{}?{}".format(url, urllib.urlencode(data_list))
    query = urllib2.Request(url)
    current_try = 0
    while current_try < max_try:
        try:
            response = urllib2.urlopen(query)
            html = response.read()
            response.close()
            return html
        except Exception, e:
            return None
    raise Exception("Cannot open page {}".format(url))


def get_yahoo_finance_data(symbol):
    """
    Using yahoo finance API Get stock price with high low open close data

    :param symbol: stock symbol used in yahoo finance
    :param start_date: start date of the given stock data 2012-03-15
    :param end_date: end data
    :param remove_zero_volume: if True, will remove all data with zero volume
    :return: a list of stock price as [date, open, high, low, close]
    """
    data_list = [('s', symbol), ('g', 'd'), ('ignore', '.csv')]

    url = "http://chart.finance.yahoo.com/table.csv"
    stock_info = get(url=url, data_list=data_list)
    if stock_info is None:
        return None
    stock_data = StringIO(stock_info)
    stock_df = pd.read_csv(stock_data)
    stock_df['Date'] = stock_df['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    stock_df = stock_df.set_index('Date').sort_index()

    return stock_df


def get_all_yahoo_finance_data():
    for i in range(3606, 3607):
        symbol = '{:04d}.HK'.format(i)
        info = get_yahoo_finance_data(symbol)
        if info is None:
            continue

        print symbol
        info.to_csv('YahooStockPrice/{:04d}.csv'.format(i))
        time.sleep(1)


if __name__ == '__main__':
    get_all_yahoo_finance_data()
