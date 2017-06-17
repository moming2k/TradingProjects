#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: race_basic_downloader
# @Date: 2017-03-09
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
from time import time, sleep
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

tmp_dict = {'Place': None,
            'HorseNo': None,
            'HorseName': None,
            'HorseCode': None,
            'JockeyName': None,
            'JockeyCode': None,
            'TrainerName': None,
            'TrianerCode': None,
            'ActualWt': None,
            'DeclarHorseWt': None,
            'Draw': None,
            'LBW': None,
            'FinishTime': None,
            'WinOdd': None,
            'SecTime1': None,
            'SecTime2': None,
            'SecTime3': None,
            'SecTime4': None,
            'SecTime5': None,
            'SecTime6': None,
            }

columns = ['Place', 'HorseNo', 'HorseName', 'HorseCode', 'JockeyName', 'JockeyCode', 'TrainerName', 'TrianerCode',
           'ActualWt', 'DeclarHorseWt', 'Draw', 'LBW', 'FinishTime', 'WinOdd', 'SecTime1', 'SecTime2', 'SecTime3',
           'SecTime4', 'SecTime5', 'SecTime6']


def convert_str_to_int(int_str):
    try:
        return int(int_str)
    except Exception as err:
        return int_str


def convert_str_to_float(int_str):
    try:
        return float(int_str)
    except Exception as err:
        return int_str


def convert_time_to_second(input_data):
    try:
        split_data = input_data.split('.')
        if len(split_data) == 2:
            return float(input_data)
        else:
            return int(split_data[0]) * 60 + float('.'.join(split_data[1:]))

    except Exception as err:
        return input_data

def process_get_race_date_id(date_str, race_id, driver, race_course='ST'):
    failed_info = ''

    if not os.path.isdir('var_{}'.format(race_course)):
        os.makedirs('var_{}'.format(race_course))

    filename = 'var_{}/{}_{}.xlsx'.format(race_course, date_str, race_id)
    url = 'http://racing.hkjc.com/racing/Info/meeting/Results/english/Local/{}/{}/{}'.format(date_str,
                                                                                             race_course,
                                                                                             race_id)

    if os.path.isfile(filename):
        return failed_info
    driver.get(url)
    sleep(4)
    result_df = pd.DataFrame(columns=columns)
    start_time = time()
    while start_time - time() < 30:
        try:
            driver.find_element_by_class_name('contentR1')
        except NoSuchElementException:
            break
        else:
            sleep(1)

    try:
        table = driver.find_elements_by_class_name('tableBorder')[0]

        data = table.find_elements_by_tag_name('tr')
        '''print(len(data))'''
        for index in range(1, len(data)):
            tmp_result = tmp_dict.copy()
            detail = data[index].find_elements_by_tag_name('td')
            if (len(detail) > 10):
                try:
                    tmp_result['Place'] = convert_str_to_int(detail[0].text)
                except IndexError:
                    print('Can not find place')

                try:
                    tmp_result['HorseNo'] = convert_str_to_int(detail[1].text)
                except IndexError:
                    # print('')
                    print('Can not find horseNo')

                try:
                    Horsename = detail[2].text
                    if '(' in Horsename:
                        horsecode = Horsename.split('(')[1].split(')')[0]
                        tmp_result['HorseName'] = Horsename.split('(')[0]
                        tmp_result['HorseCode'] = horsecode
                    else:
                        tmp_result['HorseName'] = Horsename
                except IndexError:
                    print('Can not find Horsename')

                try:
                    JockeyCode = detail[3].text
                    tmp_result['JockeyName'] = JockeyCode
                    link = detail[3].find_element_by_tag_name('a')
                    if link:
                        link = link.get_attribute('href').split('=')[1].split('&')[0]
                        tmp_result['JockeyCode'] = link
                except NoSuchElementException:
                    pass
                except Exception:
                    print('Can not find JockeyCode')

                try:
                    TrainerCode = detail[4].text
                    tmp_result['TrainerName'] = TrainerCode
                    link2 = detail[4].find_element_by_tag_name('a')
                    if link2:
                        link2 = link2.get_attribute('href').split('=')[1].split('&')[0]
                        tmp_result['TrianerCode'] = link2
                except NoSuchElementException:
                    pass
                except Exception:
                    print('Can not find TrainerCode')

                try:
                    tmp_result['ActualWt'] = convert_str_to_int(detail[5].text)
                except IndexError:
                    print('Can not find actualweight')

                try:
                    tmp_result['DeclarHorseWt'] = convert_str_to_int(detail[6].text)

                except IndexError:
                    print('Can not find declareweight')

                try:
                    tmp_result['Draw'] = convert_str_to_int(detail[7].text)
                except IndexError:
                    print('Can not find draw')

                try:
                    tmp_result['LBW'] = detail[8].text
                except IndexError:
                    print('Can not find LBW')

                try:
                    tmp_result['FinishTime'] = convert_time_to_second(detail[-2].text)
                except IndexError:
                    print('Can not find finishtime')

                try:
                    tmp_result['WinOdd'] = convert_str_to_float(detail[-1].text)
                except IndexError:
                    print('Can not find winOdd')

                result_df.loc[index] = tmp_result

        try:
            temp = driver.find_element_by_class_name('rowDivRight')
            temp2 = temp.find_element_by_tag_name('a').get_attribute('href')
            driver.get(temp2)
            sleep(4)
            tbody = driver.find_elements_by_tag_name('tbody')[10]
            line = tbody.find_elements_by_tag_name('tr')
            '''print(len(line))'''
            timelist = []
            for li in line:
                if (li.text.count('.') >= 3):
                    if ('Sec' not in li.text):
                        timelist.append(li.text)

            result_index = 0
            for time_info in timelist:
                current_index = result_df.index[result_index]
                dot_count = time_info.count('.')
                time_slot = time_info.split('  ')

                for i in range(dot_count):
                    result_df.loc[current_index, 'SecTime{}'.format(i + 1)] = convert_str_to_float(time_slot[i])

                result_index = result_index + 1
        except NoSuchElementException:
            failed_info = '{} {}_{}_NoSuchElement'.format(failed_info, date_str, race_id)
        except IndexError:
            failed_info = '{} {}_{}_IndexError'.format(failed_info, date_str, race_id)

    except Exception as err:
        failed_info = '{} {}: test_failed as {}'.format(failed_info, datetime.today().strftime('%Y-%m-%d'), err)

    finally:

        if result_df.empty:
            failed_info = '{} has no result.{}'.format(filename, failed_info)
        else:
            result_df.to_excel(filename, index=False)

        if failed_info:
            failed_info = '{}: {}\n'.format(datetime.today(), failed_info)
        return failed_info


