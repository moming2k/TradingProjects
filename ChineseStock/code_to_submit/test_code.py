#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: test_code
# @Date: 2017-03-14
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

from main import calculate_data_and_return_picture

if __name__ == '__main__':
    from xvfbwrapper import Xvfb

    vdisplay = Xvfb(width=1366, height=768)
    vdisplay.start()

    # insider best sharpe and best return are all the same
    # calculate_data_and_return_picture('insider', 6, 14, 5)

    # forecast best sharpe and best return are all the same
    calculate_data_and_return_picture('forecast', 5, 14, 5)

    # Best sharpe ratio after 2016 using forecast
    calculate_data_and_return_picture('forecast', 6, 14, 4)

    vdisplay.stop()
