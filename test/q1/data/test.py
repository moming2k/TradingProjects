#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: test
# Author: Mark Wang
# Date: 13/7/2016

import pickle

dict1 = None
dict2 = None

with open('output.p') as f:
    dict1 = pickle.load(f)


with open('output_xlsx.p') as f:
    dict2 = pickle.load(f)


set1 = set(dict1.keys())
set2 = set(dict2.keys())

for i in set1.union(set2):
    if i not in dict2:
        print 'Dict2 does not contains %s' % i
    elif i not in dict1:
        print 'Dict1 does not contains %s' % i
    elif dict2[i] != dict1[i]:
        print 'key: %s; Dict1: %s; Dict2 %s' % (i, dict1[i], dict2[i])
