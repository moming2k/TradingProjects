#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sz_downloader
# @Date: 2017-02-19
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime

import numpy as np

from basic_downloader import BasicDownloader


class SZDownloader(BasicDownloader):
    def __init__(self, logger=None):
        BasicDownloader.__init__(self, logger)
        self.init_constant()

    def init_constant(self):
        self.start_date = None
        self.end_date = None

    def http_post(self, data_list):
        return self.ctrl.post('{}?randnum={}'.format(self.SZ_POST_URL, np.random.rand()), data_list=data_list)

    def has_next_page(self, soup):
        next_button = soup.find('input', {"class": "cls-navigate-next", 'type': 'button'})
        return hasattr(next_button, 'get') and len(next_button.get('onclick')) > 0

    def download_report(self, start_date=None, end_date=None):
        if start_date is None:
            start_date = self.start_date

        elif hasattr(start_date, 'strftime'):
            pass

        else:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')

        if end_date is None:
            end_date = self.end_date

        elif hasattr(end_date, 'strftime'):
            pass

        else:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        return self._download_report(start_date, end_date)

    def _download_report(self, start_date, end_date):
        pass
