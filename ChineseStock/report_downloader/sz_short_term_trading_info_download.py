#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sz_short_term_trading_info_downloader
# @Date: 2017-02-19
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import re
import time

import pandas as pd
from bs4 import BeautifulSoup

from sz_downloader import SZDownloader


class SZShortTermTradingInfoDownloader(SZDownloader):
    def download_report(self, start_date=None, end_date=None):
        page_number, record_num = self.get_total_page_number(start_date, end_date)

        self.logger.info('There are {} pages, and {} records in total'.format(page_number, record_num))
        report_list = []

        for i in range(page_number):
            self.logger.info('Start to download page {} info'.format(i + 1))
            report_list.append(self.download_page_num(i + 1, start_date, end_date, record_num, page_number))
            time.sleep(3)

        report_df = pd.concat(report_list, axis=0, ignore_index=True)
        self.logger.info('Download short term trading info finished')
        return report_df

    def download_page_num(self, page_num, start_date, end_date, record_num, total_page_num):
        post_data = {'ACTIONID': 7,
                     'AJAX': 'AJAX-TRUE',
                     'CATALOGID': '1800_cxda',
                     'TABKEY': 'tab1',
                     'tab1PAGENUM': page_num,
                     'tab1PAGECOUNT': total_page_num,
                     'tab1RECORDCOUNT': record_num,
                     'REPORT_ACTION': 'navigate',
                     'txtStart': start_date.strftime('%Y-%m-%d') if hasattr(start_date, 'strftime') else '',
                     'txtEnd': end_date.strftime('%Y-%m-%d') if hasattr(end_date, 'strftime') else ''}
        response = self.http_post(post_data)
        soup = BeautifulSoup(response, 'lxml')
        info_list = soup.find('table', {'id': 'REPORTID_tab1'}).findAll('tr')[1:]
        result_df = pd.DataFrame(columns=[self.TICKER, self.COMPANY_NAME, self.SHAREHOLDER_NAME, self.SHAREHOLDER_TYPE,
                                          self.REPORT_ANNOUNCE_DATE, self.BUY_OR_SELL, self.VOLUME, self.PRICE])

        for i, info in enumerate(info_list):
            if info is None:
                continue
            parameters = info.findAll('td')
            result_df.loc[i] = {self.TICKER: parameters[0].text,
                                self.COMPANY_NAME: parameters[1].text,
                                self.SHAREHOLDER_NAME: parameters[2].text,
                                self.SHAREHOLDER_TYPE: parameters[3].text,
                                self.REPORT_ANNOUNCE_DATE: self.get_datetime_type_str(parameters[4].text),
                                self.BUY_OR_SELL: parameters[5].text,
                                self.VOLUME: self.get_int_type_str(parameters[6].text),
                                self.PRICE: self.get_float_type_str(parameters[7].text)}

        return result_df

    def get_total_page_number(self, start_date, end_date):

        self.logger.info('Start to query total page number')
        post_data = {'ACTIONID': 7,
                     'AJAX': 'AJAX-TRUE',
                     'CATALOGID': '1800_cxda',
                     'TABKEY': 'tab1',
                     'REPORT_ACTION': 'search',
                     'selectGsbk': '',
                     'txtDMorJC': '',
                     'selectGdlb': '',
                     'txtGdmc': '',
                     'txtStart': start_date.strftime('%Y-%m-%d') if hasattr(start_date, 'strftime') else '',
                     'txtEnd': end_date.strftime('%Y-%m-%d') if hasattr(end_date, 'strftime') else ''}

        response = self.http_post(post_data)

        soup = BeautifulSoup(response, 'lxml')
        next_button = soup.find('input', {"class": "cls-navigate-next", 'type': 'button'})
        if len(next_button.get('onclick')) == 0:

            table_trs = soup.find('table', {'id': 'REPORTID_tab1'}).findAll('tr')
            return 1, len(table_trs) - 1

        else:
            parameters = re.findall(r'\w+', next_button.get('onclick'))
            return int(parameters[-2]), int(parameters[-1])


if __name__ == '__main__':
    import sys
    import os
    import logging
    import datetime

    today_str = datetime.datetime.today().strftime('%Y%m%d')

    root_path = SZShortTermTradingInfoDownloader.get_root_path()

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')
    downloader = SZShortTermTradingInfoDownloader()
    result_df = downloader.download_report()
    result_df.to_pickle(os.path.join(root_path, 'downloaded_report',
                                     '{}_sz_short_term_trading_report.p'.format(today_str)))
    result_df.to_excel(os.path.join(root_path, 'downloaded_report',
                                    '{}_sz_short_term_trading_report.xlsx'.format(today_str)),
                       index=False)
