#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: sort_picture
# Author: Mark Wang
# Date: 27/9/2016

import os
import shutil

import pandas as pd

FORMER_RESULT_PATH = '/Users/warn/Documents/RAForWangZG/2016.9.18/xlsx_results'
q = 8

max_sta_df = pd.read_excel(os.path.join(FORMER_RESULT_PATH, 'max_info_statistics.xlsx'),
                           sheetname='division {} (no dup)'.format(q))

source_dir = 'output_picture_8'
dst_dir = 'sorted_picture'

i = 1

for method in max_sta_df['method']:
    src = os.path.join(source_dir, '{}.png'.format(method))
    dst = os.path.join(dst_dir, '{}.png'.format(i))
    shutil.copy(src, dst)
    i += 1
