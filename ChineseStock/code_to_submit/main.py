#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: running_system
# @Date: 2017-03-15
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

from util_classes.constants import Constant as const
from util_classes.calculate_return_utils import CalculateReturnUtils
from util_classes.util_function import make_dirs, plot_multiline_picture_text


def calculate_data_and_return_picture(report_type, part_num, holding_days, stop_loss):
    datetime_str = datetime.datetime.today().strftime('%Y%m%d%H%M')

    print datetime.datetime.today(), 'Start to handle report type {}'.format(report_type)
    calculator = CalculateReturnUtils(trading_list_path=const.TRADING_DAYS_20170228_PATH,
                                      stock_price_path=const.STOCK_DATA_PATH, root_path=os.path.abspath(os.curdir))

    report_path = os.path.join(calculator.TEMP_PATH, report_type)
    result_path = os.path.join(calculator.RESULT_PATH, '{}{}result'.format(datetime_str, report_type))
    make_dirs([report_path, result_path])

    print datetime.datetime.today(), 'Result would be saved in {}'.format(result_path)

    info_dict = {const.PORTFOLIO_NUM: part_num,
                 const.HOLDING_DAYS: holding_days,
                 const.TRANSACTION_COST: 0.002,
                 const.REPORT_RETURN_PATH: report_path,
                 const.WEALTH_DATA_PATH: result_path,
                 const.STOPLOSS_RATE: -float(abs(stop_loss)) / 100,
                 const.REPORT_PATH: calculator.FORECAST_REPORT_PATH if report_type == 'forecast' \
                     else calculator.INSIDER_EXE_GT2_PATH,
                 const.INFO_TYPE: const.ALL if report_type == 'forecast' else 'exe'
                 }
    raw_return, alpha_return = calculator.calculate_return_and_wealth(info_dict)

    if report_type == 'forecast':
        pic_title = 'all_{}p_{}d_2cost_{}sr'.format(part_num, holding_days, stop_loss)
    else:
        pic_title = 'exe_{}p_{}d_2cost_{}sr'.format(part_num, holding_days, stop_loss)

    plot_multiline_picture_text(pic_title, [raw_return, alpha_return], ['Raw Strategy', 'Alpha Strategy'],
                                os.path.join(result_path, '{}.png'.format(pic_title)), stop_loss)

    print datetime.datetime.today(), "Process finished all result are saved in {}".format(result_path)


if __name__ == '__main__':

    print 'Please Select which strategy you want to run:'
    print '1. Best sharpe ratio after 2016 using insider'
    print '2. Best annualized return after 2016 using insider'
    print '3. Best sharpe ratio after 2016 using forecast'
    print '4. Best annualized return after 2016 using forecast'
    while True:
        s = raw_input('Please select one info: ')
        if s.strip().isdigit() and int(s.strip()) in range(1, 5):
            break
        else:
            print 'Wrong input {}'.format(s)
            s = raw_input('Please select one info: ')

    # insider best sharpe and return are same
    if s == '1' or s == '2':
        calculate_data_and_return_picture('insider', 6, 14, 5)

    # Best sharpe ratio after 2016 using forecast
    elif s == '3':
        calculate_data_and_return_picture('forecast', 6, 14, 4)

    # Best annualized return after 2016 using forecast
    elif s == '4':
        calculate_data_and_return_picture('forecast', 5, 14, 5)

