#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: os_related_function
# @Date: 2017-02-04
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os


def make_dirs(dir_or_dirs):
    for dir_path in dir_or_dirs:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
