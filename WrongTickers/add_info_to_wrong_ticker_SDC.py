#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_info_to_wrong_ticker_SDC
# Author: Mark Wang
# Date: 16/8/2016

from add_info_to_wrong_ticker_Bloomberg import fill_in_missing_info

if __name__ == '__main__':
    print 'Start to handle SDC'
    fill_in_missing_info('result_csv/wrong_tickers_from_SDC_target_name.csv')
