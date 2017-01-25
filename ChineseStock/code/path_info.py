#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: path_info
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from os_related import get_root_path

root_path = get_root_path()
temp_path = os.path.join(root_path, 'temp')
data_path = os.path.join(root_path, 'data')
result_path = os.path.join(root_path, 'result')
stock_price_path = os.path.join(data_path, 'stock_price')
buy_only_report_data_path = os.path.join(data_path, 'report_info_buy_only')

trading_day_list = pd.read_pickle(os.path.join(data_path, 'trading_days_list.p'))