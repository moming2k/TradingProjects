#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step7_generate_new_stock_return_info_stop_loss5
# @Date: 2017-01-31
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

from calculate_return_utils.calculate_return_utils_20170117_data import based_on_sr_rate_generate_result

stop_loss_rate = -0.05

if __name__ == '__main__':

    if hasattr(os, 'uname'):

        from xvfbwrapper import Xvfb

        vdisplay = Xvfb(width=1366, height=768)
        vdisplay.start()

        based_on_sr_rate_generate_result(stop_loss_rate)

        vdisplay.stop()

    else:
        based_on_sr_rate_generate_result(stop_loss_rate)
