#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: download_data_urllib_ctrl
# @Date: 2017-01-03
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import time
import urllib
import urllib2
import datetime

from BeautifulSoup import BeautifulSoup
import pandas as pd

from constant import Constant


def get(url, data_list=None, max_try=3):
    if data_list:
        url = "{}?{}".format(url, urllib.urlencode(data_list))
    query = urllib2.Request(url)
    current_try = 0
    while current_try < max_try:
        try:
            response = urllib2.urlopen(query)
            html = response.read()
            response.close()
            return html
        except Exception, e:
            return None
    raise Exception("Cannot open page {}".format(url))


class AIRDailyDownloadUrllib(Constant):
    def __init__(self):
        self.browser = None

    def start(self):
        pass

    def stop(self):
        pass

    def get_target_day_date(self, target_date):
        self.start_date = target_date
        self.end_date = target_date

        query_dict = {self.PAGE: 1,
                      self.START_DATE: self.start_date,
                      self.END_DATE: self.end_date,
                      self.CITY: self.city}

        html = get(self.URL, query_dict)

        soup = BeautifulSoup(html)
        total_page_num = int(soup.findAll('tr', {'height': '25'})[0].findAll('td')[0].findAll('b')[1].text)

        result_df = pd.DataFrame()

        for i in range(1, total_page_num + 1):
            # print datetime.datetime.today(), i
            result_df = pd.concat([result_df, self.get_page_info(i)], axis=0, ignore_index=True)
            time.sleep(1)

        return result_df

    def get_page_info(self, page_num):
        query_dict = {self.PAGE: page_num,
                      self.START_DATE: self.start_date,
                      self.END_DATE: self.end_date,
                      self.CITY: self.city}

        html = get(self.URL, query_dict)

        df = pd.DataFrame(columns=self.COLUMNS)

        soup = BeautifulSoup(html)
        table = soup.find('table', {'id': 'report1'})
        rows = table.findAll('tr', {'height': '30'})[2:]

        for i, row in enumerate(rows):
            info_list = row.findAll('td')
            df.loc[i] = {self.CITY: info_list[1].text,
                         self.DATE: info_list[2].text,
                         self.AQI: info_list[3].text,
                         self.AIR_QUALITY_LEVEL: info_list[4].text,
                         self.PRIMARY_POLLUTANT: info_list[5].text}

        return df

if __name__ == '__main__':
    test = AIRDailyDownloadUrllib()

    df = test.get_target_day_date('2015-01-01')
    print df
    df.to_csv('../data/20150101.csv', encoding='utf8')
