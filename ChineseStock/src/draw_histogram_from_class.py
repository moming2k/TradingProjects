#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: draw_histogram_from_class
# @Date: 2017-02-17
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import sys
import logging

from path_info import Path
from report_generator_draw_alpha_strategies import ReportGeneratorDrawAlphaStrategies

if __name__ == '__main__':
    transaction_cost = 0.002

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')
    suffix = 'insider_stock_20170214_alpha_no_neglect_all_types'
    report_path = os.path.join(Path.REPORT_DATA_PATH, 'report_info_buy_only')
    test = ReportGeneratorDrawAlphaStrategies(transaction_cost, folder_suffix=suffix, report_path=report_path)
    result_path = os.path.join(Path.RESULT_PATH, 'insider_stock_20170214_alpha_no_neglect_all_types')

    from xvfbwrapper import Xvfb

    vdisplay = Xvfb(width=1366, height=768)
    vdisplay.start()
    test.generate_histogram_from_result_path(result_path)

    vdisplay.stop()
