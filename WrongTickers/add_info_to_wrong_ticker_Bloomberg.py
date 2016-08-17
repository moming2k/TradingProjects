#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_info_to_wrong_ticker
# Author: Mark Wang
# Date: 15/8/2016

from add_info_to_wrong_ticker import *

if __name__ == "__main__":
    print 'Start to handle bloomberg'
    add_real_price_stock_info('result_csv/wrong_tickers_from_Bloomberg_large_ES.csv', 'Bloomberg')
