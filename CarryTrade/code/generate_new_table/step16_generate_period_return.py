#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step16_generate_period_return
# @Date: 2017-01-24
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import re

import pandas as pd

from path_info import *
from util_function import plot_sub_date_picture

period_picture_path = os.path.join(picture_save_path, 'period')

if not os.path.isdir(period_picture_path):
    os.makedirs(period_picture_path)

# df_48 = pd.read_pickle(os.path.join(return_data_path, '20160919_1m_updated_48_curr.p'))
# df_15 = pd.read_pickle(os.path.join(return_data_path, '20160919_1m_updated_15_curr.p'))
#
# keys_48 = ['48_currs_10_liquid_3_parts_1m', '48_currs_34_liquid_34_parts_1m', '48_currs_48_liquid_24_parts_1m']
# keys_15 = ['15_currs_14_liquid_7_parts_1m', '15_currs_12_liquid_3_parts_1m', '15_currs_10_liquid_10_parts_1m']
#
# for i, key in enumerate(keys_48):
#     num_info = re.findall(r'\d+', key)
#     picture_title = '{d[1]}l, {d[2]}p, {d[3]}m'.format(d=num_info)
#     file_name = '{d[0]}currs_{d[1]}l_{d[2]}p_{d[3]}m_period_{e}.png'.format(d=num_info, e=(i + 1))
#     plot_sub_date_picture(data_series=df_48[key], picture_title=picture_title,
#                           picture_save_path=os.path.join(period_picture_path, file_name),
#                           period=(i + 1))
#
# for i, key in enumerate(keys_15):
#     num_info = re.findall(r'\d+', key)
#     picture_title = '{d[1]}l, {d[2]}p, {d[3]}m'.format(d=num_info)
#     file_name = '{d[0]}currs_{d[1]}l_{d[2]}p_{d[3]}m_period_{e}.png'.format(d=num_info, e=(i + 1))
#     plot_sub_date_picture(data_series=df_15[key], picture_title=picture_title,
#                           picture_save_path=os.path.join(period_picture_path, file_name),
#                           period=(i + 1))


df_48 = pd.read_pickle(os.path.join(return_data_path, '20160919_3m_updated_48_curr.p'))

key = '48_currs_18_liquid_9_parts_3m'

num_info = re.findall(r'\d+', key)
picture_title = '{d[1]}l, {d[2]}p, {d[3]}m'.format(d=num_info)
file_name = '{d[0]}currs_{d[1]}l_{d[2]}p_{d[3]}m_period_{e}.png'.format(d=num_info, e=(1))
plot_sub_date_picture(data_series=df_48[key], picture_title=picture_title,
                      picture_save_path=os.path.join(period_picture_path, file_name),
                      period=(1))