#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step1_optimize_strategy
# @Date: 2017-04-07
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


if __name__ == '__main__':
    import sys
    import logging
    import cProfile

    from ..constants.path_info import Path
    from ..calculate_return_utils.calculate_return_utils_20170303 import CalculateReturnUtils
    from ..report_generator.report_generator_add_max_drawdown_limit import ReportGenerator

    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    # define some variables
    transaction_cost = 0.002
    suffix = 'forecast_run_up_optimize_test'
    stop_loss_rate = 5
    run_up_rate = 5
    run_up_x = 10
    report_path = Path.FORECAST_RUN_UP_REPORT_PATH

    test_info = ReportGenerator(transaction_cost=transaction_cost, report_path=report_path,
                                folder_suffix=suffix, trading_days_list_path=Path.TRADING_DAYS_20170228_PATH,
                                stock_price_path=Path.STOCK_PRICE_20170214_PATH)
    calculator = CalculateReturnUtils(trading_list_path=Path.TRADING_DAYS_20170228_PATH,
                                      stock_price_path=Path.STOCK_PRICE_20170214_PATH)

    test_info.INFO_TYPE_LIST = [test_info.ALL]
    test_info.RUN_UP_DAY_X_LIST = [5, 10, 15, 20]
    w_path, s_path, r_path, p_path, bp_path15, bp_path2 = test_info._generate_useful_paths(stop_loss_rate)

    portfolio_info = {test_info.PORTFOLIO_NUM: 15,
                      test_info.HOLDING_DAYS: 12,
                      test_info.TRANSACTION_COST: transaction_cost,
                      test_info.REPORT_RETURN_PATH: r_path,
                      test_info.WEALTH_DATA_PATH: w_path,
                      test_info.STOPLOSS_RATE: -float(abs(stop_loss_rate)) / 100,
                      test_info.REPORT_PATH: report_path,
                      test_info.RUN_UP_RATE: run_up_rate,
                      test_info.RUN_UP_X: run_up_x,
                      test_info.RUN_UP_Y: 1,
                      test_info.INFO_TYPE: test_info.ALL,
                      }

    cProfile.run("calculator.calculate_return_and_wealth(portfolio_info)")


