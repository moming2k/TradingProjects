#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: test_utils
# Author: Mark Wang
# Date: 11/9/2016

import math

import pandas as pd


class SPASRCCalculator(object):
    def __init__(self, data_path, bootstrap_num):
        self.input_df = pd.read_csv(data_path, index_col=0)
        self.bootstrap_time = bootstrap_num
        self._mean = self.input_df.mean()
        self._demean = self.input_df - self._mean
        self._std = self._demean.std()
        self._sample_size, self._strategy_num = self.input_df.shape
        self.sspa_statistics = self._sample_size ** 0.5 * self._mean / self._std
        self.recenter_vector = self._mean / self._std
        threshold = - 2 * math.log(math.log(self._sample_size)) ** 0.5
        self.recenter_vector = self.recenter_vector[self.sspa_statistics <= threshold]

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

    def _bootstrap(self, diff_type):
        boot_result = pd.DataFrame(columns=self.input_df.keys())
        for i in range(self.bootstrap_time):
            if diff_type == 'Sharpe':
                boot_result.loc[i] = self._demean.sample(self._sample_size,
                                                         replace=True).mean() / self._std + self.recenter_vector
            else:
                boot_result.loc[i] = self._demean.sample(self._sample_size, replace=True).mean()

        return boot_result
