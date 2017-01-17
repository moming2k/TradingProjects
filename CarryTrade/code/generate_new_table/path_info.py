#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: path_info
# @Date: 2017-01-16
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

root_path = '/home/wangzg/Documents/WangYouan/research/CarryTrade'
original_return_data = os.path.join(root_path, 'CurrData')
result_path = os.path.join(root_path, 'result')
data_path = os.path.join(root_path, 'data')
return_data_path = os.path.join(data_path, 'adjusted_return')
learning_data_path = os.path.join(data_path, 'learning_return')
temp_path = os.path.join(root_path, 'temp')

if __name__ == '__main__':
    path_list = [return_data_path, temp_path, result_path]
    for dir_path in path_list:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
