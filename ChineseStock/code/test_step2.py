#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: test_step2
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd

from path_info import daily_date_sep_path
from constants import Constant as const

file_list = os.listdir(daily_date_sep_path)

for file_name in file_list:
    data_df = pd.read_pickle(os.path.join(daily_date_sep_path, file_name))
    data_df[const.STOCK_DATE] = data_df[const.STOCK_DATE].apply(lambda x: datetime.datetime.strptime(x, '%Y%m%d'))
    data_df.to_pickle(os.path.join(daily_date_sep_path, file_name))
