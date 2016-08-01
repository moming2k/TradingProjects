#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: base_clasee
# Author: Mark Wang
# Date: 24/7/2016

import os
import urllib
import urllib2
import traceback
import time


class BaseClass(object):
    def __init__(self, key, proxy=None, logger=None):
        self._api_key = key
        self._proxy = proxy
        if logger is None:
            import logging
            self.logger = logging.getLogger(self.__class__.__name__)
        else:
            self.logger = logger

    def http_get(self, url, parameters=None, timeout=10, max_try=3):
        if parameters is not None:
            url = '{}?{}'.format(url, urllib.urlencode(parameters))
        self.logger.debug('Start to get page {}'.format(url))
        # print url
        if self._proxy is not None:
            proxy = urllib2.ProxyHandler({'http': self._proxy})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener=opener)
        else:
            opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        try_time = 0
        while try_time < max_try:
            try:
                # req = opener.open(fullurl=url)
                response = urllib2.urlopen(url)
                # response = opener.open(fullurl=url)
                return response.read()
            except Exception, err:
                self.logger.warn('Cannot get page {} as {}'.format(url, err))
                traceback.print_exc()
                try_time += 1
                if 'Inspiron' in os.uname()[1]:
                    time.sleep(60)
                else:
                    time.sleep(timeout)

        raise Exception('cannot open url {}'.format(url))
