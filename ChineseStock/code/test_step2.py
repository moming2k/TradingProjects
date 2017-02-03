#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: test_step2
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import re

import pandas as pd

root_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen/result/sorted_result/new_data'

dir_list = ['cost_2_stop_loss_1_new', 'cost_2_stop_loss_3_new', 'cost_2_stop_loss_5_newc', 'cost_2_stop_loss_2_new',
            'cost_2_stop_loss_4_new']

for file_name in dir_list:
    stop_loss = re.findall(r'\d+', file_name)[1]
    df_name = '20170201_stoploss_{}.p'.format(stop_loss)

    df = pd.read_pickle(os.path.join(root_path, file_name, df_name))
    df.to_csv(os.path.join(root_path, file_name, '20170201_stoploss_{}.csv'.format(stop_loss)))
