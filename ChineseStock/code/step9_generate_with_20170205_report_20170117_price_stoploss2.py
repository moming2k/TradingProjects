#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step9_generate_with_20170205_report_20170117_price_stoploss2
# @Date: 2017-02-05
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

stop_loss_rate = -0.02

if __name__ == '__main__':
    from step9_generate_with_20170205_report_20170117_price_stoploss1 import based_on_stop_loss_rate_generate_result

    if hasattr(os, 'uname'):

        from xvfbwrapper import Xvfb

        vdisplay = Xvfb(width=1366, height=768)
        vdisplay.start()

        based_on_stop_loss_rate_generate_result(stop_loss_rate)

        vdisplay.stop()

    else:
        based_on_stop_loss_rate_generate_result(stop_loss_rate)
