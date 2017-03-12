#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: race_info_downloader
# @Date: 2017-03-11
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import logging
import re

from bs4 import BeautifulSoup

import requests
from constants import Constant as const

logger = logging.getLogger(__name__)

columns = [const.DATE, const.INDEX, const.ID, const.SEASON_INDEX, const.NAME, const.CLASS, const.RATING_RANGE,
           const.RACING_COURSE, const.TRACK, const.COURSE, const.DISTANCE, const.GOING]

for i in range(1, 7):
    columns.append('{}{}'.format(const.TIME, i))

columns.append(const.POOL)


def download_race_info(race_date, race_index, race_course):
    result_dict = {}
    for key in columns:
        result_dict[key] = None

    result_dict[const.DATE] = race_date
    result_dict[const.INDEX] = race_index
    result_dict[const.RACING_COURSE] = 'Happy Valley' if race_course == 'HV' else 'Sha Tin'
    result_dict[const.ID] = '{}_{}'.format(race_date, race_index)

    try:
        url = 'http://racing.hkjc.com/racing/Info/meeting/Results/english/Local/{}/{}/{}'.format(race_date, race_course,
                                                                                                 race_index)
        logger.info('race date {}, race index {}, race course {}'.format(race_date, race_index, race_course))
        logger.info('access url is {}'.format(url))

        for i in range(4):
            r = requests.get(url, headers={'Referer': url,
                                           'Upgrade-Insecure-Requests': '1'})
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            divs = soup.find_all('div', {'class': 'rowDiv15'})
            find_div = False
            for div in divs:
                logger.debug(len(div.find_all('div')))
                if len(div.find_all('div')) == 3:
                    find_div = True
                    break
            else:
                logger.warn('Error in {}'.format(url))
                time.sleep(2)

            if find_div:
                break
        else:
            logger.warn('cannot find data')
            return None

        useful_info = div.find_all('div')

        season_index = re.findall(r'\d+', useful_info[0].text)
        if len(season_index) == 2:
            result_dict[const.SEASON_INDEX] = int(season_index[-1])
        else:
            logger.warn('Cannot find season index')

        race_info = useful_info[1].find_all('tr')

        # Class, distance and rating range and gong info
        class_dis_rating_going = race_info[0].find_all('td')
        class_dis_rating = class_dis_rating_going[0].text
        class_dis_rating_split = class_dis_rating.split('-')

        if class_dis_rating_split:
            result_dict[const.CLASS] = class_dis_rating_split[0].strip()
        else:
            logger.warn("Cannot find class info")

        if len(class_dis_rating_split) > 2:
            result_dict[const.RATING_RANGE] = '-'.join(class_dis_rating_split[2:]).strip().strip('(').strip(')')

        dis_info = re.findall(r'\d+M', class_dis_rating)
        if dis_info:
            result_dict[const.DISTANCE] = dis_info[0]
        else:
            logger.warn("Cannot find distance info")
        result_dict[const.GOING] = class_dis_rating_going[-1].text

        # Second row, name, course, track
        name_course_track = race_info[1].find_all('td')
        result_dict[const.NAME] = name_course_track[0].text
        track_course = name_course_track[-1].text.split('-')
        if len(track_course) == 2:
            result_dict[const.TRACK] = track_course[0].strip()
            result_dict[const.COURSE] = track_course[1].strip()
        if len(track_course) > 2:
            result_dict[const.TRACK] = track_course[0].strip()
            result_dict[const.COURSE] = '-'.join(track_course[1:])

        elif len(track_course) == 1:
            result_dict[const.COURSE] = track_course[0].strip()

        # find pool info
        result_dict[const.POOL] = race_info[2].find_all('td')[0].text

        # find all time section info
        time_sec = race_info[3].find_all('td')[2:]
        for i, time_td in enumerate(time_sec):
            try:
                result_dict['{}{}'.format(const.TIME, i + 1)] = float(time_td.text)
            except Exception:
                logger.warn('get time {} failed'.format(i + 1))
                result_dict['{}{}'.format(const.TIME, i + 1)] = time_td.text

    except Exception, err:
        logger.error('Cannot get info as {}'.format(err))
        return None

    else:
        return result_dict


