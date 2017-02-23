#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: ifeng_finance_downloader
# @Date: 2017-02-23
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

from basic_downloader import BasicDownloader


class IfengFinanceDownloader(BasicDownloader):
    def __init__(self, logger=None):
        BasicDownloader.__init__(self, logger)
        self.init_constant()

    def init_constant(self):
        self.DIVIDEND_URL = 'http://app.finance.ifeng.com/data/stock/fhpxjl.php'

        self.ANNOUNCE_DATE = 'AnnounceDate'
        self.TARGET = 'Target'
