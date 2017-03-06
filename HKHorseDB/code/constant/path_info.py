#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: path_info
# @Date: 2017-03-05
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os


class PathInfo(object):
    ROOT_PATH = '/home/wangzg/Documents/WangYouan/Trading/HKHorse'
    TEMP_PATH = os.path.join(ROOT_PATH, 'temp')
    RACE_TEMP_PATH = os.path.join(TEMP_PATH, 'race_data')
    MERGED_TEMP_PATH = os.path.join(TEMP_PATH, 'merged_data')

    DATA_PATH = os.path.join(ROOT_PATH, 'data')
    RACE_DATA_PATH = os.path.join(DATA_PATH, 'race_data')
    MERGED_DATA_PATH = os.path.join(DATA_PATH, 'merged_data')

    RESULT_PATH = os.path.join(ROOT_PATH, 'result')
    MERGED_RESULT_PATH = os.path.join(RESULT_PATH, 'merged_data')
