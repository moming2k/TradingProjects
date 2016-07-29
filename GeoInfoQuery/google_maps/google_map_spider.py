#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: google_map_spider
# Author: Mark Wang
# Date: 29/7/2016

import re
import json
import logging

import mechanize


class GoogleMapSpider(object):
    def __init__(self, spider_type="mechanize"):
        self.spider_type = spider_type
        self.browser = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def start(self):
        self.logger.info("spider type is {}, will start now".format(self.spider_type))
        if self.spider_type == 'mechanize':
            self.browser = mechanize.Browser()
            self.browser.set_handle_robots(False)

    def stop(self):
        self.logger.info("Stop spider")
        if self.spider_type == 'mechanize':
            if self.browser is not None:
                self.browser.close()
                self.browser = None

    def get_detail_type(self, url):
        if not url:
            return ""

        self.logger.debug("Query url is {}".format(url))
        max_try = 3
        html = None

        while max_try > 0:
            try:
                page = self.browser.open(url)
                html = page.read()
            except Exception, err:
                import traceback
                traceback.print_exc()
                print err
                max_try -= 1
            else:
                break

        if max_try == 0 and html is None:
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
