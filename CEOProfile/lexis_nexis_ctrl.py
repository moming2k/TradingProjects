#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: lexis_nexis_ctrl
# Author: Mark Wang
# Date: 4/8/2016

import os
import logging
import time
import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from constants import Constants


class LexisNexisCtrl(Constants):
    def __init__(self, username, password, logger=None):
        self._username = username
        self._password = password
        self._br = None
        self._window_id_dict = {'start_window': None,
                                'sign_in_window': None}

        if logger is None:
            self.logger = logging.getLogger(self.__class__.__name__)
        else:
            self.logger = logger.getLogger(self.__class__.__name__)

        self._cannot_handle_info = []

    def start(self):
        if self._br is not None:
            self.logger.debug("An br exists stop it first")
            self.stop()
        self.logger.debug("Start selenium browser")
        if os.uname()[0] == 'Darwin':
            self._br = webdriver.Chrome("/Users/warn/chromedriver")
        elif os.uname()[1] == 'warn-Inspiron-3437':
            self._br = webdriver.Chrome("/home/warn/chromedriver")
        elif os.uname()[1] == 'ewin3011':
            self._br = webdriver.Chrome("/home/wangzg/chromedriver")

        self._br.implicitly_wait(30)
        self._login()
        self.logger.info("Start browser successfully.")

    def stop(self):
        if self._br is not None:
            self.logger.debug("Stop selenium browser")
            try:
                self._br.quit()
            except Exception, err:
                self.logger.warn('Cannot stop browser, as {}'.format(err))
            finally:
                self._br = None

    def _login(self):
        self._open_url(self.START_URL, wait_element='/html/body/section[2]/div/div/div/div[1]/div/p[1]/a[1]',
                       wait_method=By.XPATH)
        self._window_id_dict['start_window'] = self._br.current_window_handle
        self._br.find_element_by_xpath("/html/body/section[2]/div/div/div/div[1]/div/p[1]/a[1]").click()
        time.sleep(5)
        for window_id in self._br.window_handles:
            if window_id != self._window_id_dict['start_window']:
                self._window_id_dict['sign_in_window'] = window_id
                break
        self._br.switch_to_window(self._window_id_dict['sign_in_window'])
        self._br.find_element_by_id('userid').send_keys(self._username)
        self._br.find_element_by_id('password').send_keys(self._password)
        self._br.find_element_by_id('signInSbmtBtn').click()
        while not self.wait_element(by=By.XPATH, element='//*[@id="mainSearch"]'):
            self.logger.warn('page not load well, pleas wait')
            time.sleep(5)

    def _open_url(self, url, wait_element=None, wait_method=By.XPATH, max_try=3, timeout=30):
        for try_time in range(max_try):
            try:
                self.logger.debug("Start to get url {}".format(url))
                self._br.get(url)
                if wait_element is not None:
                    if not self.wait_element(wait_method, wait_element, timeout):
                        raise Exception('Element {} by {} not found.'.format(wait_element, wait_method))
                return
            except Exception, err:
                self.logger.warn("Open target url failed as {}".format(err))
                time.sleep(10)
                self.start()
        else:
            raise TimeoutException("Can not open url {}".format(url))

    def wait_element(self, by, element, timeout=30):
        try:
            element_present = EC.presence_of_element_located((by, element))
            WebDriverWait(self._br, timeout).until(element_present)
        except TimeoutException, err:
            self.logger.warn('Can not find element {} by {}'.format(element, by))
            self.logger.warn('Query time out as {}'.format(err))
            return False
        except Exception, err:
            self.logger.warn('Can not find element {} by {}'.format(element, by))
            self.logger.warn('Query failed as {}'.format(err))
            return False
        else:
            return True

    def find_person(self, given_info=None):
        if given_info is None:
            return None
        self.logger.info('Start to locate a person')
        self.logger.debug('Given info is {}'.format(given_info))
        self._open_url(self.FIND_PERSON_URL, wait_method=By.ID, wait_element='MainContent_formSubmit_searchButton')

        if given_info is None:
            return None
        for info in given_info:
            self.logger.debug('Set attribute {} to {}'.format(info, given_info[info]))
            if info in self.TEXT_ID_DICT:
                self._br.find_element_by_id(self.TEXT_ID_DICT[info]).send_keys(given_info[info])

            elif info in self.AgeRangeID:
                self._br.execute_script(
                    'document.getElementById("{}").value = {}'.format(self.AgeRangeID[info], given_info[info]))

            elif info == self.State:
                options = self._br.find_element_by_id(self.SELECT_ID_DICT[self.State]).find_elements_by_tag_name(
                    'option')
                for option in options:
                    if option.get_attribute('value') == given_info[info]:
                        option.click()
                        break
                else:
                    self.logger.warn('target state {} is not found, use all states to query'.format(given_info[info]))
                    options[0].click()

        self._br.find_element_by_id(self.SearchButtonID).click()
        time.sleep(3)
        if self._br.title == 'Public Records':
            self.logger.warn('Cannot find target person\'s information')
            return None

        table = self._br.find_element_by_xpath('//*[@id="resultscontent"]/tbody')
        person_info = table.find_elements_by_class_name('oddrow')
        person_info.extend(table.find_elements_by_class_name('evenrow'))
        self.logger.info('Total {} person find with given info'.format(len(person_info)))
        person_info_dict = {}
        for person in person_info:
            lex_id = re.findall(r'LexID\(sm\):\s.(\d+)', person.find_elements_by_css_selector('td')[-1].text)[0]
            name_tag = person.find_elements_by_css_selector('td')[1].find_element_by_css_selector('a')
            person_info_dict[lex_id] = {
                'url': name_tag.get_attribute('href'),
                'name': name_tag.text.split('\n')
            }

        lex_id_list = person_info_dict.keys()

        # Start to query detail info of every people
        for lex_id in lex_id_list:
            self._open_url(person_info_dict[lex_id]['url'], wait_element='MainContent_resultsToolbar_deliveryPanel',
                           wait_method=By.ID)
            # self._open_url(url='file:///Users/warn/Documents/temp/Results.htm',
            #                wait_element='reportcontentlisting',
            #                wait_method=By.ID)
            info_list = self._br.find_element_by_id('mainbody1').find_elements_by_class_name('reportSection')
            for info in info_list:
                info_name = info.find_element_by_class_name('ReportHeader').text
                if info_name.endswith('JUDGMENT AND LIEN FILINGS'):
                    details = info.find_elements_by_id('resultscontent')
                    person_info_dict[lex_id]['JUDGMENT AND LIEN FILINGS'] = []
                    for i in range(0, len(details), 2):
                        self.logger.debug(details[i].text)
                        state_info = details[i].find_element_by_css_selector('td').text
                        record = self._get_info_from_tr_with_subtext(details[i + 1])
                        record['state'] = state_info
                        person_info_dict[lex_id]['JUDGMENT AND LIEN FILINGS'].append(record)

                elif info_name == 'Criminal Records':
                    details = info.find_elements_by_id('resultscontent')
                    person_info_dict[lex_id][info_name] = []
                    for i in range(0, len(details), 3):
                        self.logger.debug(details[i + 1].text)
                        court_state = re.findall(r'([\w\s]+)\s+Court Report', details[i + 1].text)
                        if not court_state:
                            court_state = re.findall(r'([\w\s]+)\s+Department Of Corrections', details[i + 1].text)
                        court_state = court_state[0]
                        criminal_record = self._get_info_from_tr_with_subtext(details[i + 2])
                        criminal_record['State'] = court_state
                        person_info_dict[lex_id][info_name].append(criminal_record)

                else:
                    details = info.find_elements_by_class_name('resultstable')
                    person_info_dict[lex_id][info_name] = self._handle_detail_info(info_name, details)

        return person_info_dict

    def _get_info_from_tr(self, detail):
        record = {}
        info_tr_list = detail.find_element_by_css_selector('tbody').find_elements_by_css_selector('tr')
        for info_tr in info_tr_list:
            info_td_list = info_tr.find_elements_by_css_selector('td')
            if len(info_td_list) != 2:
                continue
            record[info_td_list[0].text.strip(':')] = info_td_list[1].text

        return record

    def _get_info_from_tr_with_subtext(self, detail):
        record = {}
        record_name = ''
        info_tr_list = detail.find_element_by_css_selector('tbody').find_elements_by_css_selector('tr')
        self.logger.debug(detail.text)
        for i in range(len(info_tr_list)):
            info_tr = info_tr_list[i]
            info_td_list = info_tr.find_elements_by_css_selector('td')
            if info_tr.get_attribute('id') == 'subtext-request':
                record_name = info_tr.text
                if i < len(info_tr_list) and info_tr_list[i + 1].get_attribute('id') == 'subtext2':
                    record[record_name] = []
                else:
                    record[record_name] = {}
            elif info_tr.get_attribute('id') == 'subtext2':
                if record_name == 'Filing Information':
                    if 'Fillings' in record[record_name]:
                        record[record_name]['Fillings'].append({})
                    else:
                        record[record_name]['Fillings'] = [{}]
                else:
                    record[record_name].append({})
            elif len(info_td_list) == 2:
                attribute_name = info_td_list[0].text.strip(':')
                if isinstance(record[record_name], dict):
                    record[record_name][info_td_list[0].text.strip(':')] = info_td_list[1].text
                    if record_name == 'Filling Information' and attribute_name not in {u'Certificate Number',
                                                                                       u'Amount',
                                                                                       u'Filing Date'}:
                        record[record_name]['Fillings'][-1][attribute_name] = info_td_list[1].text
                elif isinstance(record[record_name], list):
                    record[record_name][-1][attribute_name] = info_td_list[1].text
        return record

    def _handle_detail_info(self, info_name, details):
        info_list = []
        if info_name in {u'Historical Person Locator', u'Person Locator 2', u'Person Locator 4', u'Email Address'}:
            for detail in details:
                info_list.append(self._get_info_from_tr(detail))
        elif info_name in {u'Deed Records', u'Assessment Record', u'Mortgage Record'}:
            for detail in details:
                info_list.append(self._get_info_from_tr_with_subtext(detail))

        elif info_name in {u'Voter Registration', u'UCC Filings'}:
            record = None
            for detail in details:
                if detail.find_element_by_css_selector('thead').text.startswith('1'):
                    if record is not None:
                        info_list.append(record)
                    record = []
                tag = info_name.split(' ')[0]
                state = re.findall(r'([\w\s]+?)\s+{}'.format(tag), detail.find_element_by_css_selector('thead').text)
                record.append(self._get_info_from_tr_with_subtext(detail))
                record[-1]['State'] = state.strip()

            if record is not None:
                info_list.append(record)

        else:
            self.logger.warn('Unknown info name {}, cannot handle this type of information'.format(info_name))
            self.logger.warn('Current url is {}'.format(self._br.current_url))
            self._cannot_handle_info.append((info_name, details))
        return info_list


if __name__ == '__main__':
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    test = LexisNexisCtrl(username='tianyutong', password='Uchicago!')
    people_info = {test.FirstName: 'Chris',
                   test.LastName: 'Paul',
                   test.State: 'CA',
                   test.AgeLow: 25,
                   test.AgeHigh: 45
                   }
    try:
        test.start()
        result = test.find_person(people_info)
        from pprint import pprint

        pprint(result)
    except Exception, err:
        import traceback

        traceback.print_exc()
    finally:
        test.stop()
