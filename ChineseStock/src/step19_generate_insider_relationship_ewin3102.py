#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step19_generate_insider_relationship_ewin3102
# @Date: 2017-02-17
# @Author: Mark Wang
# @Email: wangyouan@gmial.com
import os
import sys
import logging

from xvfbwrapper import Xvfb

from path_info import Path
from calculate_return_utils_20170216 import CalculateReturnUtils20170216
from step19_generate_insider_relationship_ewin3011 import ReportGenerator

if __name__ == '__main__':

    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    transaction_cost = 0.002
    suffix = 'insider_stock_20170214_alpha_no_neglect_all_types'
    report_path = os.path.join(Path.REPORT_DATA_PATH, 'report_info_buy_only')

    vdisplay = Xvfb(width=1366, height=768)
    vdisplay.start()

    test_info = ReportGenerator(transaction_cost=transaction_cost, report_path=report_path,
                                folder_suffix=suffix)

    for i in range(3, 6):
        test_info.main_progress(calculate_class=CalculateReturnUtils20170216, stop_loss_rate=i)

    vdisplay.stop()
