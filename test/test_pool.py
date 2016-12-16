#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: test_pool
# @Date: 2016-12-16
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import multiprocessing
from functools import partial

process_num = 2

a = [1, 2, 3, 4, 5]
b = [1, 2, 3]


def compare_ab(i):
    return i[0] > i[1]


def compare(i, j):
    return i > j


if __name__ == '__main__':

    pool = multiprocessing.Pool(process_num)
    for m in a:
        f = partial(compare, m)
        print pool.map(f, b)

        data = [(n, m) for n in b]
        print pool.map(compare_ab, data)

    pool.close()
    pool.join()
