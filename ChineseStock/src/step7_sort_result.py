#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sort_result
# @Date: 2017-02-04
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import shutil

import pandas as pd

from ChineseStock.src.constants.path_info import result_path
from ChineseStock.src.util_functions.os_related import make_dirs

file_list = os.listdir(result_path)

for dir_name in file_list:
    if not dir_name.endswith('new'):
        continue

    picture_1_5_save_path = os.path.join(result_path, dir_name, 'sharpe_1_5')
    picture_2_save_path = os.path.join(result_path, dir_name, 'sharpe_2')
    picture_save_path = os.path.join(result_path, dir_name, 'picture')

    make_dirs([picture_2_save_path, picture_1_5_save_path])

    info_names = os.listdir(os.path.join(result_path, dir_name))
    for info_file in info_names:
        if 'statistic' in info_file and info_file.endswith('.p'):
            break

    else:
        continue

    print info_file

    df = pd.read_pickle(os.path.join(result_path, dir_name, info_file))
    for method in df.keys():
        if df.ix['sharpe_ratio', method] >= 2.:
            shutil.copy(os.path.join(picture_save_path, '{}.png'.format(method)),
                        os.path.join(picture_2_save_path, '{}.png'.format(method)))

        elif df.ix['sharpe_ratio', method] >= 1.5:
            shutil.copy(os.path.join(picture_save_path, '{}.png'.format(method)),
                        os.path.join(picture_1_5_save_path, '{}.png'.format(method)))
