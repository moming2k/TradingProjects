#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: lexis_nexis_ctrl
# Author: Mark Wang
# Date: 4/8/2016

import os
import logging
import time
from urllib2 import URLError

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

START_URL = "http://www.lexisnexis.com/en-us/products/lexis-advance/lexis-advance-customer.page"
FIND_PERSON_URL = 'https://r3.lexis.com/laprma/FindAPerson.aspx?national=true'


class LexisNexisCtrl(object):
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
        self._open_url(START_URL)
        self._window_id_dict['start_window'] = self._br.current_window_handle
        self._br.find_element_by_xpath("/html/body/section[2]/div/div/div/div[1]/div/p[1]/a[1]").click()
        for window_id in self._br.window_handles:
            if window_id != self._window_id_dict['start_window']:
                self._window_id_dict['sign_in_window'] = window_id
                break
        self._br.switch_to_window(self._window_id_dict['start_window'])
        self._br.find_element_by_id('userid').send_keys(self._username)
        self._br.find_element_by_id('password').send_keys(self._password)
        self._br.find_element_by_id('signInSbmtBtn').click()
        while not self.wait_element(by=By.XPATH, element='//*[@id="mainSearch"]'):
            self.logger.warn('page not load well, pleas wait')
            # self._br.find_element_by_xpath('//*[@id="nav_productswitcher_arrowbutton"]').click()
            # self._br.find_element_by_xpath('//*[@id="1000200"]').click()

    def _open_url(self, url, wait_element=None, wait_method=By.XPATH, max_try=3, timeout=30):
        for try_time in range(max_try):
            try:
                self.logger.debug("Start to get url {}".format(url))
                self._br.get(url)
                if wait_element is not None:
                    if not self.wait_element(wait_method, wait_element, timeout):
                        raise Exception('Element {} by {} not found.'.format(wait_element, wait_method))
            except Exception, err:
                self.logger.warn("Open target url failed as {}".format(err))
                time.sleep(10)
                self.start()
        else:
            raise URLError("Can not open url {}".format(url))

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

    def find_a_person(self, given_info=None):
        if given_info is None:
            return None
        self._open_url(FIND_PERSON_URL, wait_method=By.ID, wait_element='MainContent_formSubmit_searchButton')
