#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: test_multiprocess
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import multiprocessing

for j in range(4):
    def print_test(i):
        print j * 4


    pool = multiprocessing.Pool(2)
    pool.map(print_test, range(5))
    pool.close()
