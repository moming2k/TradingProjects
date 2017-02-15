#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: jockey_basic_downloader
# @Date: 2017-02-14
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import re
import time
import logging

import pandas as pd
import numpy as np
from BeautifulSoup import BeautifulSoup

from http_ctrl import HttpCtrl
from constants import Constant


class JockeyBasicDownloader(Constant):
    def __init__(self, logger=None):
        if logger is None:
            self.logger = logging.getLogger(self.__class__.__name__)
            self.ctrl = HttpCtrl()

        else:
            self.logger = logger.getLogger(self.__class__.__name__)
            self.ctrl = HttpCtrl(logger)

    def download_jockey_info(self):
        self.logger.info('Start to download all jockey info')

        # Download jockey name and id
        jockey_id_df = self.__get_all_jockey_info_list()

        # Download each jockey information
        jockey_info_df = self.__get_jockey_detail_info(jockey_id_df)
        result_df = pd.DataFrame(index=jockey_info_df.index)
        for key in jockey_info_df.keys():
            result_df['{}{}'.format(self.JOCKEY, key)] = jockey_info_df[key]

        self.logger.info('Download finished')

        return result_df

    def __get_all_jockey_info_list(self):

        self.logger.info('Start to get all jockey name list')
        previous_season_url = '{}/{}/Previous/Numbers/ALL/ALL'.format(self.JOCKEY_LIST_URL, self.CHINESE)
        current_season_url = '{}/{}/Current/Numbers/ALL/ALL'.format(self.JOCKEY_LIST_URL, self.CHINESE)
        df1 = self.__download_jockey_data_info(previous_season_url)
        df2 = self.__download_jockey_data_info(current_season_url)
        merged_df = pd.concat([df1, df2], axis=0, ignore_index=True).drop_duplicates(self.CODE)
        self.logger.info('Download jockey names finished')
        return merged_df

    def __download_jockey_data_info(self, url):

        html = self.ctrl.post(url)
        soup = BeautifulSoup(html)
        jockey_info_rows = soup.find('table', cellpadding='1px').findAll('tr')[2:]
        df = pd.DataFrame(columns=[self.CODE, self.NAME])
        for i, row in enumerate(jockey_info_rows):
            self.logger.debug('Row info {}'.format(row))
            require_info = row.find('a')

            if require_info is None:
                continue

            df.loc[i] = {self.CODE: require_info.get('href').split('&')[0].split('=')[-1],
                         self.NAME: require_info.text}

        return df

    def __get_jockey_detail_info(self, jockey_id_df):
        self.logger.info('Get details of every jockey info')

        # Generate columns information
        jockey_basic_columns = ['{}{}'.format(self.ENGLISH, self.NAME),
                                '{}{}'.format(self.CHINESE, self.NAME),
                                self.AGE,
                                self.BACKGROUND,
                                self.ACHIEVEMENTS,
                                self.NOTABLE_WINS,
                                self.HK_CAREER_WINS,
                                self.HK_CAREER_WINS_RATE,
                                self.IJC_RECORD,
                                ]

        jockey_season_columns = [self.NATIONALITY,
                                 self.STAKES,
                                 self.NUMBER_ONE,
                                 self.NUMBER_TWO,
                                 self.NUMBER_THREE,
                                 self.NUMBER_FOUR,
                                 self.NUMBER_STARTS]

        for i in [self.CURRENT_SEASON, self.LAST_SEASON]:
            for j in jockey_season_columns:
                jockey_basic_columns.append('{}{}'.format(i, j))

        empty_dict = {i: np.nan for i in jockey_basic_columns}

        self.logger.debug('Columns are {}'.format(jockey_basic_columns))
        result_df = pd.DataFrame(columns=jockey_basic_columns)

        for i in jockey_id_df.index:
            code = jockey_id_df.ix[i, self.CODE]
            chinese_name = jockey_id_df.ix[i, self.NAME]

            result_dict = empty_dict.copy()

            self.logger.debug('Start to query code {}'.format(code))
            current_info_dict = self.__decode_jockey_detail_page(self.CURRENT_SEASON, code)
            last_info_dict = self.__decode_jockey_detail_page(self.LAST_SEASON, code)

            result_dict.update(last_info_dict)
            result_dict.update(current_info_dict)
            result_dict['{}{}'.format(self.CHINESE, self.NAME)] = chinese_name

            self.logger.debug('last info dict: {}'.format(result_dict))

            result_df.loc[code] = result_dict

            time.sleep(3)

        return result_df

    def __decode_jockey_detail_page(self, season, code):
        self.logger.info('Start to get {} season jockey {} info'.format(season, code))

        season_dict = {self.LAST_SEASON: 'Previous',
                       self.CURRENT_SEASON: 'Current'}

        url = '{}/{}/{}'.format(self.HKJC_HOST_URL, self.ENGLISH, self.JOCKEY_DETAIL_LIST_URL)
        html = self.ctrl.get(url, [('JockeyCode', code), ('season', season_dict[season])])

        soup = BeautifulSoup(html)
        table = soup.find('table', width="435")
        if table is None:
            return {}

        info_list = table.findAll('tr')[1:]

        english_name = info_list[0].text
        result_dict = {'{}{}'.format(self.ENGLISH, self.NAME): english_name}

        def get_digit(s):
            return ''.join(re.findall(r'\d+', s))

        for info in info_list[1:]:
            info_text_list = info.text.split(':')
            self.logger.debug('info text list is {}'.format(info_text_list))

            if 'Background' in info_text_list[0]:
                result_dict[self.BACKGROUND] = info_text_list[1]

            elif 'Age' in info_text_list[0]:
                result_dict[self.AGE] = info_text_list[1]

            elif 'Notable' in info_text_list[0]:
                result_dict[self.NOTABLE_WINS] = info_text_list[1]

            elif 'IJC' in info_text_list[0]:
                result_dict[self.IJC_RECORD] = info_text_list[1]

            elif 'Achievements' in info_text_list[0]:
                result_dict[self.ACHIEVEMENTS] = info_text_list[1]

            elif 'Career' in info_text_list[0]:
                if len(info_text_list) == 3:
                    result_dict[self.HK_CAREER_WINS] = int(get_digit(info_text_list[1]))
                    result_dict[self.HK_CAREER_WINS_RATE] = float('.'.join(re.findall(r'\d+', info_text_list[2]))) / 100
                elif len(info_text_list) == 2:
                    digit = re.findall(r'\d+', info_text_list[1])
                    if len(digit) == 0:
                        continue
                    result_dict[self.HK_CAREER_WINS] = int(digit[0])
                    result_dict[self.HK_CAREER_WINS_RATE] = float('.'.join(digit[1:])) / 100
                else:
                    self.logger.error('Error info list {}'.format(info))
                    raise ValueError('Error info list {}'.format(info))

        info_tables = soup.findAll('table', width='800')

        for table in info_tables:
            if (season_dict[season] not in table.text
                and season_dict[self.CURRENT_SEASON if season == self.LAST_SEASON else self.LAST_SEASON] in table.text):
                break
        else:
            return result_dict

        info_list = table.findAll('tr')[2:-1]
        tmp_dict = {self.NATIONALITY: info_list[0].findAll('td')[1].text[2:],
                    self.NUMBER_ONE: int(get_digit(info_list[0].findAll('td')[3].text)),
                    self.NUMBER_STARTS: int(get_digit(info_list[0].findAll('td')[5].text)),
                    self.STAKES: int(get_digit(info_list[1].findAll('td')[1].text)),
                    self.NUMBER_TWO: int(get_digit(info_list[1].findAll('td')[3].text)),
                    self.NUMBER_THREE: int(get_digit(info_list[2].findAll('td')[3].text)),
                    self.NUMBER_FOUR: int(get_digit(info_list[3].findAll('td')[3].text)),
                    }

        for key in tmp_dict:
            result_dict['{}{}'.format(season, key)] = tmp_dict[key]

        return result_dict
