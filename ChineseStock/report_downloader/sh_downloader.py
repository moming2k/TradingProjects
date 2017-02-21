#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sh_downloader
# @Date: 2017-02-20
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import re
import json
import time

import numpy as np

from basic_downloader import BasicDownloader


class SHDownloader(BasicDownloader):
    def http_get(self, data_list, refer_page):
        if isinstance(data_list, dict) and '_' in data_list:
            data_list['_'] = self.get_time_info()

        if isinstance(data_list, dict) and 'jsonCallBack' in data_list:
            data_list['jsonCallBack'] = 'jsonCallBack{}'.format(np.random.randint(10000, 99999))

        response_date = self.ctrl.get(self.SH_GET_URL, data_list=data_list, headers={'Referer': refer_page})
        json_data = re.findall(r'\((.+)\)', response_date)[0].encode('gbk')

        self.logger.debug('Response json data is {}'.format(json_data))
        return json.loads(json_data, encoding='gbk')

    @staticmethod
    def get_time_info():
        return int(time.time() * 1000)
