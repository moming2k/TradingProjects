#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sh_report_downloader
# @Date: 2017-02-16
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import re
import time
import logging
import json
import datetime

import numpy as np
import pandas as pd

from url_constants import URLConstant
from http_ctrl import HttpCtrl


class SHReportDownloader(URLConstant):
    def __init__(self, logger=None):
        if logger is None:
            logger = logging
        self.logger = logger.getLogger(self.__class__.__name__)
        self.ctrl = HttpCtrl(logger)

    def main_downloader(self):
        self.logger.info('Start to download SH stock report')

        result_list = []
        page_num = self.get_maximum_page_count()
        for i in range(page_num):
            result_list.append(self.download_page(i + 1))
            time.sleep(3)
        result_df = pd.concat(result_list, axis=0, ignore_index=True)
        return result_df

    def get_maximum_page_count(self):
        headers = {'Referer': 'http://www.sse.com.cn/disclosure/credibility/supervision/change/'}
        request_dict = {'jsonCallBack': 'jsonpCallback3289',
                        'isPagination': 'true',
                        'sqlId': 'COMMON_SSE_XXPL_CXJL_SSGSGFBDQK_S',
                        'pageHelp.pageSize': 25,
                        'pageHelp.pageNo': 1,
                        'pageHelp.beginPage': 1,
                        'pageHelp.cacheSize': 1,
                        'pageHelp.endPage': 5,
                        '_': int(time.time() * 1000)}
        response_date = self.ctrl.get(self.SH_GET_URL, data_list=request_dict, headers=headers)
        data = re.findall(r'\((.+)\)', response_date)[0]
        page_num = json.loads(data)['pageHelp']['pageCount']
        self.logger.info('Maximum page number is {}'.format(page_num))
        return page_num

    def download_page(self, page_num):
        self.logger.info('Start to download page {}'.format(page_num))

        headers = {'Referer': 'http://www.sse.com.cn/disclosure/credibility/supervision/change/'}
        request_dict = {'jsonCallBack': 'jsonpCallback3289',
                        'isPagination': 'true',
                        'sqlId': 'COMMON_SSE_XXPL_CXJL_SSGSGFBDQK_S',
                        'pageHelp.pageSize': 25,
                        'pageHelp.pageNo': page_num,
                        'pageHelp.beginPage': page_num,
                        'pageHelp.cacheSize': 1,
                        'pageHelp.endPage': page_num + 5,
                        '_': int(time.time() * 1000)}

        response_date = self.ctrl.get(self.SH_GET_URL, data_list=request_dict, headers=headers)

        json_data = re.findall(r'\((.+)\)', response_date)[0]
        data = json.loads(json_data)['pageHelp']['data']

        columns = [self.REPORT_TICKER, self.REPORT_ANNOUNCE_DATE, self.REPORT_COMPANY_NAME,
                   self.REPORT_ACTION, self.REPORT_RELATIONSHIP, self.REPORT_REASON,
                   self.REPORT_POSITION, self.REPORT_CHANGE_NUMBER, self.REPORT_AVERAGE_PRICE,
                   self.REPORT_CHANGER_NAME]
        self.logger.info('Start to decode page info')
        report_df = pd.DataFrame(columns=columns)

        for i, datum in enumerate(data):
            result_df = {self.REPORT_TICKER: datum['COMPANY_CODE'],
                         self.REPORT_COMPANY_NAME: datum['COMPANY_ABBR'],
                         self.REPORT_CHANGER_NAME: datum['NAME'],
                         self.REPORT_ANNOUNCE_DATE: datetime.datetime.strptime(datum['FORM_DATE'], '%Y-%m-%d'),
                         self.REPORT_REASON: datum['CHANGE_REASON'],
                         self.REPORT_POSITION: datum['DUTY'],
                         self.REPORT_RELATIONSHIP: np.nan
                         }

            if datum['CHANGE_NUM'].isdigit():
                result_df[self.REPORT_CHANGE_NUMBER] = int(datum['CHANGE_NUM'])
            else:
                result_df[self.REPORT_CHANGE_NUMBER] = np.nan

            try:
                result_df[self.REPORT_AVERAGE_PRICE] = float(datum['CURRENT_AVG_PRICE'])

            except Exception:
                result_df[self.REPORT_AVERAGE_PRICE] = np.nan

            if result_df[self.REPORT_CHANGE_NUMBER] > 0:
                result_df[self.REPORT_ACTION] = self.OVERWEIGHT

            else:
                result_df[self.REPORT_ACTION] = self.REDUCTION
            report_df.loc[i] = result_df

        return report_df


if __name__ == '__main__':
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    test = SHReportDownloader()
    result_df = test.main_downloader()
    result_df.to_excel('test.xlsx')
