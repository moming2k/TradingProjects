#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: path_info
# @Date: 2017-02-14
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

root_path = '/home/wangzg/Documents/WangYouan/research/Polution'

data_path = os.path.join(root_path, 'data')
temp_path = os.path.join(root_path, 'temp')
result_path = os.path.join(root_path, 'result')
year_data_path = os.path.join(data_path, '20161109_cusip_append_plus')
crsp_data_path = os.path.join(data_path, 'crsp_stocknames.xls')
compustat_data_path = os.path.join(data_path, 'cusip_sic_compustat.csv')
