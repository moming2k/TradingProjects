#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: q4
# Author: Mark Wang
# Date: 12/7/2016

import pandas

if __name__ == '__main__':
    all_files = ['2014.csv', '2015.csv']
    pandas.concat(pandas.read_csv(f, index_col=0) for f in all_files).to_csv('output.csv')