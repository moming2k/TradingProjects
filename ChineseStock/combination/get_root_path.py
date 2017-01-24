#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: get_root_path
# @Date: 2017-01-15
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os


def get_root_path():
    if hasattr(os, 'uname'):
        if os.uname()[1] == 'ewin3102':
            return '/home/zigan/Documents/WangYouan/trading/ChineseStock', 30
        else:
            return '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen', 15
    else:
        return r'C:\Users\CFID\Documents\ChinaStock', 30


root_path, process_num = get_root_path()
temp_path = os.path.join(root_path, 'temp')
data_path = os.path.join(root_path, 'data')
stock_price_path = os.path.join(data_path, 'stock_price')
buy_only_report_data_path = os.path.join(data_path, 'report_info_buy_only')

if __name__ == '__main__':
    a, b = get_root_path()
    print a
    print temp_path