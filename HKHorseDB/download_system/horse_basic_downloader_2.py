#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: horse_basic_downloader_2
# @Date: 2017-03-06
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import re
import datetime

import pandas as pd
from bs4 import BeautifulSoup

import horse_basic_downloader


class HorseBasicDownloader(horse_basic_downloader.HorseBasicDownloader):
    def __get_all_horse_name(self):
        self.logger.info('Start to collect all horse name info')

        basic_url = 'http://{}/{}/{}'.format(self.HKJC_HOST_URL, self.CHINESE, self.HORSE_FORMER_NAME_PAGE)

        html = self.ctrl.get(basic_url)
        soup = BeautifulSoup(html, 'lxml')

        table = soup.find('table', attrs={'name': 'rsTable', 'id': 'rsTable'})
        rows = table.find_all('tr', attrs={'bgcolor': '#EEEEEE'})

        result_df = pd.DataFrame(columns=[self.CODE, self.BIRTHDAY, self.FORMER_NAME])

        for i, row in enumerate(rows):
            cols = row.find_all('td')
            code = re.findall(r'\((\w+)\)', cols[1].text)
            birthday = datetime.datetime.strptime(cols[-1].text, '%d/%m/%Y')
            former_name = cols[2].text.strip()
            result_df.loc[i] = {self.CODE: code,
                                self.BIRTHDAY: birthday,
                                self.FORMER_NAME: former_name}

        return result_df
