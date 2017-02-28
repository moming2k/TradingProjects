#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sh_allotment_report
# @Date: 2017-02-21
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import pandas as pd

from sh_downloader import SHDownloader


class SHAllotmentReport(SHDownloader):
    def __init__(self, logger=None):
        SHDownloader.__init__(self, logger)

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

        self.start_year = 1997
        self.init_constants()

    def init_constants(self):
        self.TRUE_COLUME = 'TRUE_COLUME'
        self.RIGHTS_TYPE = 'RIGHTS_TYPE'
        self.PRICE_OF_RIGHTS_ISSUE = 'PRICE_OF_RIGHTS_ISSUE'
        self.RATIO_OF_RIGHTS_ISSUE = 'RATIO_OF_RIGHTS_ISSUE'
        self.LISTING_DATE = 'LISTING_DATE'
        self.SECURITY_NAME = 'SECURITY_NAME'
        self.EX_RIGHTS_DATE = 'EX_RIGHTS_DATE'
        self.COMPANY_CODE = 'COMPANY_CODE'
        self.SECURITY_CODE = 'SECURITY_CODE'
        self.LAST_TRADE_DATE = 'LAST_TRADE_DATE'
        self.START_DATE_OF_REMITTANCE = 'START_DATE_OF_REMITTANCE'
        self.END_DATE_OF_REMITTANCE = 'END_DATE_OF_REMITTANCE'
        self.EXCHANGE_RATE = 'EXCHANGE_RATE'
        self.RECORD_DATE = 'RECORD_DATE'

    def _get_year_page_data(self, year, stock_type, page_num):
        self.logger.debug('Get year {}, stock type {}, page num {}'.format(year, stock_type, page_num))
        data_dict = self.get_data_dict.copy()
        data_dict['sqlId'] = 'COMMON_SSE_GP_SJTJ_MJZJ_PG_{}GPG_L'.format(stock_type.upper())
        data_dict['pageHelp.pageNo'] = page_num
        data_dict['pageHelp.beginPage'] = page_num
        data_dict['pageHelp.endPage'] = page_num * 10 + 1
        data_dict['searchyear'] = year
        return self.http_get(data_list=data_dict, refer_page=self.SH_ADDITIONAL_URL)

    def _decode_result_data(self, json_data, stock_type):
        result_dict = {self.SECURITY_TYPE: stock_type.upper(),
                       self.TRUE_COLUME: None,
                       self.RIGHTS_TYPE: None,
                       self.PRICE_OF_RIGHTS_ISSUE: None,
                       self.RATIO_OF_RIGHTS_ISSUE: None,
                       self.LISTING_DATE: None,
                       self.SECURITY_NAME: None,
                       self.EX_RIGHTS_DATE: None,
                       self.COMPANY_CODE: None,
                       self.SECURITY_CODE: None,
                       self.LAST_TRADE_DATE: None,
                       self.START_DATE_OF_REMITTANCE: None,
                       self.END_DATE_OF_REMITTANCE: None,
                       self.EXCHANGE_RATE: None,
                       self.RECORD_DATE: None,
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
            tmp_dict[self.TRUE_COLUME] = digit_times(self.get_dict_info(data, '{}_{}'.format(self.TRUE_COLUME,
                                                                                             stock_type.upper()),
                                                                        self.DATA_TYPE_FLOAT), 10000)
            tmp_dict[self.PRICE_OF_RIGHTS_ISSUE] = self.get_dict_info(data, '{}_{}'.format(self.PRICE_OF_RIGHTS_ISSUE,
                                                                                           stock_type.upper()),
                                                                      self.DATA_TYPE_FLOAT)
            tmp_dict[self.RATIO_OF_RIGHTS_ISSUE] = self.get_dict_info(data, '{}_{}'.format(self.RATIO_OF_RIGHTS_ISSUE,
                                                                                           stock_type.upper()),
                                                                      self.DATA_TYPE_FLOAT)
            tmp_dict[self.LISTING_DATE] = self.get_dict_info(data, '{}_{}'.format(self.LISTING_DATE,
                                                                                  stock_type.upper()),
                                                             self.DATA_TYPE_DATE)
            tmp_dict[self.EX_RIGHTS_DATE] = self.get_dict_info(data, '{}_{}'.format(self.EX_RIGHTS_DATE,
                                                                                    stock_type.upper()),
                                                               self.DATA_TYPE_DATE)
            tmp_dict[self.RECORD_DATE] = self.get_dict_info(data, '{}_{}'.format(self.RECORD_DATE,
                                                                                 stock_type.upper()),
                                                            self.DATA_TYPE_DATE)
            tmp_dict[self.START_DATE_OF_REMITTANCE] = self.get_dict_info(data, '{}_{}'.format(
                self.START_DATE_OF_REMITTANCE,
                stock_type.upper()),
                                                                         self.DATA_TYPE_DATE)
            tmp_dict[self.END_DATE_OF_REMITTANCE] = self.get_dict_info(data, '{}_{}'.format(
                self.END_DATE_OF_REMITTANCE,
                stock_type.upper()),
                                                                       self.DATA_TYPE_DATE)

            tmp_dict[self.SECURITY_NAME] = self.get_dict_info(data, '{}_{}'.format(self.SECURITY_NAME,
                                                                                   stock_type.upper()))
            tmp_dict[self.SECURITY_CODE] = self.get_dict_info(data, '{}_{}'.format(self.SECURITY_CODE,
                                                                                   stock_type.upper()))

            tmp_dict[self.COMPANY_CODE] = self.get_dict_info(data, self.COMPANY_CODE)

            if stock_type == 'a':
                pass

            else:
                tmp_dict[self.RIGHTS_TYPE] = self.get_dict_info(data, self.RIGHTS_TYPE)
                tmp_dict[self.EXCHANGE_RATE] = self.get_dict_info(data, self.EXCHANGE_RATE, self.DATA_TYPE_FLOAT)
                tmp_dict[self.LAST_TRADE_DATE] = self.get_dict_info(data, '{}_{}'.format(self.LAST_TRADE_DATE,
                                                                                         stock_type.upper()),
                                                                    self.DATA_TYPE_DATE)

            result_df.loc[i] = tmp_dict

        return result_df


if __name__ == '__main__':
    import sys
    import logging
    import datetime

    save_name = 'sh_allotment_report'

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    today_str = datetime.datetime.today().strftime('%Y%m%d')

    test = SHAllotmentReport()

    result_df = test.download_report()
    result_df.to_pickle('{}_{}.p'.format(today_str, save_name))
    result_df.to_excel('{}_{}.xlsx'.format(today_str, save_name),
                       index=False)
