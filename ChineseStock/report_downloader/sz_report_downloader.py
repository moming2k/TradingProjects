#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sz_report_downloader
# @Date: 2017-02-16
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import re
import time
import logging
import datetime

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from url_constants import URLConstant
from http_ctrl import HttpCtrl


class SZReportDownloader(URLConstant):
    def __init__(self, logger=None):
        if logger is None:
            logger = logging
        self.logger = logger.getLogger(self.__class__.__name__)
        self.ctrl = HttpCtrl(logger)

    def main_downloader(self):
        self.logger.info('Start to download info from sz website')
        main_page = self.ctrl.get(self.SZ_MAIN_URL)

        result_df_list = []

        soup = BeautifulSoup(main_page, 'lxml')

        result_df_list.append(self.get_current_page_ino(soup, True))

        while self.has_next_page(soup):
            soup = self.go_to_next_page(soup)
            result_df_list.append(self.get_current_page_ino(soup))
            time.sleep(3)

        result_df = pd.concat(result_df_list, axis=0, ignore_index=True)
        self.logger.info('Download finished')
        return result_df

    def get_current_page_ino(self, soup, is_first_page=False):
        columns = [self.REPORT_TICKER, self.REPORT_ANNOUNCE_DATE, self.REPORT_COMPANY_NAME,
                   self.REPORT_ACTION, self.REPORT_RELATIONSHIP, self.REPORT_REASON,
                   self.REPORT_POSITION, self.REPORT_CHANGE_NUMBER, self.REPORT_AVERAGE_PRICE,
                   self.REPORT_CHANGER_NAME]
        self.logger.info('Start to decode page info')
        report_df = pd.DataFrame(columns=columns)
        data_table = soup.find('table', id='REPORTID_tab1')

        def format_text(text):
            # return text
            if is_first_page:
                return text.encode('ISO-8859-1').decode('gbk')
            else:
                return text

        tr_list = data_table.findAll('tr')[1:]
        for i, tr in enumerate(tr_list):
            td_list = tr.findAll('td')
            result_df = {self.REPORT_TICKER: td_list[0].text,
                         self.REPORT_COMPANY_NAME: format_text(td_list[1].text),
                         self.REPORT_CHANGER_NAME: format_text(td_list[9].text),
                         self.REPORT_ANNOUNCE_DATE: datetime.datetime.strptime(td_list[3].text, '%Y-%m-%d'),
                         self.REPORT_CHANGE_NUMBER: int(td_list[4].text),
                         self.REPORT_AVERAGE_PRICE: float(td_list[5].text),
                         self.REPORT_REASON: format_text(td_list[6].text),
                         self.REPORT_POSITION: format_text(td_list[10].text),
                         self.REPORT_RELATIONSHIP: format_text(td_list[11].text)
                         }
            if result_df[self.REPORT_CHANGE_NUMBER] > 0:
                result_df[self.REPORT_ACTION] = self.OVERWEIGHT

            else:
                result_df[self.REPORT_ACTION] = self.REDUCTION
            report_df.loc[i] = result_df

        return report_df

    def has_next_page(self, soup):
        next_button = soup.find('input', {"class": "cls-navigate-next"})
        return len(next_button.get('onclick')) > 0

    def go_to_next_page(self, soup):
        next_button = soup.find('input', {"class": "cls-navigate-next"})
        random_number = np.random.rand()
        parameters = re.findall(r'\w+', next_button.get('onclick'))
        post_data = {'ACTIONID': 7,
                     'AJAX': 'AJAX-TRUE',
                     'CATALOGID': parameters[1],
                     'TABKEY': parameters[2],
                     'tab1PAGENUM': parameters[3],
                     'tab1PAGECOUNT': parameters[4],
                     'tab1RECORDCOUNT': parameters[5],
                     'REPORT_ACTION': 'navigate',
                     }
        self.logger.info('Next page is {}, total page number is {}'.format(parameters[3], parameters[4]))
        html = self.ctrl.post('{}{}'.format(self.SZ_POST_URL, random_number), post_data)
        return BeautifulSoup(html, 'lxml')


if __name__ == '__main__':
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    test = SZReportDownloader()
    result_df = test.main_downloader()
    result_df.to_excel('test.xlsx')
