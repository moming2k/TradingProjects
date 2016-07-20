#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: merge_church_file
# Author: Mark Wang
# Date: 20/7/2016

import pandas

df1 = pandas.read_csv('us_church_information.csv')
df2 = pandas.read_pickle('southern_churches.p')
df3 = pandas.read_pickle('northern_churches.p')

df = pandas.concat([df1, df2, df3], axis=0, ignore_index=True).drop_duplicates(['place_id'])
df.to_csv('us_church_information(whole).csv', encoding='utf8')
print len(df['name'])
