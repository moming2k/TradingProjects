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
import pandas as pd

from basic_downloader import BasicDownloader


class SHDownloader(BasicDownloader):
    def __init__(self, logger=None):
        BasicDownloader.__init__(self, logger)
        self.get_data_dict = {'jsonCallBack': 'jsonpCallback',
                              'isPagination': 'true',
                              'sqlId': 'COMMON_SSE_GP_SJTJ_MJZJ_PG_AGPG_L',
                              'pageHelp.pageSize': 25,
                              'pageHelp.pageNo': 1,
                              'pageHelp.beginPage': 1,
                              'pageHelp.endPage': 5,
                              'pageHelp.cacheSize': 1,
                              'searchyear': 2016,
                              '_': 1487657675314}

    def http_get(self, data_list, refer_page):
        if isinstance(data_list, dict) and '_' in data_list:
            data_list['_'] = self.get_time_info()

        if isinstance(data_list, dict) and 'jsonCallBack' in data_list:
            data_list['jsonCallBack'] = 'jsonCallBack{}'.format(np.random.randint(10000, 99999))

        response_date = self.ctrl.get(self.SH_GET_URL, data_list=data_list, headers={'Referer': refer_page})
        json_data = re.findall(r'\((.+)\)', response_date)[0].encode('gbk', errors='ignore')

        self.logger.debug('Response json data is {}'.format(json_data))
        json_data = unicode(json_data, encoding='gbk', errors='ignore')
        data =  json.loads(json_data, encoding='gbk')
        return data
        # return json.loads(json_data, encoding='cp936')

    @staticmethod
    def get_time_info():
        return int(time.time() * 1000)

    def _download_year_stock_type(self, year, stock_type):
        page_num = 1
        max_page_num = 1

        result_list = []

        while page_num <= max_page_num:
            json_data = self._get_year_page_data(year, stock_type, page_num)
            result_list.append(self._decode_result_data(json_data, stock_type))

            if page_num == 1:
                max_page_num = json_data['pageHelp']['pageCount']

            page_num += 1

        return pd.concat(result_list, axis=0, ignore_index=True)

    def _get_year_page_data(self, year, stock_type, page_num):
        pass

    def _decode_result_data(self, json_data, stock_type):
        pass

    def _download_year_data(self, year):
        self.logger.debug('Start to download year {} data'.format(year))
        result_list = [self._download_year_stock_type(year, 'a'),
                       self._download_year_stock_type(year, 'b')]

        return pd.concat(result_list, axis=0, ignore_index=True)
