#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sh_download_additional_data
# @Date: 2017-02-21
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import pandas as pd

from sh_downloader import SHDownloader


class SHDownloadAdditionalData(SHDownloader):
    def __init__(self, logger=None):
        SHDownloader.__init__(self, logger)

        self.get_data_dict = {'jsonCallBack': 'jsonpCallback',
                              'isPagination': 'true',
                              'sqlId': 'COMMON_SSE_GP_SJTJ_MJZJ_ZF_AGZF_L',
                              'pageHelp.pageSize': 25,
                              'pageHelp.pageNo': 1,
                              'pageHelp.beginPage': 1,
                              'pageHelp.endPage': 5,
                              'pageHelp.cacheSize': 1,
                              'searchyear': 2016,
                              '_': 1487657675314}

        self.start_year = 1999
        self.init_constants()

    def init_constants(self):
        self.COMPANY_CODE = 'COMPANY_CODE'
        self.BEGIN_DATE = 'BEGIN_DATE'
        self.MAIN_UNDERWRITER_NAME = 'MAIN_UNDERWRITER_NAME'
        self.SECURITY_NAME = 'SECURITY_NAME'
        self.SECURITY_CODE = 'SECURITY_CODE'
        self.ISSUED_VOLUME = 'ISSUED_VOLUME'
        self.END_DATE = 'END_DATE'
        self.ANNOUNCED_DATE = 'ANNOUNCED_DATE'
        self.COORDINATOR = 'COORDINATOR'
        self.RAISED_MONEY = 'RAISED_MONEY'
        self.RAISED_MONEY_USD = 'RAISED_MONEY_USD'
        self.ISSUED_MODE_CODE = 'ISSUED_MODE_CODE'
        self.ISSUED_PRICE = 'ISSUED_PRICE'
        self.ISSUED_PRICE_USD = 'ISSUED_PRICE_USD'
        self.LISTING_DATE = 'LISTING_DATE'

    def _download_year_data(self, year):
        self.logger.debug('Start to download year {} data'.format(year))
        result_list = [self._download_year_stock_type(year, 'a'),
                       self._download_year_stock_type(year, 'b')]

        return pd.concat(result_list, axis=0, ignore_index=True)

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
        self.logger.debug('Get year {}, stock type {}, page num {}'.format(year, stock_type, page_num))
        data_dict = self.get_data_dict.copy()
        data_dict['sqlId'] = 'COMMON_SSE_GP_SJTJ_MJZJ_ZF_{}GZF_L'.format(stock_type.upper())
        data_dict['pageHelp.pageNo'] = page_num
        data_dict['pageHelp.beginPage'] = page_num
        data_dict['pageHelp.endPage'] = page_num * 10 + 1
        data_dict['searchyear'] = year
        return self.http_get(data_list=data_dict, refer_page=self.SH_ADDITIONAL_URL)

    def _decode_result_data(self, json_data, stock_type):
        result_dict = {self.SECURITY_TYPE: stock_type,
                       self.COMPANY_CODE: None,
                       self.MAIN_UNDERWRITER_NAME: None,
                       self.SECURITY_NAME: None,
                       self.SECURITY_CODE: None,
                       self.ISSUED_VOLUME: None,
                       self.END_DATE: None,
                       self.BEGIN_DATE: None,
                       self.ANNOUNCED_DATE: None,
                       self.RAISED_MONEY: None,
                       self.RAISED_MONEY_USD: None,
                       self.ISSUED_PRICE: None,
                       self.ISSUED_PRICE_USD: None,
                       self.ISSUED_MODE_CODE: None,
                       self.COORDINATOR: None,
                       self.LISTING_DATE: None
                       }

        data_list = json_data['pageHelp']['data']
        result_df = pd.DataFrame(columns=list(result_dict))

        def digit_times(value, target_times):
            if value is None or hasattr(value, 'split'):
                return value
            else:
                return value * target_times

        for i, data in enumerate(data_list):
            tmp_dict = result_dict.copy()
            tmp_dict[self.COMPANY_CODE] = data[self.COMPANY_CODE]

            tmp_dict[self.END_DATE] = self.get_datetime_type_str(data[self.END_DATE])
            tmp_dict[self.BEGIN_DATE] = self.get_datetime_type_str(data[self.BEGIN_DATE])
            tmp_dict[self.ANNOUNCED_DATE] = self.get_datetime_type_str(data[self.ANNOUNCED_DATE])
            tmp_dict[self.LISTING_DATE] = self.get_datetime_type_str(data.get('{}_{}'.format(self.LISTING_DATE,
                                                                                             stock_type.upper())))

            tmp_dict[self.MAIN_UNDERWRITER_NAME] = data['{}_{}'.format(self.MAIN_UNDERWRITER_NAME, stock_type.upper())]
            tmp_dict[self.ISSUED_MODE_CODE] = data['{}_{}'.format(self.ISSUED_MODE_CODE, stock_type.upper())]
            tmp_dict[self.SECURITY_NAME] = data['{}_{}'.format(self.SECURITY_NAME, stock_type.upper())]
            tmp_dict[self.SECURITY_CODE] = data['{}_{}'.format(self.SECURITY_CODE, stock_type.upper())]
            tmp_dict[self.ISSUED_VOLUME] = digit_times(self.get_float_type_str(
                data['{}_{}'.format(self.ISSUED_VOLUME, stock_type.upper())]
            ), 10000)

            if stock_type == 'a':
                tmp_dict[self.RAISED_MONEY] = digit_times(self.get_float_type_str(
                    data['{}_A'.format(self.RAISED_MONEY)]
                ), 10000)
                tmp_dict[self.ISSUED_PRICE] = self.get_float_type_str(
                    data['{}_A'.format(self.ISSUED_PRICE)]
                )

            else:
                tmp_dict[self.COORDINATOR] = data['{}_B'.format(self.COORDINATOR)]

                tmp_dict[self.RAISED_MONEY] = digit_times(self.get_float_type_str(
                    data['{}_B2'.format(self.RAISED_MONEY)]
                ), 10000)
                tmp_dict[self.RAISED_MONEY_USD] = digit_times(self.get_float_type_str(
                    data['{}_B1'.format(self.RAISED_MONEY)]
                ), 10000)

                tmp_dict[self.ISSUED_PRICE] = digit_times(self.get_float_type_str(
                    data['{}_B2'.format(self.ISSUED_PRICE)]
                ), 10000)
                tmp_dict[self.ISSUED_PRICE_USD] = digit_times(self.get_float_type_str(
                    data['{}_B1'.format(self.ISSUED_PRICE)]
                ), 10000)

            result_df.loc[i] = tmp_dict

        return result_df


if __name__ == '__main__':
    import sys
    import logging
    import datetime

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    today_str = datetime.datetime.today().strftime('%Y%m%d')

    test = SHDownloadAdditionalData()

    result_df = test.download_report()
    result_df.to_pickle('{}_sh_additional_report.p'.format(today_str))
    result_df.to_excel('{}_sh_additional_report.xlsx'.format(today_str),
                       index=False)
