#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: select_significant_file
# Author: Mark Wang
# Date: 15/11/2016

import os
import shutil


result_path = '/home/wangzg/Documents/WangYouan/research/Glassdoor/regression_result'
output_path = '/home/wangzg/Documents/WangYouan/research/Glassdoor/significant_result'

if not os.path.isdir(output_path):
    os.makedirs(output_path)

for txt_file in os.listdir(result_path):
    if not txt_file.endswith('1kResult.txt'):
        continue

    f = open(os.path.join(result_path, txt_file))
    s = f.read()
    f.close()
    parameters = s.split('\n')[3].split('\t')
    n = len(parameters)
    par_name = parameters[0]
    count = 0
    if par_name.startswith('cons'):
        for par in parameters[1:]:
            if par.endswith('*'):
                count += 1
    else:
        for par in parameters[1:]:
            if par.endswith('*') and par.startswith('-'):
                count += 1

    if float(count) / n >= 0.2:
        src = os.path.join(result_path, txt_file)
        dst = os.path.join(output_path, txt_file)
        shutil.copy(src=src, dst=dst)

        xls_file = '{}.xls'.format(txt_file[:-4])
        src = os.path.join(result_path, xls_file)
        dst = os.path.join(output_path, xls_file)
        shutil.copy(src=src, dst=dst)
