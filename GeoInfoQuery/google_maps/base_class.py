#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: base_clasee
# Author: Mark Wang
# Date: 24/7/2016

import urllib
import urllib2
import traceback
import time


class BaseClass(object):
    def __init__(self, key, proxy=None):
        self._api_key = key
        self._proxy = None

    def http_get(self, url, parameters=None, timeout=10, max_try=3):
        if parameters is not None:
            url = '{}?{}'.format(url, urllib.urlencode(parameters))

        print url
        if self._proxy is not None:
            proxy = urllib2.ProxyHandler({'http': self._proxy})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener=opener)

        try_time = 0
        while try_time < max_try:
            try:
                req = urllib2.Request(url=url)
                response = urllib2.urlopen(req, timeout=timeout)
                return response.read()
            except Exception, err:
                traceback.print_exc()
                print err
                try_time += 1
                time.sleep(10)
