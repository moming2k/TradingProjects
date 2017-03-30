#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step4_redraw_forecast_picture
# @Date: 2017-03-28
# @Author: Mark Wang
# @Email: wangyouan@gmial.com



if __name__ == '__main__':
    import os
    import sys
    import logging
    import datetime

    from xvfbwrapper import Xvfb

    from ChineseStock.src.constants.path_info import Path
    from ChineseStock.src.report_generator.report_generator_add_alpha_hedge import ReportGeneratorAlphaHedge as ReportGenerator

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    transaction_cost = 0.002
    suffix = 'forecast_report_stock_20170214'
    report_path = Path.FORECAST_REPORT_PATH

    vdisplay = Xvfb(width=1366, height=768)
    vdisplay.start()

    test_info = ReportGenerator(transaction_cost=transaction_cost, report_path=report_path,
                                folder_suffix=suffix, trading_days_list_path=Path.TRADING_DAYS_20170228_PATH,
                                stock_price_path=Path.STOCK_PRICE_20170214_PATH)

    result_path = os.path.join(Path.RESULT_PATH, suffix)
    test_info.generate_histogram_from_result_path(result_path)

    period_list = [
        (datetime.datetime(2013, 7, 22), datetime.datetime(2016, 7, 20)),
        (datetime.datetime(2009, 1, 1), datetime.datetime(2014, 12, 31)),
        (datetime.datetime(2016, 2, 1), None)
    ]

    for start_date, end_date in period_list:
        test_info.find_best_period_between_target_period(result_path=result_path,
                                                         end_date=end_date,
                                                         start_date=start_date)
    vdisplay.stop()
