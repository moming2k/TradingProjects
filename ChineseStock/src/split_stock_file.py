#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: split_stock_file
# @Date: 2017-01-09
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from constant import Constant

const = Constant()

root_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'
data_path = os.path.join(root_path, 'data')
temp_path = os.path.join(root_path, 'temp')
stock_price_path = os.path.join(root_path, 'stock_price')

if not os.path.isdir(stock_price_path):
    os.makedirs(stock_price_path)

stock_data = pd.read_pickle(os.path.join(temp_path, '20170106', 'daily_0516.p'))
