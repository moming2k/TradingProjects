#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step23_complement_result
# @Date: 2017-02-28
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import re
import os

import pandas as pd

from constants.path_info import Path
from calculate_return_utils.calculate_return_utils_20170219 import CalculateReturnUtils20170219

root_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen/temp/forecast_report_stock_20170214'
wealth_path = os.path.join(root_path, 'cost_2_sr_5_wealth')
report_path = os.path.join(root_path, 'cost_2_sr_5_report')

file_list = os.listdir(wealth_path)

calculator = CalculateReturnUtils20170219(trading_list_path=Path.TRADING_DAYS_20170216_PATH,
                                          stock_price_path=Path.STOCK_PRICE_20170214_PATH)

for f in file_list:
    if 'raw' not in f:
        continue

    file_size = os.path.getsize(os.path.join(wealth_path, f))

    if file_size > 10000:
        continue

    cost = 0.002

    parameters = re.findall(r'\d+', f)
    p = int(parameters[0])
    d = int(parameters[1])

    report_df = pd.read_pickle(os.path.join(report_path, 'hdays_{}_report.p'.format(d)))

    wealth_series, alpha_hedge_series = calculator.calculate_portfolio_return(report_df, p, cost)
    wealth_series.to_pickle(os.path.join(wealth_path, f))
