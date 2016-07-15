#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: q1
# Author: Mark Wang
# Date: 3/7/2016

import pickle

import pandas


df = pandas.read_csv('20151225USPubBankMnANameFull.csv')
info_dict = df.set_index(df.keys()[0]).T.to_dict('list')

with open('output.p', 'w') as f:
    pickle.dump(info_dict, f)