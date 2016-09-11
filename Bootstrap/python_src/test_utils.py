#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: test_utils
# Author: Mark Wang
# Date: 11/9/2016

import pandas as pd


class SPASRCCalculator(object):
    def __init__(self, data_path, bootstrap_num):
        self.data_file = pd.read_csv(data_path)
        self.bootstrap_time = bootstrap_num

    def get_spa(self, diff_type='Sharpe'):
        pass

    def get_spa_k(self, k=3, diff_type='Sharpe'):
        pass

    def get_src(self):
        pass

    def get_src_k(self, k=3):
        pass

    def get_stepwise_spa(self, diff_type='Sharpe'):
        pass

    def _bootstrap(self):
        pass
