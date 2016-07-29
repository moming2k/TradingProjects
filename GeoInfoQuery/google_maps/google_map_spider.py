#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: google_map_spider
# Author: Mark Wang
# Date: 29/7/2016

import os
import re
import json
import logging
import random
import time

import mechanize
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class GoogleMapSpider(object):
    def __init__(self, spider_type="mechanize"):
        self.spider_type = spider_type
        self.browser = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def start(self):
        self.logger.info("spider type is {}, will start now".format(self.spider_type))
        self.stop()
        if self.spider_type == 'mechanize':
            self.browser = mechanize.Browser()
            self.browser.set_handle_robots(False)
        elif self.spider_type == 'selenium':
            if os.uname()[0] == 'Darwin':
                self.browser = webdriver.Chrome("/Users/warn/chromedriver")
            elif os.uname()[1] == 'warn-Inspiron-3437':
                self.browser = webdriver.Chrome("/home/warn/chromedriver")

    def stop(self):
        self.logger.info("Stop spider")
        if self.browser is not None:
            if self.spider_type == 'mechanize':
                self.browser.close()
                self.browser = None

            elif self.spider_type == 'selenium':
                self.browser.close()
                self.browser = None

    def _get_page_html(self, url):
        self.logger.debug("Query url is {}".format(url))
        max_try = 3
        html = None

        while max_try > 0:
            try:
                if self.spider_type == 'mechanize':
                    page = self.browser.open(url)
                    html = page.read()
                elif self.spider_type == 'selenium':
                    self.browser.get(url)
                    html = self.browser.page_source
            except Exception, err:
                import traceback
                traceback.print_exc()
                print err
                max_try -= 1
            else:
                break
        return html

    def get_detail_type(self, url):
        if not url:
            return ""

        if self.spider_type == 'mechanize':
            html = self._get_page_html(url)

            if html is None:
                raise Exception("Unable to reach {}".format(url))

            result = re.findall(ur'cacheResponse\((.*)\)', html)
            if not result:
                self.logger.warn('Cannot find target information of given url')
                return ""
            info = unicode(result[0], encoding='utf8')

            brace_num = -1
            new_info_list = []
            index = 0
            for c in info:
                if c == '[':
                    brace_num += 1
                if c == ']':
                    brace_num -= 1

                if brace_num == 0 and c == ',':
                    index += 1
                elif index > 9:
                    new_info = u"".join(new_info_list)
                    break
                elif index == 9:
                    new_info_list.append(c)
            else:
                self.logger.warn('Can not find target information')
                self.logger.debug('information is {}'.format(info))
                return ""

            try:
                b = json.loads(new_info, encoding='utf8')
                return b[-16]
            except Exception, err:
                import traceback
                traceback.print_exc()
                self.logger.warn('translate json file failed as {}'.format(err))
                return ""

        elif self.spider_type == 'selenium':
            max_try = 3
            while max_try > 0:
                try:
                    detail_type = self.wait_selenium(
                        url, by=By.XPATH, timeout=30,
                        element='//*[@id="pane"]/div/div[1]/div/div/div[1]/div[2]/div[2]/div[2]/span/span[1]/button')
                    return detail_type.text
                except Exception, err:
                    print err
                    self.stop()
                    self.start()
                    time.sleep(60 if os.uname()[1] == 'warn-Inspiron-3437' else 5)
                    max_try -= 1

            self.logger.error("Get url {} failed".format(url))
            raise Exception('Get url {} failed'.format(url))

    def wait_selenium(self, url, by=By.XPATH, element=None, timeout=10):
        self.logger.debug("Target url is {}".format(url))
        self.browser.get(url)
        try:
            element_present = EC.presence_of_element_located((by, element))
            WebDriverWait(self.browser, timeout).until(element_present)
            time.sleep(random.randint(1, 10))
        except TimeoutException:
            self.logger.error("Time out while wait for element presents")
            raise TimeoutException('Time out while wait for element presents')

        else:
            return self.browser.find_element(by=by, value=element)