if __name__ == '__main__':
    import re
    # from xvfbwrapper import Xvfb

    # vdisplay = Xvfb(width=1366, height=768)
    # vdisplay.start()

    driver = webdriver.Chrome('/Users/moming2k/chromedriver')
    # driver = webdriver.Chrome('/home/zigan/chromedriver')
    # driver = webdriver.Chrome('/home/wangzg/chromedriver')

    # hv_dict = {'20081217': [3]}
    #
    # st_dict = {'20101106': [2]}
    #
    # for key in st_dict:
    #     for race_id in st_dict[key]:
    #         wrong_info = process_get_race_date_id(key, race_id, driver, 'ST')
    #         if len(wrong_info) > 1:
    #             print wrong_info
    #         sleep(3)

    # for key in hv_dict:
    #     for race_id in hv_dict[key]:
    #         wrong_info = process_get_race_date_id(key, race_id, driver, 'HV')
    #         if len(wrong_info) > 1:
    #             print wrong_info
    #         sleep(3)

    # st_info = [('20080406', '2'),
    #            ('20080412', '3'),
    #            ('20080412', '11'),
    #            ('20080112', '3'),
    #            ('20080112', '10'),
    #            ('20080106', '1'),
    #            ('20080106', '2'),
    #            ('20080106', '3'),
    #            ('20080106', '4'),
    #            ('20080106', '5'),
    #            ('20080106', '6'),
    #            ('20080501', '11'),
    #            ('20080127', '1'),
    #            ('20080127', '2'),
    #            ('20080127', '3'),
    #            ('20080127', '4'),
    #            ('20080127', '5'),
    #            ('20080316', '4')
    #            ]

    # for race_date, race_id in st_info:
    #     wrong_info = process_get_race_date_id(race_date, int(race_id), driver, 'ST')
    #     if wrong_info:
    #         print wrong_info

    # hv_info = [('20080309', '11'),
    #            ('20080409', '2'),
    #            ('20080130', '3'),
    #            ('20080123', '3'),
    #            ('20080123', '7')]

    # for race_date, race_id in hv_info:
    #     wrong_info = process_get_race_date_id(race_date, int(race_id), driver, 'HV')
    #     if wrong_info:
    #         print wrong_info

    # miss_info = ["('20080109', 1, HV) seq error", "('20080109', 2, HV) seq error", "('20080109', 4, HV) seq error",
    #              "('20080109', 5, HV) seq error", "('20080109', 6, HV) seq error", "('20080109', 7, HV) seq error",
    #              "('20080109', 8, HV) seq error", "('20080123', 1, HV) seq error", "('20080123', 2, HV) seq error",
    #              "('20080123', 3, HV) seq error", "('20080123', 4, HV) seq error", "('20080123', 5, HV) seq error",
    #              "('20080123', 6, HV) seq error", "('20080123', 7, HV) seq error", "('20080123', 8, HV) seq error",
    #              "('20080130', 1, HV) seq error", "('20080130', 2, HV) seq error", "('20080130', 3, HV) seq error",
    #              "('20080130', 4, HV) seq error", "('20080130', 5, HV) seq error", "('20080130', 8, HV) seq error",
    #              "('20080213', 1, HV) seq error", "('20080213', 2, HV) seq error", "('20080213', 3, HV) seq error",
    #              "('20080213', 4, HV) seq error", "('20080213', 5, HV) seq error", "('20080213', 6, HV) seq error",
    #              "('20080213', 7, HV) seq error", "('20080213', 8, HV) seq error", "('20080220', 1, HV) seq error",
    #              "('20080220', 2, HV) seq error", "('20080220', 4, HV) seq error", "('20080220', 5, HV) seq error",
    #              "('20080220', 6, HV) seq error", "('20080220', 7, HV) seq error", "('20080220', 8, HV) seq error",
    #              "('20080227', 1, HV) seq error", "('20080227', 2, HV) seq error", "('20080227', 3, HV) seq error",
    #              "('20080227', 4, HV) seq error", "('20080227', 5, HV) seq error", "('20080227', 6, HV) seq error",
    #              "('20080227', 8, HV) seq error", "('20080305', 1, HV) seq error", "('20080305', 2, HV) seq error",
    #              "('20080305', 3, HV) seq error", "('20080305', 4, HV) seq error", "('20080305', 6, HV) seq error",
    #              "('20080305', 7, HV) seq error", "('20080305', 8, HV) seq error", "('20080319', 2, HV) seq error",
    #              "('20080319', 3, HV) seq error", "('20080319', 4, HV) seq error", "('20080319', 5, HV) seq error",
    #              "('20080319', 6, HV) seq error", "('20080319', 7, HV) seq error", "('20080319', 8, HV) seq error",
    #              "('20080409', 1, HV) seq error", "('20080409', 2, HV) seq error", "('20080409', 3, HV) seq error",
    #              "('20080409', 5, HV) seq error", "('20080409', 7, HV) seq error", "('20080423', 1, HV) seq error",
    #              "('20080423', 2, HV) seq error", "('20080423', 3, HV) seq error", "('20080423', 4, HV) seq error",
    #              "('20080423', 5, HV) seq error", "('20080423', 6, HV) seq error", "('20080423', 7, HV) seq error",
    #              "('20080423', 8, HV) seq error", "('20080507', 1, HV) seq error", "('20080507', 2, HV) seq error",
    #              "('20080507', 3, HV) seq error", "('20080507', 4, HV) seq error", "('20080507', 5, HV) seq error",
    #              "('20080507', 6, HV) seq error", "('20081210', 8, HV) seq error", "('20090218', 6, HV) seq error",
    #              "('20090225', 5, HV) seq error", "('20100923', 6, HV) seq error", "('20120415', 6, HV) seq error",
    #              "('20130227', 6, HV) seq error", "('20130605', 6, HV) seq error", "('20131120', 1, HV) seq error",
    #              "('20160203', 1, HV) seq error", "('20080106', 1, ST) seq error", "('20080106', 2, ST) seq error",
    #              "('20080106', 3, ST) seq error", "('20080106', 4, ST) seq error", "('20080106', 5, ST) seq error",
    #              "('20080106', 6, ST) seq error", "('20080106', 7, ST) seq error", "('20080106', 8, ST) seq error",
    #              "('20080106', 9, ST) seq error", "('20080112', 1, ST) seq error", "('20080112', 10, ST) seq error",
    #              "('20080112', 2, ST) seq error", "('20080112', 3, ST) seq error", "('20080112', 4, ST) seq error",
    #              "('20080112', 5, ST) seq error", "('20080112', 7, ST) seq error", "('20080112', 8, ST) seq error",
    #              "('20080120', 1, ST) seq error", "('20080120', 10, ST) seq error", "('20080120', 2, ST) seq error",
    #              "('20080120', 3, ST) seq error", "('20080120', 5, ST) seq error", "('20080120', 6, ST) seq error",
    #              "('20080120', 8, ST) seq error", "('20080120', 9, ST) seq error", "('20080127', 1, ST) seq error",
    #              "('20080127', 10, ST) seq error", "('20080127', 2, ST) seq error", "('20080127', 3, ST) seq error",
    #              "('20080127', 4, ST) seq error", "('20080127', 7, ST) seq error", "('20080127', 8, ST) seq error",
    #              "('20080127', 9, ST) seq error", "('20080202', 1, ST) seq error", "('20080202', 10, ST) seq error",
    #              "('20080202', 2, ST) seq error", "('20080202', 3, ST) seq error", "('20080202', 4, ST) seq error",
    #              "('20080202', 5, ST) seq error", "('20080202', 6, ST) seq error", "('20080202', 7, ST) seq error",
    #              "('20080202', 9, ST) seq error", "('20080209', 1, ST) seq error", "('20080209', 10, ST) seq error",
    #              "('20080209', 11, ST) seq error", "('20080209', 2, ST) seq error", "('20080209', 4, ST) seq error",
    #              "('20080209', 5, ST) seq error", "('20080209', 6, ST) seq error", "('20080209', 8, ST) seq error",
    #              "('20080209', 9, ST) seq error", "('20080217', 1, ST) seq error", "('20080217', 10, ST) seq error",
    #              "('20080217', 2, ST) seq error", "('20080217', 3, ST) seq error", "('20080217', 4, ST) seq error",
    #              "('20080217', 5, ST) seq error", "('20080217', 6, ST) seq error", "('20080217', 7, ST) seq error",
    #              "('20080217', 8, ST) seq error", "('20080224', 1, ST) seq error", "('20080224', 10, ST) seq error",
    #              "('20080224', 2, ST) seq error", "('20080224', 4, ST) seq error", "('20080224', 5, ST) seq error",
    #              "('20080224', 6, ST) seq error", "('20080224', 8, ST) seq error", "('20080224', 9, ST) seq error",
    #              "('20080301', 10, ST) seq error", "('20080301', 3, ST) seq error", "('20080301', 4, ST) seq error",
    #              "('20080301', 5, ST) seq error", "('20080301', 6, ST) seq error", "('20080301', 7, ST) seq error",
    #              "('20080301', 9, ST) seq error", "('20080309', 10, ST) seq error", "('20080309', 11, ST) seq error",
    #              "('20080309', 2, ST) seq error", "('20080309', 3, ST) seq error", "('20080309', 4, ST) seq error",
    #              "('20080309', 5, ST) seq error", "('20080309', 6, ST) seq error", "('20080309', 7, ST) seq error",
    #              "('20080312', 1, ST) seq error", "('20080312', 2, ST) seq error", "('20080312', 3, ST) seq error",
    #              "('20080312', 4, ST) seq error", "('20080312', 5, ST) seq error", "('20080312', 7, ST) seq error",
    #              "('20080312', 8, ST) seq error", "('20080316', 1, ST) seq error", "('20080316', 10, ST) seq error",
    #              "('20080316', 2, ST) seq error", "('20080316', 3, ST) seq error", "('20080316', 4, ST) seq error",
    #              "('20080316', 5, ST) seq error", "('20080316', 6, ST) seq error", "('20080316', 7, ST) seq error",
    #              "('20080316', 9, ST) seq error", "('20080324', 1, ST) seq error", "('20080324', 10, ST) seq error",
    #              "('20080324', 2, ST) seq error", "('20080324', 3, ST) seq error", "('20080324', 4, ST) seq error",
    #              "('20080324', 6, ST) seq error", "('20080324', 7, ST) seq error", "('20080324', 8, ST) seq error",
    #              "('20080324', 9, ST) seq error", "('20080330', 10, ST) seq error", "('20080330', 11, ST) seq error",
    #              "('20080330', 2, ST) seq error", "('20080330', 3, ST) seq error", "('20080330', 4, ST) seq error",
    #              "('20080330', 5, ST) seq error", "('20080330', 6, ST) seq error", "('20080330', 7, ST) seq error",
    #              "('20080330', 8, ST) seq error", "('20080330', 9, ST) seq error", "('20080406', 1, ST) seq error",
    #              "('20080406', 10, ST) seq error", "('20080406', 2, ST) seq error", "('20080406', 3, ST) seq error",
    #              "('20080406', 4, ST) seq error", "('20080406', 5, ST) seq error", "('20080406', 6, ST) seq error",
    #              "('20080406', 9, ST) seq error", "('20080412', 11, ST) seq error", "('20080412', 2, ST) seq error",
    #              "('20080412', 4, ST) seq error", "('20080412', 5, ST) seq error", "('20080412', 6, ST) seq error",
    #              "('20080412', 7, ST) seq error", "('20080412', 8, ST) seq error", "('20080412', 9, ST) seq error",
    #              "('20080427', 1, ST) seq error", "('20080427', 10, ST) seq error", "('20080427', 2, ST) seq error",
    #              "('20080427', 3, ST) seq error", "('20080427', 4, ST) seq error", "('20080427', 5, ST) seq error",
    #              "('20080427', 6, ST) seq error", "('20080501', 10, ST) seq error", "('20080501', 11, ST) seq error",
    #              "('20080501', 3, ST) seq error", "('20080501', 4, ST) seq error", "('20080501', 5, ST) seq error",
    #              "('20080501', 7, ST) seq error", "('20080501', 8, ST) seq error", "('20080501', 9, ST) seq error",
    #              "('20080504', 1, ST) seq error", "('20080504', 10, ST) seq error", "('20080504', 2, ST) seq error",
    #              "('20080504', 3, ST) seq error", "('20080504', 4, ST) seq error", "('20080504', 5, ST) seq error",
    #              "('20080504', 6, ST) seq error", "('20080504', 8, ST) seq error", "('20080504', 9, ST) seq error",
    #              "('20080615', 8, ST) seq error", "('20081026', 4, ST) seq error", "('20081220', 4, ST) seq error",
    #              "('20090509', 3, ST) seq error", "('20090920', 3, ST) seq error", "('20110130', 10, ST) seq error",
    #              "('20120211', 10, ST) seq error", "('20130420', 9, ST) seq error", "('20130602', 4, ST) seq error",
    #              "('20130602', 6, ST) seq error", "('20140330', 7, ST) seq error", "('20141012', 9, ST) seq error",
    #              "('20150315', 10, ST) seq error", "('20150412', 6, ST) seq error", "('20161102', 6, ST) seq error"]

    miss_info = ['20130206_5 HV',
                 '20130206_4 HV',
                 '20130206_7 HV',
                 '20130206_6 HV',
                 '20130206_1 HV',
                 '20130206_3 HV',
                 '20130206_2 HV',
                 '20130206_8 HV']

    wrong_log = open('wrong_logs.txt', 'w')
    for info in miss_info:
        usefully_parameters = re.findall(r'\d+', info)
        if 'ST' in info:
            rc = 'ST'
        else:
            rc = 'HV'
        wrong_info = process_get_race_date_id(usefully_parameters[0], int(usefully_parameters[1]), driver, rc)
        if len(wrong_info) > 1:
            wrong_log.write(wrong_info)
            print(wrong_info)
        sleep(1)

    wrong_log.close()
    driver.close()
    # vdisplay.stop()
