#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: http_ctrl
# @Date: 2017-02-13
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import urllib
import urllib2
import time
import logging
import requests


class HttpCtrl(object):
    def __init__(self, logger=None):
        if logger is None:
            self.logger = logging.getLogger(self.__class__.__name__)

        else:
            self.logger = logger.getLogger(self.__class__.__name__)

    # def get(self, url, data_list=None, header_list=None, max_try=3, timeout=10):
    #
    #     if not url.startswith('http'):
    #         url = 'http://{}'.format(url)
    #
    #     if data_list:
    #         url = "{}?{}".format(url, urllib.urlencode(data_list))
    #
    #     self.logger.info('Start to access {}'.format(url))
    #     query = urllib2.Request(url)
    #     if header_list is not None:
    #         for header in header_list:
    #             query.add_header(header[0], header[1])
    #     current_try = 0
    #     while current_try < max_try:
    #         self.logger.debug('Access time {}'.format(current_try + 1))
    #         try:
    #             response = urllib2.urlopen(query)
    #             html = ''
    #             while True:
    #                 current_html = response.read(1024)
    #                 # print current_html
    #                 if not len(current_html):
    #                     break
    #
    #                 html = '{}{}'.format(html, current_html)
    #
    #             self.logger.debug('Response is {}'.format(html))
    #             response.close()
    #             return html
    #         except Exception, e:
    #             self.logger.warn('Get failed as {}'.format(e))
    #             current_try += 1
    #             time.sleep(timeout)
    #
    #     self.logger.error("Cannot open page {}".format(url))
    #     raise Exception("Cannot open page {}".format(url))

    def get(self, url, data_list=None, headers=None, max_try=3, timeout=10):

        if not url.startswith('http'):
            url = 'http://{}'.format(url)

        if data_list:
            url = "{}?{}".format(url, urllib.urlencode(data_list))

        self.logger.info('Start to access {}'.format(url))
        current_try = 0
        while current_try < max_try:
            self.logger.debug('Access time {}'.format(current_try + 1))
            try:
                r = requests.get(url, headers=headers)
                time.sleep(0.1)
                if r.status_code == 200:
                    return r.text
            except Exception, e:
                self.logger.warn('Get failed as {}'.format(e))

            current_try += 1
            time.sleep(timeout)

        self.logger.error("Cannot open page {}".format(url))
        raise Exception("Cannot open page {}".format(url))

    def post(self, url, data_list=None, headers=None, max_try=3, timeout=10):

        if not url.startswith('http'):
            url = 'http://{}'.format(url)

        self.logger.info('Start to access {}'.format(url))
        self.logger.debug('Start to post data {}'.format(data_list))

        for i in range(max_try):
            self.logger.debug('Start {}th time trying'.format(i + 1))

            try:
                r = requests.post(url=url, data=data_list, headers=headers)
                time.sleep(0.1)
                if r.status_code == 200:
                    return r.text

            except Exception, e:
                self.logger.warn('Post failed as {}'.format(e))

            time.sleep(timeout)

        self.logger.error("Cannot open page {}".format(url))
        raise Exception("Cannot open page {}".format(url))
