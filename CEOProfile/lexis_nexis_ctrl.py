#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: lexis_nexis_ctrl
# Author: Mark Wang
# Date: 4/8/2016

import os
import logging

from selenium import webdriver


class LexisNexisCtrl(object):
    def __init__(self, username, password, logger=None):
        self._username = username
        self._password = password
        self._br = None
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
            self.browser = webdriver.Chrome("/Users/warn/chromedriver")
        elif os.uname()[1] == 'warn-Inspiron-3437':
            self.browser = webdriver.Chrome("/home/warn/chromedriver")
        elif os.uname()[1] == 'ewin3011':
            self.browser = webdriver.Chrome("/home/wangzg/chromedriver")
        self._login()
        self.logger.info("Start browser successfully.")

    def stop(self):
        if self._br is not None:
            self.logger.debug("Stop selenium browser")
            try:
                self._br.stop()
            except Exception, err:
                self.logger.warn('Cannot stop browser, as {}'.format(err))
            finally:
                self._br = None

    def _login(self):
        pass
