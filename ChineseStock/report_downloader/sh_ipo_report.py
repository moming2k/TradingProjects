#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sh_ipo_report
# @Date: 2017-02-21
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import pandas as pd

from sh_downloader import SHDownloader


class SHIPOReport(SHDownloader):
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

        self.start_year = 1991
        self.init_constants()

    def init_constants(self):
        self.BEGIN_DATE = 'BEGIN_DATE'

        # 加权法
        self.ISSUED_PROFIT_RATE_1 = 'ISSUED_PROFIT_RATE'

        # 摊薄法
        self.ISSUED_PROFIT_RATE_2 = 'ISSUED_PROFIT_RATE_2'

        self.MAIN_UNDERWRITER_NAME = 'MAIN_UNDERWRITER_NAME'
        self.LISTING_DATE = 'LISTING_DATE'
        self.SECURITY_NAME = 'SECURITY_NAME'
        self.COMPANY_CODE = 'COMPANY_CODE'
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
        self.PUBLISHED_DATE = 'EXCHANGE_RATE'
        self.GOT_RATE = 'GOT_RATE'

    def _get_year_page_data(self, year, stock_type, page_num):
        self.logger.debug('Get year {}, stock type {}, page num {}'.format(year, stock_type, page_num))
        data_dict = self.get_data_dict.copy()
        if stock_type.upper() == 'A':
            data_dict['sqlId'] = 'COMMON_SSE_GP_SJTJ_MJZJ_SF_AGSF_ZQDMPX_L_NEW_DESC'
        else:
            data_dict['sqlId'] = 'COMMON_SSE_GP_SJTJ_MJZJ_SF_BGSF_ZQDM_L_NEW_ASC'
        data_dict['pageHelp.pageNo'] = page_num
        data_dict['pageHelp.beginPage'] = page_num
        data_dict['pageHelp.endPage'] = page_num * 10 + 1
        data_dict['searchyear'] = year
        return self.http_get(data_list=data_dict, refer_page=self.SH_ADDITIONAL_URL)

    def _decode_result_data(self, json_data, stock_type):
        result_dict = {self.SECURITY_TYPE: stock_type.upper(),
                       self.BEGIN_DATE: None,
                       self.ISSUED_PROFIT_RATE_1: None,
                       self.ISSUED_PROFIT_RATE_2: None,
                       self.MAIN_UNDERWRITER_NAME: None,
                       self.LISTING_DATE: None,
                       self.SECURITY_NAME: None,
                       self.COMPANY_CODE: None,
                       self.SECURITY_CODE: None,
                       self.ISSUED_VOLUME: None,
                       self.END_DATE: None,
                       self.ANNOUNCED_DATE: None,
                       self.COORDINATOR: None,
                       self.RAISED_MONEY: None,
                       self.RAISED_MONEY_USD: None,
                       self.ISSUED_MODE_CODE: None,
                       self.ISSUED_PRICE: None,
                       self.ISSUED_PRICE_USD: None,
                       self.PUBLISHED_DATE: None,
                       self.GOT_RATE: None,
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
            tmp_dict[self.BEGIN_DATE] = self.get_dict_info(data, self.BEGIN_DATE, self.DATA_TYPE_DATE)
            tmp_dict[self.ISSUED_PROFIT_RATE_1] = self.get_dict_info(data, '{}_{}1'.format(self.ISSUED_PROFIT_RATE_1,
                                                                                           stock_type.upper()),
                                                                     self.DATA_TYPE_FLOAT)
            tmp_dict[self.ISSUED_PROFIT_RATE_2] = self.get_dict_info(data, '{}_{}2'.format(self.ISSUED_PROFIT_RATE_1,
                                                                                           stock_type.upper()),
                                                                     self.DATA_TYPE_FLOAT)
            tmp_dict[self.LISTING_DATE] = self.get_dict_info(data, '{}_{}'.format(self.LISTING_DATE,
                                                                                  stock_type.upper()),
                                                             self.DATA_TYPE_DATE)
            tmp_dict[self.END_DATE] = self.get_dict_info(data, self.END_DATE, self.DATA_TYPE_DATE)
            tmp_dict[self.ANNOUNCED_DATE] = self.get_dict_info(data, self.ANNOUNCED_DATE, self.DATA_TYPE_DATE)
            tmp_dict[self.MAIN_UNDERWRITER_NAME] = self.get_dict_info(data, '{}_{}'.format(self.MAIN_UNDERWRITER_NAME,
                                                                                           stock_type.upper()))
            tmp_dict[self.ISSUED_MODE_CODE] = self.get_dict_info(data, '{}_{}'.format(self.ISSUED_MODE_CODE,
                                                                                      stock_type.upper()))

            tmp_dict[self.SECURITY_CODE] = self.get_dict_info(data, '{}_{}'.format(self.SECURITY_CODE,
                                                                                   stock_type.upper()))
            tmp_dict[self.SECURITY_NAME] = self.get_dict_info(data, '{}_{}'.format(self.SECURITY_NAME,
                                                                                   stock_type.upper()))

            tmp_dict[self.COMPANY_CODE] = self.get_dict_info(data, self.COMPANY_CODE)

            tmp_dict[self.ISSUED_VOLUME] = digit_times(self.get_dict_info(data, '{}_{}'.format(self.ISSUED_VOLUME,
                                                                                               stock_type.upper()),
                                                                          self.DATA_TYPE_FLOAT), 10000)

            if stock_type == 'a':
                tmp_dict[self.RAISED_MONEY] = digit_times(self.get_dict_info(data, '{}_A'.format(self.RAISED_MONEY),
                                                                             self.DATA_TYPE_FLOAT), 10000)
                tmp_dict[self.ISSUED_PRICE] = self.get_dict_info(data, '{}_A'.format(self.ISSUED_PRICE),
                                                                 self.DATA_TYPE_FLOAT)
                tmp_dict[self.GOT_RATE] = self.get_dict_info(data, '{}_A'.format(self.GOT_RATE),
                                                             self.DATA_TYPE_FLOAT)
                tmp_dict[self.PUBLISHED_DATE] = self.get_dict_info(data, self.PUBLISHED_DATE,
                                                                   self.DATA_TYPE_DATE)

            else:
                tmp_dict[self.COORDINATOR] = self.get_dict_info(data, '{}_B'.format(self.COORDINATOR))
                tmp_dict[self.RAISED_MONEY] = digit_times(self.get_dict_info(data, '{}_B1'.format(self.RAISED_MONEY),
                                                                             self.DATA_TYPE_FLOAT), 10000)
                tmp_dict[self.RAISED_MONEY_USD] = digit_times(
                    self.get_dict_info(data, '{}_B2'.format(self.RAISED_MONEY),
                                       self.DATA_TYPE_FLOAT), 10000)
                tmp_dict[self.ISSUED_PRICE] = self.get_dict_info(data, '{}_B1'.format(self.ISSUED_PRICE),
                                                                 self.DATA_TYPE_FLOAT)
                tmp_dict[self.ISSUED_PRICE_USD] = self.get_dict_info(data, '{}_B2'.format(self.ISSUED_PRICE),
                                                                     self.DATA_TYPE_FLOAT)

            result_df.loc[i] = tmp_dict

        return result_df


if __name__ == '__main__':
    import sys
    import logging
    import datetime

    save_name = 'sh_ipo_report'

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    today_str = datetime.datetime.today().strftime('%Y%m%d')

    test = SHIPOReport()

    result_df = test.download_report()
    result_df.to_pickle('{}_{}.p'.format(today_str, save_name))
    result_df.to_excel('{}_{}.xlsx'.format(today_str, save_name),
                       index=False)
