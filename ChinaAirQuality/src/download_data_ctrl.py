#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: 1_download_data
# @Date: 2017-01-03
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os
import urllib
import time
import datetime

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from BeautifulSoup import BeautifulSoup

from constant import Constant


class AIRDailyDownload(Constant):
    def __init__(self):
        self.browser = None

    def start(self):
        if os.uname()[0] == 'Darwin':
            self.browser = webdriver.Chrome("/Users/warn/chromedriver")
        elif os.uname()[1] == 'warn-Inspiron-3437':
            self.browser = webdriver.Chrome("/home/warn/chromedriver")
        elif os.uname()[1] == 'ewin3011':
            self.browser = webdriver.Chrome("/home/wangzg/chromedriver")

        self.browser.implicitly_wait(60)

    def stop(self):
        if self.browser is not None:
            try:
                self.browser.close()
            except Exception, err:
                print ('Stop browser failed as {}'.format(err))
            finally:
                self.browser = None

    def _get_target_page(self, url, wait_time=10, retry_times=3, wait_report=False):
        for _ in range(retry_times):
            try:

                if wait_report:
                    self.wait_selenium(url, by=By.ID, element='report1', timeout=60)
                else:
                    self.browser.get(url)

            except TimeoutException, err:
                import traceback
                traceback.print_exc()
                self.stop()
                time.sleep(wait_time)
                self.start()

            else:
                break

    def get_page_info(self, page_num):
        query_dict = {self.PAGE: page_num,
                      self.START_DATE: self.start_date,
                      self.END_DATE: self.end_date,
                      self.CITY: self.city}
        target_url = '{}?{}'.format(self.URL, urllib.urlencode(query_dict))

        self._get_target_page(target_url)

        result_df = pd.DataFrame(columns=self.COLUMNS)

        soup = BeautifulSoup(self.browser.page_source)
        table = soup.find('table', {'id': 'report1'})
        rows = table.findAll('tr', {'height': '30'})[2:]

        for i, row in enumerate(rows):
            info_list = row.findAll('td')
            result_df.loc[i] = {self.CITY: info_list[1].text,
                                self.DATE: info_list[2].text,
                                self.AQI: info_list[3].text,
                                self.AIR_QUALITY_LEVEL: info_list[4].text,
                                self.PRIMARY_POLLUTANT: info_list[5].text}

        return result_df

    def get_period_data(self, start_date='2014-01-01', end_date='2016-12-31'):
        self.start_date = start_date
        self.end_date = end_date

        query_dict = {self.PAGE: 1,
                      self.START_DATE: self.start_date,
                      self.END_DATE: self.end_date,
                      self.CITY: self.city}

        target_url = '{}?{}'.format(self.URL, urllib.urlencode(query_dict))
        self._get_target_page(target_url)
        source = self.browser.page_source

        soup = BeautifulSoup(source)
        total_page_num = int(soup.findAll('tr', {'height': '25'})[0].findAll('td')[0].findAll('b')[1].text)

        result_df = pd.DataFrame()

        for i in range(1, total_page_num + 1):
            print datetime.datetime.today(), i
            result_df = pd.concat([result_df, self.get_page_info(i)], axis=0, ignore_index=True)
            time.sleep(5)

        return result_df

    def get_target_day_date(self, target_date):
        self.start_date = target_date
        self.end_date = target_date

        query_dict = {self.PAGE: 1,
                      self.START_DATE: self.start_date,
                      self.END_DATE: self.end_date,
                      self.CITY: self.city}

        target_url = '{}?{}'.format(self.URL, urllib.urlencode(query_dict))
        self._get_target_page(target_url)
        source = self.browser.page_source

        soup = BeautifulSoup(source)
        total_page_num = int(soup.findAll('tr', {'height': '25'})[0].findAll('td')[0].findAll('b')[1].text)

        result_df = pd.DataFrame()

        for i in range(1, total_page_num + 1):
            print datetime.datetime.today(), i
            result_df = pd.concat([result_df, self.get_page_info(i)], axis=0, ignore_index=True)
            time.sleep(3)

        return result_df

    def wait_selenium(self, url, by=By.XPATH, element=None, timeout=10):
        self.browser.get(url)
        try:
            element_present = EC.presence_of_element_located((by, element))
            WebDriverWait(self.browser, timeout).until(element_present)
        except TimeoutException:
            raise TimeoutException('Time out while wait for element presents')

        else:
            return self.browser.find_element(by=by, value=element)


if __name__ == '__main__':
    test = AIRDailyDownload()

    start_time = time.time()
    test.start()

    try:

        df = test.get_period_data(end_date='2014-01-01')

        print df

        df.to_csv('test.csv', encoding='cp936')

    except Exception, err:
        import traceback

        traceback.print_exc()

    finally:
        test.stop()

    print time.time() - start_time
