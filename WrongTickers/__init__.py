#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: __init__
# Author: Mark Wang
# Date: 15/7/2016

import pandas

from solution import all_tickers, get_wrong_ticker

df = pandas.read_pickle('temp2.p')
for index, row in df.iterrows():
    print row
    print get_wrong_ticker(row)
