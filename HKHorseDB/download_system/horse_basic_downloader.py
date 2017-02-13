#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: horse_basic_downloader
# @Date: 2017-02-13
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import time
import logging
from HTMLParser import HTMLParser

import pandas as pd
from BeautifulSoup import BeautifulSoup

from http_ctrl import HttpCtrl
from constants import Constant


class HorseBasicDownloader(Constant):
    def __init__(self, logger=None):
        if logger is None:
            self.logger = logging.getLogger(self.__class__.__name__)
            self.ctrl = HttpCtrl()

        else:
            self.logger = logger.getLogger(self.__class__.__name__)
            self.ctrl = HttpCtrl(logger)

    def download_horse_info(self):
        self.logger.info('Start to download all horse info')

        # Download horse name and id
        horse_id = self.__get_all_horse_name()

        # Download each horse information
        return self.__get_horse_detail_info(horse_id)

    def __get_all_horse_name(self):
        self.logger.info('Start to collect all horse name info')
        horse_info_list = []

        basic_url = 'http://{}/{}/{}'.format(self.HKJC_HOST_URL, self.ENGLISH, self.HORSE_LIST_PAGE)

        for i in range(26):
            current_char = chr(i + 65)
            current_url = '{}?ordertype={}'.format(basic_url, current_char)
            self.logger.debug('Get page {} info'.format(current_char))
            page_html = self.ctrl.get(current_url, headers={'Referer': current_url})
            horse_info_list.append(self.__decode_horse_list_page(page_html=page_html))
            time.sleep(3)

        self.logger.info('Collect horse name finished')
        return pd.concat(horse_info_list, axis=0, ignore_index=True)

    def __decode_horse_list_page(self, page_html):
        self.logger.debug('Start to decode page info')
        soup = BeautifulSoup(page_html)

        all_tables = soup.findAll('table')

        def is_horse_info_page(tb):
            a_list = tb.findAll('a')
            return len(a_list) == 1 and a_list[0].get('href').startswith('horse.asp')

        horse_info = pd.DataFrame(columns=[self.NAME, self.CODE])

        index = 0
        for table in all_tables:
            self.logger.debug('Table content: {}'.format(table))
            if not is_horse_info_page(table):
                continue
            # print table
            horse_code = table.findAll('a')[0].get('href').split('=')[-1]
            horse_name = table.findAll('a')[0].text
            horse_info.loc[index] = {self.NAME: horse_name,
                                     self.CODE: horse_code}
            index += 1

        return horse_info

    def __get_horse_detail_info(self, horse_id_df):
        columns = [self.SIRE, '{}{}'.format(self.TRAINER, self.CODE), self.ORIGIN, self.AGE, self.SEX, self.COLOR,
                   self.SEASON_STAKE, self.TOTAL_STAKE, self.NUMBER_ONE, self.NUMBER_STARTS, self.NUMBER_THREE,
                   self.NUMBER_TWO, '{}{}'.format(self.ENGLISH, self.OWNER), '{}{}'.format(self.CHINESE, self.OWNER),
                   '{}{}'.format(self.ENGLISH, self.NAME), '{}{}'.format(self.CHINESE, self.NAME),
                   self.CURRENT_RATING, self.SEASON_START_RATING, self.DAM, self.DAM_SIRE, self.IMPORT_TYPE]

        # horse_columns = map(lambda x: '{}{}'.format(self.HORSE, x), columns)
        # self.logger.debug('Columns: {}'.format(columns))
        horse_info_df = pd.DataFrame(columns=columns)
        self.logger.info('Start to query detail info of horse')

        for index in horse_id_df.index:
            horse_code = horse_id_df.ix[index, self.CODE]
            self.logger.debug('Horse code is {}'.format(horse_code))
            chinese_info = self.__get_horse_chinese_info(horse_code)

            english_info = self.__get_horse_english_info(horse_code)

            chinese_info.update(english_info)
            chinese_info['{}{}'.format(self.ENGLISH, self.NAME)] = horse_id_df.ix[index, self.NAME]
            # self.logger.debug('Saved data info: {}'.format(chinese_info))
            horse_info_df.loc[horse_code] = chinese_info
            time.sleep(3)

        self.logger.info('Query detail info of horse finished')
        result_df = pd.DataFrame(index=horse_info_df.index)
        for column in horse_info_df.keys():
            result_df['{}{}'.format(self.HORSE, column)] = horse_info_df[column]

        return result_df

    def __get_horse_chinese_info(self, horse_code):
        self.logger.info('Get Chinese detail of horse code {}'.format(horse_code))
        query_url = '{}/{}/{}/{}'.format(self.HKJC_RACING_URL, self.HORSE_DETAIL_PAGE, self.CHINESE, horse_code)
        page_info = self.ctrl.get(query_url)
        soup = BeautifulSoup(page_info)
        name = soup.title.text.split(' - ')[0]
        owner_name = soup.findAll('table')[2].findAll('tr')[1].findAll('a')[0].text
        return {'{}{}'.format(self.CHINESE, self.NAME): name,
                '{}{}'.format(self.CHINESE, self.OWNER): owner_name}

    def __get_horse_english_info(self, horse_code):
        self.logger.info('Get English detail of horse code {}'.format(horse_code))
        query_url = '{}/{}/{}/{}'.format(self.HKJC_RACING_URL, self.HORSE_DETAIL_PAGE, self.ENGLISH, horse_code)
        page_info = self.ctrl.get(query_url)

        soup = BeautifulSoup(page_info)
        h = HTMLParser()

        table1 = soup.findAll('table')[1]
        table2 = soup.findAll('table')[2]

        result_dict = {
            '{}{}'.format(self.ENGLISH, self.OWNER): table2.findAll('tr')[1].findAll('a')[0].text,
            self.IMPORT_TYPE: table1.findAll('tr')[2].find('td').text,
            self.SEASON_STAKE: table1.findAll('tr')[3].find('td').text,
            self.TOTAL_STAKE: table1.findAll('tr')[4].find('td').text,
            '{}{}'.format(self.TRAINER, self.CODE): table2.findAll('tr')[0].find('a').get('href').split('=')[-1],
            self.CURRENT_RATING: table2.findAll('tr')[2].find('td').text,
            self.SEASON_START_RATING: table2.findAll('tr')[3].find('td').text,
            self.SIRE: table2.findAll('tr')[4].find('td').text,
            self.DAM: table2.findAll('tr')[5].find('td').text,
            self.DAM_SIRE: table2.findAll('tr')[6].find('td').text,
        }

        country_age = h.unescape(table1.findAll('tr')[0].find('td').text).split('/')
        result_dict[self.ORIGIN] = country_age[0].replace(u'\xa0', u'')
        result_dict[self.AGE] = country_age[1].replace(u'\xa0', u'')

        color_sex = h.unescape(table1.findAll('tr')[1].find('td').text).split('/')
        result_dict[self.COLOR] = color_sex[0].replace(u'\xa0', u'')
        result_dict[self.SEX] = color_sex[1].replace(u'\xa0', u'')

        racing_info = table1.findAll('tr')[5].find('td').text.split('-')
        result_dict[self.NUMBER_THREE] = racing_info[2]
        result_dict[self.NUMBER_TWO] = racing_info[1]
        result_dict[self.NUMBER_ONE] = racing_info[0]
        result_dict[self.NUMBER_STARTS] = racing_info[3]

        return result_dict


if __name__ == '__main__':
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    test = HorseBasicDownloader()

    horse_basic_info = test.download_horse_info()
    horse_basic_info.to_pickle('horse_info.p')
    horse_basic_info.to_excel('horse_info.xlsx')