if __name__ == '__main__':
    import os
    import sys
    import time
    import random
    import pickle
    import pprint

    import pandas as pd

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    if os.path.isfile('failed_info.txt'):
        os.remove('failed_info.txt')

    if os.uname()[1] == 'ewin3011':
        need_race_course = 'ST'
        data_file = open('/home/wangzg/Documents/WangYouan/Trading/HKHorse/data/all_course_info_list.p')
        data_list = pickle.load(data_file)
        save_path = '/home/wangzg/Documents/WangYouan/Trading/HKHorse/data/race_data'
        data_file.close()

    elif os.uname()[1] == 'ewin3102':
        need_race_course = 'HV'
        data_file = open('/home/zigan/Documents/WangYouan/trading/HKJCHorse/data/all_course_info_list.p')
        data_list = pickle.load(data_file)
        save_path = '/home/zigan/Documents/WangYouan/trading/HKJCHorse/data/race_data'
        data_file.close()
    else:
        # data_list = [('20161026', '8', 'HV')]
        # data_list = [(20090204, 1, 'HV'), (20090422, 8, 'HV'), (20100106, 3, 'HV'), (20101110, 2, 'HV'),
        #              (20101117, 4, 'HV'), (20110417, 3, 'HV'), (20110420, 7, 'HV'), (20110518, 2, 'HV'),
        #              (20110525, 7, 'HV'), (20110601, 3, 'HV'), (20110601, 7, 'HV'), (20110601, 8, 'HV'),
        #              (20110608, 4, 'HV'), (20140402, 9, 'HV'), (20141203, 2, 'HV'), (20141217, 8, 'HV'),
        #              (20150107, 3, 'HV'), (20150114, 6, 'HV'), (20160420, 6, 'HV'), (20161026, 8, 'HV')]

        data_list = [(20080427, 7, 'ST'), (20080512, 2, 'ST'), (20080525, 9, 'ST'), (20080608, 4, 'ST'),
                     (20091004, 10, 'ST'), (20091004, 2, 'ST'), (20091011, 10, 'ST'), (20100616, 5, 'ST'),
                     (20100627, 10, 'ST'), (20100701, 4, 'ST'), (20100704, 2, 'ST'), (20100711, 7, 'ST'),
                     (20100905, 5, 'ST'), (20100905, 4, 'ST'), (20100912, 6, 'ST'), (20100912, 10, 'ST'),
                     (20101010, 1, 'ST'), (20101010, 5, 'ST'), (20101010, 6, 'ST'), (20101010, 7, 'ST'),
                     (20110619, 4, 'ST'), (20110626, 2, 'ST'), (20110701, 5, 'ST'), (20110911, 7, 'ST'),
                     (20110918, 9, 'ST'), (20110918, 5, 'ST'), (20110918, 1, 'ST'), (20110925, 7, 'ST'),
                     (20110925, 6, 'ST'), (20111019, 7, 'ST'), (20111019, 8, 'ST'), (20111120, 3, 'ST'),
                     (20120125, 2, 'ST'), (20120205, 1, 'ST'), (20120211, 5, 'ST'), (20120211, 4, 'ST'),
                     (20120211, 3, 'ST'), (20120211, 2, 'ST'), (20120211, 1, 'ST'), (20120211, 10, 'ST'),
                     (20120211, 8, 'ST'), (20120211, 9, 'ST'), (20120211, 6, 'ST'), (20120211, 7, 'ST'),
                     (20120219, 10, 'ST'), (20120321, 5, 'ST'), (20120321, 8, 'ST'), (20120325, 1, 'ST'),
                     (20120325, 8, 'ST'), (20120401, 4, 'ST'), (20120401, 8, 'ST'), (20120401, 10, 'ST'),
                     (20120401, 2, 'ST'), (20120409, 10, 'ST'), (20120429, 1, 'ST'), (20120429, 2, 'ST'),
                     (20120506, 6, 'ST'), (20120516, 8, 'ST'), (20120519, 9, 'ST'), (20120519, 7, 'ST'),
                     (20120527, 10, 'ST'), (20120527, 2, 'ST'), (20131012, 8, 'ST'), (20131027, 6, 'ST'),
                     (20131027, 10, 'ST'), (20150712, 3, 'ST'), (20150913, 6, 'ST'), (20150919, 1, 'ST'),
                     (20160501, 5, 'ST'), (20160522, 3, 'ST'), (20160522, 9, 'ST'), (20160529, 10, 'ST'),
                     (20160612, 8, 'ST'), (20160701, 5, 'ST')]
        need_race_course = 'ST'
        save_path = '.'
    result_list = []

    # missing_list = [['20081019', '11', 'HV'],
    #                 ['20090225', '4', 'HV'],
    #                 ['20090311', '4', 'HV'],
    #                 ['20090422', '8', 'HV'],
    #                 ['20090923', '3', 'HV'],
    #                 ['20100106', '2', 'HV'],
    #                 ['20100106', '3', 'HV'],
    #                 ['20100106', '4', 'HV'],
    #                 ['20100106', '6', 'HV'],
    #                 ['20100113', '1', 'HV'],
    #                 ['20100113', '2', 'HV'],
    #                 ['20100113', '4', 'HV'],
    #                 ['20100113', '8', 'HV'],
    #                 ['20100120', '7', 'HV'],
    #                 ['20100609', '5', 'HV'],
    #                 ['20101031', '6', 'HV'],
    #                 ['20101110', '2', 'HV'],
    #                 ['20101110', '4', 'HV'],
    #                 ['20101110', '6', 'HV'],
    #                 ['20101117', '4', 'HV'],
    #                 ['20110105', '5', 'HV'],
    #                 ['20110706', '3', 'HV'],
    #                 ['20110706', '5', 'HV'],
    #                 ['20110706', '6', 'HV'],
    #                 ['20110921', '7', 'HV'],
    #                 ['20120215', '4', 'HV'],
    #                 ['20120502', '3', 'HV'],
    #                 ['20120502', '4', 'HV'],
    #                 ['20120502', '5', 'HV'],
    #                 ['20120509', '4', 'HV'],
    #                 ['20120509', '7', 'HV'],
    #                 ['20130227', '1', 'HV'],
    #                 ['20130227', '4', 'HV'],
    #                 ['20130306', '1', 'HV'],
    #                 ['20130306', '2', 'HV'],
    #                 ['20130306', '4', 'HV'],
    #                 ['20131218', '2', 'HV'],
    #                 ['20131226', '4', 'HV'],
    #                 ['20140402', '9', 'HV'],
    #                 ['20141019', '10', 'HV'],
    #                 ['20141019', '6', 'HV'],
    #                 ['20141022', '3', 'HV'],
    #                 ['20141022', '5', 'HV'],
    #                 ['20141022', '8', 'HV'],
    #                 ['20141029', '1', 'HV'],
    #                 ['20141029', '6', 'HV'],
    #                 ['20141126', '7', 'HV'],
    #                 ['20150128', '4', 'HV'],
    #                 ['20160203', '6', 'HV'],
    #                 ['20160302', '2', 'HV'],
    #                 ['20161026', '5', 'HV'],
    #                 ['20161026', '6', 'HV'],
    #                 ['20161026', '7', 'HV'],
    #                 ['20161026', '8', 'HV'],
    #                 ['20161030', '1', 'HV'],
    #                 ['20080209', '11', 'ST'],
    #                 ['20080309', '11', 'ST'],
    #                 ['20080330', '11', 'ST'],
    #                 ['20080412', '1', 'ST'],
    #                 ['20080412', '11', 'ST'],
    #                 ['20080412', '2', 'ST'],
    #                 ['20080427', '2', 'ST'],
    #                 ['20080427', '9', 'ST'],
    #                 ['20080501', '1', 'ST'],
    #                 ['20080501', '10', 'ST'],
    #                 ['20080501', '11', 'ST'],
    #                 ['20080501', '2', 'ST'],
    #                 ['20080501', '3', 'ST'],
    #                 ['20080501', '5', 'ST'],
    #                 ['20080501', '6', 'ST'],
    #                 ['20080501', '7', 'ST'],
    #                 ['20080501', '8', 'ST'],
    #                 ['20080504', '3', 'ST'],
    #                 ['20080504', '4', 'ST'],
    #                 ['20080512', '1', 'ST'],
    #                 ['20080512', '6', 'ST'],
    #                 ['20080512', '9', 'ST'],
    #                 ['20080518', '11', 'ST'],
    #                 ['20080518', '4', 'ST'],
    #                 ['20080525', '11', 'ST'],
    #                 ['20080601', '11', 'ST'],
    #                 ['20080615', '11', 'ST'],
    #                 ['20080628', '11', 'ST'],
    #                 ['20080701', '11', 'ST'],
    #                 ['20081012', '11', 'ST'],
    #                 ['20081026', '11', 'ST'],
    #                 ['20081116', '11', 'ST'],
    #                 ['20081123', '11', 'ST'],
    #                 ['20090101', '11', 'ST'],
    #                 ['20090128', '11', 'ST'],
    #                 ['20090208', '11', 'ST'],
    #                 ['20090215', '11', 'ST'],
    #                 ['20090301', '11', 'ST'],
    #                 ['20090315', '2', 'ST'],
    #                 ['20090315', '4', 'ST'],
    #                 ['20090322', '1', 'ST'],
    #                 ['20090322', '11', 'ST'],
    #                 ['20090322', '2', 'ST'],
    #                 ['20090322', '3', 'ST'],
    #                 ['20090322', '9', 'ST'],
    #                 ['20090328', '1', 'ST'],
    #                 ['20090328', '5', 'ST'],
    #                 ['20090328', '8', 'ST'],
    #                 ['20090328', '9', 'ST'],
    #                 ['20090405', '5', 'ST'],
    #                 ['20090413', '11', 'ST'],
    #                 ['20090501', '11', 'ST'],
    #                 ['20090517', '11', 'ST'],
    #                 ['20090531', '11', 'ST'],
    #                 ['20090628', '11', 'ST'],
    #                 ['20090701', '11', 'ST'],
    #                 ['20091017', '8', 'ST'],
    #                 ['20091115', '5', 'ST'],
    #                 ['20100101', '11', 'ST'],
    #                 ['20100216', '11', 'ST'],
    #                 ['20100221', '11', 'ST'],
    #                 ['20100501', '11', 'ST'],
    #                 ['20100508', '7', 'ST'],
    #                 ['20100516', '11', 'ST'],
    #                 ['20100523', '4', 'ST'],
    #                 ['20100530', '6', 'ST'],
    #                 ['20100606', '11', 'ST'],
    #                 ['20100606', '2', 'ST'],
    #                 ['20100606', '8', 'ST'],
    #                 ['20100612', '4', 'ST'],
    #                 ['20100612', '8', 'ST'],
    #                 ['20100616', '11', 'ST'],
    #                 ['20100616', '7', 'ST'],
    #                 ['20100627', '11', 'ST'],
    #                 ['20100704', '11', 'ST'],
    #                 ['20100711', '11', 'ST'],
    #                 ['20100905', '7', 'ST'],
    #                 ['20110101', '11', 'ST'],
    #                 ['20110205', '11', 'ST'],
    #                 ['20110205', '3', 'ST'],
    #                 ['20110212', '8', 'ST'],
    #                 ['20110323', '6', 'ST'],
    #                 ['20110323', '8', 'ST'],
    #                 ['20110327', '3', 'ST'],
    #                 ['20110327', '4', 'ST'],
    #                 ['20110327', '5', 'ST'],
    #                 ['20110327', '6', 'ST'],
    #                 ['20110403', '11', 'ST'],
    #                 ['20110403', '6', 'ST'],
    #                 ['20110409', '6', 'ST'],
    #                 ['20110425', '11', 'ST'],
    #                 ['20110510', '11', 'ST'],
    #                 ['20110529', '11', 'ST'],
    #                 ['20110619', '11', 'ST'],
    #                 ['20110701', '11', 'ST'],
    #                 ['20110710', '11', 'ST'],
    #                 ['20111009', '11', 'ST'],
    #                 ['20111030', '11', 'ST'],
    #                 ['20111113', '1', 'ST'],
    #                 ['20111127', '11', 'ST'],
    #                 ['20111217', '11', 'ST'],
    #                 ['20120101', '11', 'ST'],
    #                 ['20120115', '10', 'ST'],
    #                 ['20120115', '5', 'ST'],
    #                 ['20120115', '6', 'ST'],
    #                 ['20120115', '8', 'ST'],
    #                 ['20120115', '9', 'ST'],
    #                 ['20120121', '7', 'ST'],
    #                 ['20120121', '9', 'ST'],
    #                 ['20120125', '11', 'ST'],
    #                 ['20120409', '11', 'ST'],
    #                 ['20120506', '11', 'ST'],
    #                 ['20120527', '11', 'ST'],
    #                 ['20120603', '1', 'ST'],
    #                 ['20120617', '11', 'ST'],
    #                 ['20120701', '11', 'ST'],
    #                 ['20120708', '11', 'ST'],
    #                 ['20120715', '11', 'ST'],
    #                 ['20121028', '11', 'ST'],
    #                 ['20121028', '4', 'ST'],
    #                 ['20121104', '1', 'ST'],
    #                 ['20121104', '3', 'ST'],
    #                 ['20121104', '9', 'ST'],
    #                 ['20121110', '8', 'ST'],
    #                 ['20121118', '11', 'ST'],
    #                 ['20121202', '11', 'ST'],
    #                 ['20121216', '11', 'ST'],
    #                 ['20130101', '11', 'ST'],
    #                 ['20130212', '11', 'ST'],
    #                 ['20130407', '11', 'ST'],
    #                 ['20130501', '11', 'ST'],
    #                 ['20130608', '4', 'ST'],
    #                 ['20130612', '11', 'ST'],
    #                 ['20130623', '11', 'ST'],
    #                 ['20130623', '2', 'ST'],
    #                 ['20130623', '3', 'ST'],
    #                 ['20130623', '5', 'ST'],
    #                 ['20130623', '7', 'ST'],
    #                 ['20130623', '8', 'ST'],
    #                 ['20130623', '9', 'ST'],
    #                 ['20130701', '10', 'ST'],
    #                 ['20130701', '11', 'ST'],
    #                 ['20130701', '4', 'ST'],
    #                 ['20130701', '5', 'ST'],
    #                 ['20130701', '6', 'ST'],
    #                 ['20130707', '11', 'ST'],
    #                 ['20131001', '2', 'ST'],
    #                 ['20131001', '5', 'ST'],
    #                 ['20131001', '7', 'ST'],
    #                 ['20131006', '6', 'ST'],
    #                 ['20131012', '1', 'ST'],
    #                 ['20131012', '2', 'ST'],
    #                 ['20131103', '11', 'ST'],
    #                 ['20131117', '11', 'ST'],
    #                 ['20131201', '11', 'ST'],
    #                 ['20131229', '11', 'ST'],
    #                 ['20140101', '11', 'ST'],
    #                 ['20140202', '11', 'ST'],
    #                 ['20140323', '11', 'ST'],
    #                 ['20140413', '11', 'ST'],
    #                 ['20140413', '2', 'ST'],
    #                 ['20140413', '5', 'ST'],
    #                 ['20140421', '6', 'ST'],
    #                 ['20140421', '7', 'ST'],
    #                 ['20140427', '10', 'ST'],
    #                 ['20140427', '4', 'ST'],
    #                 ['20140427', '9', 'ST'],
    #                 ['20140504', '1', 'ST'],
    #                 ['20140504', '11', 'ST'],
    #                 ['20140504', '6', 'ST'],
    #                 ['20140510', '2', 'ST'],
    #                 ['20140517', '2', 'ST'],
    #                 ['20140517', '3', 'ST'],
    #                 ['20140517', '4', 'ST'],
    #                 ['20140517', '5', 'ST'],
    #                 ['20140517', '7', 'ST'],
    #                 ['20140525', '1', 'ST'],
    #                 ['20140525', '10', 'ST'],
    #                 ['20140525', '11', 'ST'],
    #                 ['20140525', '7', 'ST'],
    #                 ['20140525', '9', 'ST'],
    #                 ['20140601', '3', 'ST'],
    #                 ['20140601', '5', 'ST'],
    #                 ['20140601', '8', 'ST'],
    #                 ['20140608', '10', 'ST'],
    #                 ['20140608', '11', 'ST'],
    #                 ['20140615', '11', 'ST'],
    #                 ['20140615', '9', 'ST'],
    #                 ['20140701', '11', 'ST'],
    #                 ['20140706', '11', 'ST'],
    #                 ['20141008', '3', 'ST'],
    #                 ['20141026', '11', 'ST'],
    #                 ['20141123', '11', 'ST'],
    #                 ['20141207', '11', 'ST'],
    #                 ['20141228', '11', 'ST'],
    #                 ['20150101', '11', 'ST'],
    #                 ['20150221', '11', 'ST'],
    #                 ['20150308', '7', 'ST'],
    #                 ['20150308', '8', 'ST'],
    #                 ['20150315', '2', 'ST'],
    #                 ['20150315', '3', 'ST'],
    #                 ['20150321', '4', 'ST'],
    #                 ['20150412', '11', 'ST'],
    #                 ['20150503', '11', 'ST'],
    #                 ['20150509', '7', 'ST'],
    #                 ['20150524', '11', 'ST'],
    #                 ['20150531', '9', 'ST'],
    #                 ['20150614', '11', 'ST'],
    #                 ['20150701', '11', 'ST'],
    #                 ['20150705', '11', 'ST'],
    #                 ['20150712', '11', 'ST'],
    #                 ['20150906', '1', 'ST'],
    #                 ['20150928', '10', 'ST'],
    #                 ['20151018', '11', 'ST'],
    #                 ['20151108', '11', 'ST'],
    #                 ['20151206', '11', 'ST'],
    #                 ['20151227', '11', 'ST'],
    #                 ['20151227', '5', 'ST'],
    #                 ['20160101', '1', 'ST'],
    #                 ['20160101', '11', 'ST'],
    #                 ['20160101', '2', 'ST'],
    #                 ['20160124', '11', 'ST'],
    #                 ['20160131', '11', 'ST'],
    #                 ['20160210', '11', 'ST'],
    #                 ['20160306', '11', 'ST'],
    #                 ['20160328', '11', 'ST'],
    #                 ['20160410', '11', 'ST'],
    #                 ['20160501', '11', 'ST'],
    #                 ['20160522', '11', 'ST'],
    #                 ['20160612', '11', 'ST'],
    #                 ['20160619', '11', 'ST'],
    #                 ['20160701', '11', 'ST'],
    #                 ['20160710', '11', 'ST'],
    #                 ['20160911', '1', 'ST'],
    #                 ['20161001', '11', 'ST'],
    #                 ['20161008', '1', 'ST'],
    #                 ['20161008', '4', 'ST'],
    #                 ['20161008', '7', 'ST'],
    #                 ['20161008', '8', 'ST'],
    #                 ['20161016', '11', 'ST'],
    #                 ['20161016', '7', 'ST'],
    #                 ['20161016', '8', 'ST'],
    #                 ['20161023', '5', 'ST'],
    #                 ['20161023', '6', 'ST'],
    #                 ['20161106', '11', 'ST'],
    #                 ['20161127', '11', 'ST'],
    #                 ['20161227', '11', 'ST'],
    #                 ['20170101', '11', 'ST'],
    #                 ['20170130', '11', 'ST']]
    # for race_date, race_index, race_course in missing_list[-5:]:
    # for race_date, race_index, race_course in random.sample(missing_list, 5):
    failed_list = []
    for race_date, race_index, race_course in data_list:
        # for race_date, race_index, race_course in random.sample(data_list, 20):
        if race_course != need_race_course and need_race_course != None:
            continue

        test_dict = download_race_info(race_date, race_index, race_course)
        if test_dict is not None:
            result_list.append(test_dict)
        else:
            failed_list.append([race_date, race_index, race_course])
        time.sleep(1)

    df = pd.DataFrame(result_list, columns=columns)

    df.to_excel(os.path.join(save_path, '20170311_race_in_{}.xlsx'.format(need_race_course)), index=False)
    df.to_csv(os.path.join(save_path, '20170311_race_in_{}.csv'.format(need_race_course)), index=False)

    if failed_list:
        with open('failed_info.txt', 'w') as f:
            f.write(pprint.pformat(failed_list))
