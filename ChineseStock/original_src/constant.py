#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: constant
# @Date: 2017-01-06
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


class Constant(object):
    # trading market type
    SHANGHAI_A = 1
    SHANGHAI_B = 2
    SHENZHEN_A = 4
    SHENZHEN_B = 8
    GEM = 16  # Growth Enterprises Market Board

    # Common Column Names for all report
    STOCK_TICKER = 'Ticker'
    MARKET_TYPE = 'TickerType'

    # Report Information
    REPORT_ANNOUNCE_DATE = 'AnnDate'
    REPORT_RATIO = 'Ratio'
    REPORT_LONG_PRICE = 'LongPrice'
    REPORT_LONG_DATE = 'LongDate'
    REPORT_AMOUNT = 'Amount'
    REPORT_SHORT_PRICE = 'ShortPrice'
    REPORT_SHORT_DATE = 'ShortDate'

    # The following information are mainly used in stock price record data
    STOCK_PRICE_DATE = 'TradingDate'
    STOCK_OPEN_PRICE = 'OpenPrice'
    STOCK_OPEN_PRICE_2 = 'OpenPrice2'
    STOCK_CLOSE_PRICE = 'ClosePrice'
    STOCK_CLOSE_PRICE_2 = 'ClosePrice2'
    STOCK_VOLUME = 'Volume'

    # The following columns are used in wealth report data or other data
    SHARPE_RATE = 'Sharpe Ratio'
    ANNUALIZED_RETURN = 'Ann Return'
    MAX_DRAW_DOWN = 'Max Drawdown Rate'

