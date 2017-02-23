#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: ifeng_finance_dividend_downloader
# @Date: 2017-02-23
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import re
import time

import pandas as pd
from bs4 import BeautifulSoup

from basic_downloader import BasicDownloader


class IfengFinanceDividendDownloader(BasicDownloader):
    def __init__(self, logger=None):
        BasicDownloader.__init__(self, logger)
        self.init_constant()

    def init_constant(self):
        self.DIVIDEND_URL = 'http://app.finance.ifeng.com/data/stock/fhpxjl.php'

        self.ANNOUNCE_DAY = 'Announce_Day'
        self.TARGET = 'Target'
        self.DIVIDEND_PRE10 = 'Dividend_Per10'
        self.DIVIDEND_PRE10_TAXED = 'Dividend_Per10_Taxed'
        self.BONUS_SHARES_PRE10 = 'Bonus_Shares_Per10'
        self.CAPITALIZATION_PRE10 = 'Capitalization_Per10'
        self.REGISTRATION_DAY = 'Registration_day'
        self.FINAL_TRADING_DAY = 'Final_trading_day'
        self.EX_DIVIDEND_DAY = 'EX_Dividend_Day'
        self.CAPITALIZATION_LISTING_DAY = 'Capitalization_Listing'
        self.BONUS_LISTING_DAY = 'Bonus_Listing'
        self.SHARES_BASE = 'Shares_base'
        self.DIVIDEND_DATE = 'Dividend_day'
        self.DIVIDEND_CUTOFF_DATE = 'Dividend_cutoff_day'

    def download_dividend(self, ticker_list):
        self.logger.info('Start to download ticker info {}'.format(ticker_list))

        result_list = []
        for ticker in ticker_list:
            result_list.append(self._download_ticker_info(ticker))
            time.sleep(3)

        if result_list:
            return pd.concat(result_list, axis=0, ignore_index=True)
        else:
            return pd.DataFrame()

    def _download_ticker_info(self, ticker):
        self.logger.info('Download result of ticker {}'.format(ticker))
        get_data_dict = {'symbol': ticker}

        html = self.ctrl.get(self.DIVIDEND_URL, get_data_dict)
        soup = BeautifulSoup(html, 'lxml')

        with open('temp.p', 'w') as f:
            import pickle

            pickle.dump(html, f)

        result_dict = {self.ANNOUNCE_DAY: None,
                       self.TICKER: ticker,
                       self.DIVIDEND_CUTOFF_DATE: None,
                       self.TARGET: None,
                       self.SHARES_BASE: None,
                       self.DIVIDEND_PRE10: None,
                       self.DIVIDEND_PRE10_TAXED: None,
                       self.BONUS_SHARES_PRE10: None,
                       self.CAPITALIZATION_PRE10: None,
                       self.REGISTRATION_DAY: None,
                       self.EX_DIVIDEND_DATE: None,
                       self.LAST_TRADE_DATE: None,
                       self.DIVIDEND_DATE: None,
                       self.BONUS_LISTING_DAY: None,
                       self.CAPITALIZATION_LISTING_DAY: None
                       }
        tables = soup.find_all('table', attrs={'width': '706'})

        result_df = pd.DataFrame(columns=list(result_dict.keys()))

        def get_useful_digit(input_str):
            digit = re.findall(r'[\d\.]+', input_str)
            if digit:
                return digit[0]
            else:
                return None

        for i, table in enumerate(tables):
            tmp_dict = result_dict.copy()

            rows = table.find_all('tr')

            if len(rows) != 7:
                continue
            td_list = map(lambda x: x.find_all('td'), rows)

            tmp_dict[self.ANNOUNCE_DAY] = self.get_datetime_type_str(td_list[0][1].text)
            tmp_dict[self.DIVIDEND_CUTOFF_DATE] = self.get_datetime_type_str(td_list[0][3].text)

            tmp_dict[self.TARGET] = td_list[1][1].text
            tmp_dict[self.SHARES_BASE] = self.get_int_type_str(get_useful_digit(td_list[1][3].text))

            tmp_dict[self.DIVIDEND_PRE10] = self.get_float_type_str(get_useful_digit(td_list[2][1].text))
            tmp_dict[self.DIVIDEND_PRE10_TAXED] = self.get_float_type_str(get_useful_digit(td_list[2][3].text))

            tmp_dict[self.BONUS_SHARES_PRE10] = self.get_float_type_str(get_useful_digit(td_list[3][1].text))
            tmp_dict[self.CAPITALIZATION_PRE10] = self.get_float_type_str(get_useful_digit(td_list[3][3].text))

            tmp_dict[self.REGISTRATION_DAY] = self.get_datetime_type_str(td_list[4][1].text)
            tmp_dict[self.EX_DIVIDEND_DATE] = self.get_datetime_type_str(td_list[4][3].text)

            tmp_dict[self.LAST_TRADE_DATE] = self.get_datetime_type_str(td_list[5][1].text)
            tmp_dict[self.DIVIDEND_DATE] = self.get_datetime_type_str(td_list[5][3].text)

            tmp_dict[self.BONUS_LISTING_DAY] = self.get_datetime_type_str(td_list[6][1].text)
            tmp_dict[self.CAPITALIZATION_LISTING_DAY] = self.get_datetime_type_str(td_list[6][3].text)

            result_df.loc[i] = tmp_dict

        return result_df


if __name__ == '__main__':
    import sys
    import logging
    import datetime

    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    save_name = 'ifeng_bonus_report'

    f = 'ticker_list.py'
    ticker_file = open(f)
    ticker_info = ticker_file.read()
    ticker_file.close()
    ticker_list = map(lambda x: re.findall(r'\d+', x)[0], ticker_info.split('\n'))

    today_str = datetime.datetime.today().strftime('%Y%m%d')

    test = IfengFinanceDividendDownloader()

    result_df = test.download_dividend(ticker_list)
    result_df.to_pickle('{}_{}.p'.format(today_str, save_name))
    result_df.to_excel('{}_{}.xlsx'.format(today_str, save_name),
                       index=False)
