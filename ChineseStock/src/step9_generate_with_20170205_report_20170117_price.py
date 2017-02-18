#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step9_generate_with_20170205_report_20170117_price
# @Date: 2017-02-05
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

from path_info import data_path
from calculate_return_utils_20170212 import based_on_sr_rate_generate_result

transaction_cost = 0.002
suffix = 'si_own_cd_insider'
report_path = os.path.join(data_path, 'report_data', 'report_data_20170205', 'ticker_sep')

if __name__ == '__main__':
    for stop_loss_rate in [-0.01, -0.02, -0.03, -0.04, -0.05]:
        if hasattr(os, 'uname'):

            from xvfbwrapper import Xvfb

            vdisplay = Xvfb(width=1366, height=768)
            vdisplay.start()

            based_on_sr_rate_generate_result(stop_loss_rate, folder_suffix=suffix, report_path=report_path,
                                             transaction_cost=transaction_cost)

            vdisplay.stop()

        else:
            based_on_sr_rate_generate_result(stop_loss_rate, folder_suffix=suffix, report_path=report_path,
                                             transaction_cost=transaction_cost)
