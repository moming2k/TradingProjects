#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: q1_xlsx
# Author: Mark Wang
# Date: 3/7/2016

import pickle

import pandas


def datetime2str(date_time):
    return '{:d}/{:d}/{:d}'.format(date_time.month, date_time.day, date_time.year)


df = pandas.read_excel('20151225USPubBankMnANameFull.xlsx', 'Sheet1')
keys = df.keys()
df[keys[0]] = df[keys[0]].apply(datetime2str)

with open('output_xlsx.p', 'w') as f:
    pickle.dump(df.set_index(keys[0]).T.to_dict('list'), f)
