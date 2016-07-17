#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: change_column_name
# Author: Mark Wang
# Date: 15/7/2016

import csv

import pandas

name_variable = pandas.read_excel('NewVariableName.xlsx')
change_variable = name_variable[name_variable['NewVariableName'].notnull()]

with open('Bloomberg_CRSP.csv') as input_file, open('Bloomberg_CRSP(renamed).csv', 'w') as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)
    header = next(reader)
    for i in range(len(header)):
        info = header[i]
        for index, row in change_variable.iterrows():
            if info.startswith(change_variable.ix[index, 'OriginalVariableName']):
                info_list = info.split('_')
                while '' in info_list:
                    info_list.remove('')
                while 'Today' in info_list:
                    info_list.remove('Today')
                info_list[0] = change_variable.ix[index, 'NewVariableName']
                header[i] = '_'.join(info_list)
                break
    writer.writerow(header)

    for row in reader:
        writer.writerow(row)