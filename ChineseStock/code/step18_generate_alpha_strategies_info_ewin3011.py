#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step18_generate_alpha_strategies_info_ewin3011
# @Date: 2017-02-16
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

from step18_generate_alpha_strategies_info_ewin3102 import based_on_sr_rate_generate_result

if __name__ == '__main__':
    from calculate_return_utils_20170216 import CalculateReturnUtils20170216
    from path_info import Path
    from util_function import print_info

    transaction_cost = 0.002
    suffix = 'insider_stock_20170214_alpha_strategy_no_neglect_period'
    report_path = os.path.join(Path.REPORT_DATA_PATH, 'report_info_buy_only')

    if hasattr(os, 'uname'):

        from xvfbwrapper import Xvfb

        vdisplay = Xvfb(width=1366, height=768)
        vdisplay.start()

        for i in [3]:
            print_info('SR is {}'.format(i))
            based_on_sr_rate_generate_result(i, suffix, transaction_cost=transaction_cost,
                                             report_path=report_path, calculate_class=CalculateReturnUtils20170216)

        vdisplay.stop()
