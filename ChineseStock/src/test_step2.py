#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: test_step2
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import sys
import logging

from calculate_return_utils.calculate_return_utils_20170219 import CalculateReturnUtils20170219
from constants.path_info import Path

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

test = CalculateReturnUtils20170219(Path.TRADING_DAYS_20170216_PATH)

# suffix = 'all_report_stock_20170224'
# report_path = os.path.join(Path.REPORT_DATA_PATH, 'report_data_20170205', 'ticker_sep')
# stop_loss = 0
# portfolio_num = 12
# holding_days = 7

stop_loss = 0
portfolio_num = 11
holding_days = 2
suffix = 'insider_stock_20170214_alpha_hedge_no_neglect_all_types'
report_path = os.path.join(Path.REPORT_DATA_PATH, 'report_info_buy_only')

r_path = os.path.join(test.TEMP_PATH, suffix,
                      'cost_2_sr_{}_report'.format(stop_loss))
w_path = os.path.join(test.TEMP_PATH, suffix,
                      'cost_2_sr_{}_wealth'.format(stop_loss))

info = {test.PORTFOLIO_NUM: portfolio_num,
        test.HOLDING_DAYS: holding_days,
        test.TRANSACTION_COST: 0.002,
        test.REPORT_RETURN_PATH: r_path,
        test.WEALTH_DATA_PATH: w_path,
        test.STOPLOSS_RATE: -float(abs(stop_loss)) / 100,
        test.REPORT_PATH: report_path,
        test.INFO_TYPE: test.ALL
        }

result_report = test.calculate_return_and_wealth(info)
result_report.to_csv(os.path.join(Path.TEMP_PATH, 'test.csv'), encoding='utf8')
