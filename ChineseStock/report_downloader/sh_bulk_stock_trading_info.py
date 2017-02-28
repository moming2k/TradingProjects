#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sh_bulk_stock_trading_info
# @Date: 2017-02-22
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import time

import pandas as pd

from sh_downloader import SHDownloader


class SHBulkStockTradingInfo(SHDownloader):
    def __init__(self, logger=None):
        SHDownloader.__init__(self, logger)
        self.init_constant()

    def init_constant(self):
        self.STOCK_ID = 'stockid'
        self.TRADE_DATE = 'tradedate'
        self.TRADE_VOLUME = 'tradeqty'
        self.BRANCH_SELL = 'branchsell'
        self.BRANCH_BUY = 'branchbuy'
        self.TRADE_PRICE = 'tradeprice'
        self.IS_SPECIAL = 'ifZc'
        self.TRADE_AMOUNT = 'tradeamount'
        self.SECURITY_NAME = 'abbrname'

        self.get_data_dict = {'jsonCallBack': 'jsonpCallback79256',
                              'isPagination': 'true',
                              'sqlId': 'COMMON_SSE_XXPL_JYXXPL_DZJYXX_L_1',
                              'stockId': '',
                              'startDate': '1990-01-01',
                              'endDate': '2017-02-22',
                              'pageHelp.pageSize': 25,
                              'pageHelp.pageNo': 1,
                              'pageHelp.beginPage': 1,
                              'pageHelp.endPage': 5,
                              'pageHelp.cacheSize': 1,
                              '_': 1487691935978, }

        self.start_date = '1990-01-01'
        self.end_date = ''
        self.failed_page_list = []

    def download_report(self, start_date=None, end_date=None):
        if start_date is None:
            self.start_date = '1990-01-01'

        elif hasattr(start_date, 'strftime'):
            self.start_date = start_date.strftime('%Y-%m-%d')
        else:
            self.start_date = start_date

        if hasattr(end_date, 'strftime'):
            self.end_date = end_date.strftime('%Y-%m-%d')

        elif end_date is None:
            self.end_date = ''

        else:
            self.end_date = ''

        result_df = self._download_data()
        if self.failed_page_list:
            self.logger.warn('Failed page list is {}'.format(self.failed_page_list))

        return result_df

    def _download_data(self):
        self.logger.info('Start to download bulk stock trading info')
        self.logger.info('Start date is {}'.format(self.start_date))
        self.logger.info('End date is {}'.format(self.end_date))

        result_list = []

        current_page = max_page = 1

        while current_page <= max_page:
            self.logger.debug('Start to download page {}'.format(current_page))
            try:

                json_data = self._download_page(current_page)
                if current_page == 1:
                    max_page = json_data['pageHelp']['pageCount']

                result_list.append(self._decode_json_data(json_data))
            except Exception, err:
                self.logger.warn('Query page {} failed as {}'.format(current_page, err))
                self.failed_page_list.append(current_page)

            finally:
                current_page += 1
                time.sleep(1)

        if result_list:
            return pd.concat(result_list, axis=0, ignore_index=True)
        else:
            return pd.DataFrame()

    def _download_page(self, page_num):
        get_data_dict = self.get_data_dict.copy()
        get_data_dict['startDate'] = self.start_date
        get_data_dict['endDate'] = self.end_date
        get_data_dict['pageHelp.pageNo'] = page_num
        get_data_dict['pageHelp.beginPage'] = page_num
        get_data_dict['pageHelp.endPage'] = page_num * 10 + 1
        json_data = self.http_get(get_data_dict, self.SH_BLOCK_DEAL_URL)
        return json_data

    def _decode_json_data(self, json_data):
        result_dict = {self.STOCK_ID: None,
                       self.TRADE_DATE: None,
                       self.TRADE_VOLUME: None,
                       self.BRANCH_SELL: None,
                       self.BRANCH_BUY: None,
                       self.TRADE_PRICE: None,
                       self.IS_SPECIAL: None,
                       self.TRADE_AMOUNT: None,
                       self.SECURITY_NAME: None,
                       }

        data_list = json_data['pageHelp']['data']

        result_df = pd.DataFrame(columns=list(result_dict.keys()))
        for i, datum in enumerate(data_list):
            tmp_dict = result_dict.copy()
            tmp_dict[self.STOCK_ID] = self.get_dict_info(datum, self.STOCK_ID)
            tmp_dict[self.SECURITY_NAME] = self.get_dict_info(datum, self.SECURITY_NAME)
            tmp_dict[self.BRANCH_BUY] = self.get_dict_info(datum, self.BRANCH_BUY)
            tmp_dict[self.BRANCH_SELL] = self.get_dict_info(datum, self.BRANCH_SELL)
            tmp_dict[self.IS_SPECIAL] = self.get_dict_info(datum, self.IS_SPECIAL)
            tmp_dict[self.TRADE_PRICE] = self.get_dict_info(datum, self.TRADE_PRICE, self.DATA_TYPE_FLOAT)
            tmp_dict[self.TRADE_DATE] = self.get_dict_info(datum, self.TRADE_DATE, self.DATA_TYPE_DATE)
            tmp_dict[self.TRADE_VOLUME] = self.get_dict_info(datum, self.TRADE_VOLUME, self.DATA_TYPE_FLOAT_10000)
            tmp_dict[self.TRADE_AMOUNT] = self.get_dict_info(datum, self.TRADE_AMOUNT, self.DATA_TYPE_FLOAT_10000)

            result_df.loc[i] = tmp_dict

        return result_df


if __name__ == '__main__':
    import sys
    import logging
    import datetime

    save_name = 'sh_block_stock_trading_report'

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    today_str = datetime.datetime.today().strftime('%Y%m%d')

    test = SHBulkStockTradingInfo()

    result_df = test.download_report()
    result_df.to_pickle('{}_{}.p'.format(today_str, save_name))
    result_df.to_excel('{}_{}.xlsx'.format(today_str, save_name),
                       index=False)
