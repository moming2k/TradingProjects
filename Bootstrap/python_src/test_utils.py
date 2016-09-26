#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: test_utils
# Author: Mark Wang
# Date: 11/9/2016

import math
import sys
import logging

import pandas as pd
import numpy as np

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s'")


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
        self.logger = logging.getLogger(self.__class__.__name__)

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

    def _bootstrap(self, diff_type, input_demean=None, input_std=None):
        if input_demean is None:
            input_demean = self._demean

        if input_std is None:
            input_std = self._std

        sample_size = input_demean.shape[0]
        boot_result = pd.DataFrame(columns=self.input_df.keys())
        for i in range(self.bootstrap_time):
            if diff_type == 'Sharpe':
                boot_result.loc[i] = (self.input_df.sample(sample_size, replace=True).mean()
                                      - self._mean) / input_std
            else:
                boot_result.loc[i] = self.input_df.sample(sample_size, replace=True).mean() - self._mean

        return boot_result

    def main_test(self, test_time=500, max_com=10, k=3, data_partition=1):
        self.logger.info("Start to test SPA and SRC file")
        self.logger.info("The data would be split into {} parts".format(data_partition))
        if data_partition == 1:
            df_list = [self.input_df]
        else:
            df_list = np.array_split(self.input_df, data_partition)

        for i, sub_df in enumerate(df_list):
            self.logger.info("Start to handle the {} df, its data index is from {} to {}".format(i + 1, sub_df.index[0],
                                                                                                 sub_df.index[1]))
