#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sh_dividend_report_downloader
# @Date: 2017-02-20
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import time

import pandas as pd
import numpy as np

from sh_downloader import SHDownloader


class ShDividendReportDownloader(SHDownloader):
    def download_report(self, start_date=None, end_date=None):
        if start_date is None:
            start_year = 1995

        else:
            start_year = start_date.year

        if end_date is None:
            end_year = 2017

        else:
            end_year = end_date.year

        result_list = []
        for year in range(start_year, end_year + 1):
            for stock_type in ['a', 'b']:
                self.logger.info('Start to download dividend info of year {} and stock {}'.format(year, stock_type))
                result_list.append(self._download_dividend_report(year, stock_type))
                time.sleep(3)

        result_df = pd.concat(result_list, axis=0, ignore_index=True)

        self.logger.info('Query finished')
        return result_df

    def _download_dividend_report(self, year, stock_type):
        get_data_dict = {'jsonCallBack': 'jsonpCallback',
                         'isPagination': 'true',
                         'sqlId': 'COMMON_SSE_GP_SJTJ_FHSG_{}GFH_L_NEW'.format(stock_type.upper()),
                         'pageHelp.pageSize': 25,
                         'pageHelp.pageNo': 1,
                         'pageHelp.beginPage': 1,
                         'pageHelp.endPage': 5,
                         'pageHelp.cacheSize': 1,
                         'record_date_{}'.format(stock_type): year,
                         'security_code_{}'.format(stock_type): '',
                         '_': 1487578673917, }
        result_list = []
        first_page_data = self.http_get(get_data_dict, self.SH_DIVIDEND_URL)
        total_page_number = first_page_data['pageHelp']['pageCount']
        result_list.append(self._decode_data_info(first_page_data))

        for page_num in range(2, total_page_number + 1):
            self.logger.debug('Get page {} data'.format(page_num))
            get_data_dict['pageHelp.pageNo'] = page_num
            get_data_dict['pageHelp.beginPage'] = page_num
            get_data_dict['pageHelp.endPage'] = page_num * 10 + 1
            json_data = self.http_get(get_data_dict, self.SH_DIVIDEND_URL)
            result_list.append(self._decode_data_info(json_data=json_data))

        result_df = pd.concat(result_list, axis=0, ignore_index=True)

        self.logger.debug('Query finished')
        return result_df

    def _decode_data_info(self, json_data):
        data_df = pd.DataFrame(columns=[self.TICKER, self.COMPANY_NAME, self.COMPANY_SHORT_NAME,
                                        self.DIVIDEND_BEFROE_TAX, self.DIVIDEND_AFTER_TAX, self.RECORD_DATE,
                                        self.EX_DIVIDEND_DATE, self.LAST_TRADE_DATE, self.EXCHANGE_RATE,
                                        self.SECURITY_TYPE, self.DIVIDEND_DATE])

        security_type = None

        for i, datum in enumerate(json_data['pageHelp']['data']):
            if security_type is None:
                if 'SECURITY_ABBR_A' in datum:
                    security_type = 'A'
                else:
                    security_type = 'B'

            data_df.loc[i] = {self.TICKER: datum['SECURITY_CODE_{}'.format(security_type)],
                              self.COMPANY_NAME: datum['FULL_NAME'],
                              self.COMPANY_SHORT_NAME: datum['SECURITY_ABBR_{}'.format(security_type)],
                              self.DIVIDEND_BEFROE_TAX: self.get_float_type_str(datum.get(
                                  'DIVIDEND_PER_SHARE1_{}'.format(security_type), None)),
                              self.DIVIDEND_AFTER_TAX: self.get_float_type_str(datum.get(
                                  'DIVIDEND_PER_SHARE2_{}'.format(security_type), None)),
                              self.EXCHANGE_RATE: self.get_float_type_str(datum.get('EXCHANGE_RATE')),
                              self.EX_DIVIDEND_DATE: self.get_datetime_type_str(datum.get(
                                  'EX_DIVIDEND_DATE_{}'.format(security_type), None
                              )),
                              self.RECORD_DATE: self.get_datetime_type_str(datum.get(
                                  'RECORD_DATE_{}'.format(security_type), None)),
                              self.DIVIDEND_DATE: self.get_datetime_type_str(datum.get(
                                  'DIVIDEND_DATE', None
                              )),
                              self.LAST_TRADE_DATE: self.get_datetime_type_str(datum.get(
                                  'LAST_TRADE_DATE_{}'.format(security_type), None
                              )),
                              self.SECURITY_TYPE: security_type,
                              }

        return data_df


if __name__ == '__main__':
    import sys
    import logging
    import datetime

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    today_str = datetime.datetime.today().strftime('%Y%m%d')

    test = ShDividendReportDownloader()

    result_df = test.download_report()
    result_df.to_pickle('{}_sh_dividend_report.p'.format(today_str))
    result_df.to_excel('{}_sh_dividend_report.xlsx'.format(today_str),
                       index=False)
