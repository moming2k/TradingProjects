#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: select_best_file
# Author: Mark Wang
# Date: 27/11/2016

import os
import datetime
import shutil

root_path = '/home/wangzg/Documents/WangYouan/research/Glassdoor'

sig_dd_da_path = os.path.join(root_path, '{}DdDaSigResult'.format(datetime.datetime.today().strftime("%Y%m%d")))

if not os.path.isdir(sig_dd_da_path):
    os.makedirs(sig_dd_da_path)

for result_path in ['da_reg_result', 'dd_reg_result']:
    reg_path = os.path.join(root_path, result_path)

    for xls_file in os.listdir(reg_path):
        if not xls_file.endswith('txt'):
            continue

        f = open(os.path.join(reg_path, xls_file))
        s = f.read()
        f.close()
        s = map(lambda x: x.split('\t'), s.split('\n'))
        is_copy = True

        # for index in [(4, 9), (4, 10), (52, 21), (52, 22), (54, 32), (54, 33), (56, 43), (56, 44)]:
        for index in [(4, 10), (52, 22), (54, 33), (56, 44)]:
            data = s[index[0]][index[1]]
            data = data[1:-1]

            if float(data) < 1.4:
                is_copy = False
                break

        if is_copy:
            shutil.copy(os.path.join(reg_path, xls_file), os.path.join(sig_dd_da_path, xls_file))
            shutil.copy(os.path.join(reg_path, '{}.xls'.format(xls_file[:-4])),
                        os.path.join(sig_dd_da_path, '{}.xls'.format(xls_file[:-4])))
