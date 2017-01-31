#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step7_generate_new_stock_return_info_stop_loss3
# @Date: 2017-01-31
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

from calculate_return_utils_new_data import based_on_stop_loss_rate_generate_result

stop_loss_rate = -0.01

if hasattr(os, 'uname'):

    from xvfbwrapper import Xvfb

    vdisplay = Xvfb(width=1366, height=768)
    vdisplay.start()

    based_on_stop_loss_rate_generate_result(stop_loss_rate)

    vdisplay.stop()

else:
    based_on_stop_loss_rate_generate_result(stop_loss_rate)
