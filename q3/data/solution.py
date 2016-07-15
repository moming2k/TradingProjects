#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: q3
# Author: Mark Wang
# Date: 12/7/2016

import datetime

import pandas


def str2datetime(date_str):
    return datetime.datetime.strptime(date_str, '%m/%d/%Y').month


if __name__ == "__main__":
    df = pandas.read_csv('ukpound_exchange.csv', index_col=0)
    keys = df.keys()
    df['month'] = df[keys[0]].apply(str2datetime).diff().shift(-1)
    new_df = df[df['month'] > 0.5]
    del new_df['month']
    new_df.to_csv('output.csv')
