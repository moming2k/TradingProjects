#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sz_downloader
# @Date: 2017-02-19
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import numpy as np

from basic_downloader import BasicDownloader


class SZDownloader(BasicDownloader):
    def http_post(self, data_list):
        return self.ctrl.post('{}?randnum={}'.format(self.SZ_POST_URL, np.random.rand()), data_list=data_list)
