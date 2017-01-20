#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step6_generate_data_including_learning
# @Date: 2017-01-20
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd

from constant import Constant as const
from path_info import return_data_path, learning_data_path, total_data_path

if __name__ == '__main__':
    today_str = datetime.datetime.today().strftime('%Y%m%d')


    for month in [const.ONE_MONTH, const.TWELVE_MONTH, const.THREE_MONTH, const.SIX_MONTH]:
        for currency in [48, 15]:
            learning_file_name = '20160919_{}_updated_{}_curr_learning.p'.format(month, currency)
            original_file_name = '20160919_{}_updated_{}_curr.p'.format(month, currency)

            df1 = pd.read_pickle(os.path.join(learning_data_path, learning_file_name))
            df2 = pd.read_pickle(os.path.join(return_data_path, original_file_name))
            df = pd.concat([df1, df2], axis=1)
            df.to_pickle(os.path.join(total_data_path, '{}_currency_{}_{}.p'.format(today_str, currency, month)))
