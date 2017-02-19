#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: test_step2
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

from ChineseStock.src.calculate_return_utils.calculate_return_utils_20170216 import CalculateReturnUtils20170216
from ChineseStock.src.constants.path_info import Path

test = CalculateReturnUtils20170216(Path.TRADING_DAYS_20170216_PATH)

r_path = os.path.join(test.TEMP_PATH, 'insider_stock_20170214_alpha_no_neglect_all_types',
                      'cost_{}_sr_{}_report'.format(2, 5))
w_path = os.path.join(test.TEMP_PATH, 'insider_stock_20170214_alpha_no_neglect_all_types',
                      'cost_{}_sr_{}_wealth'.format(2, 5))
report_path = os.path.join(Path.REPORT_DATA_PATH, 'report_info_buy_only')

info = {test.PORTFOLIO_NUM: 6,
        test.HOLDING_DAYS: 5,
        test.TRANSACTION_COST: 0.002,
        test.REPORT_RETURN_PATH: r_path,
        test.WEALTH_DATA_PATH: w_path,
        test.STOPLOSS_RATE: -float(abs(5)) / 100,
        test.REPORT_PATH: report_path
        }

result_report = test.calculate_return_and_wealth(info)
