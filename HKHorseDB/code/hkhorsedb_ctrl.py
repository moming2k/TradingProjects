#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: hkhorsedb_ctrl
# @Date: 2016-12-30
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

from constant import Constant

from BeautifulSoup import BeautifulSoup
from selenium import webdriver


class HkhorseDbCtrl(Constant):
    def __init__(self):
        self.browser = None

    def start(self):
        if os.uname()[0] == 'Darwin':
            self.browser = webdriver.Chrome("/Users/warn/chromedriver")
        elif os.uname()[1] == 'warn-Inspiron-3437':
            self.browser = webdriver.Chrome("/home/warn/chromedriver")
        elif os.uname()[1] == 'ewin3011':
            self.browser = webdriver.Chrome("/home/wangzg/chromedriver")

        self._login()

    def _login(self):
        self.browser.get(self.ROOT_URL)
        self.browser.find_element_by_name('uname').send_keys('markwang')
        self.browser.find_element_by_name('pass').send_keys('1212az')
        self.browser.find_element_by_xpath(self.LOGIN_XPATH).click()

    def stop(self):
        if self.browser is not None:
            try:
                self.browser.close()
            except Exception, err:
                print ('Stop browser failed as {}'.format(err))
            finally:
                self.browser = None

    def get_win_loss_rate(self, date):
        url = 'http://www.hkhorsedb.com/cseh/poddsleftxml.php?rdate={}&vrecno=1&pcode=1'.format(date)
        self.browser.get(url)

        page_source = self.browser.page_source
        soup = BeautifulSoup(page_source)
        table = soup.findAll('table')[-1]
        tr_list = table.findAll('tr')

        match_num = len(tr_list[0].findAll('td'))
        result_list = [[] for _ in range(match_num)]

        for tr in tr_list[1:]:
            td_list = tr.findAll('td')
            if len(td_list) < match_num * 3:
                continue
            # print td_list
            for i in range(match_num):
                horse_name = td_list[3 * i + 1].text
                try:
                    win_loss_rate = float(td_list[3 * i + 2].text)
                except Exception:
                    continue

                if len(td_list[3 * i + 2].findAll('font')) > 0:
                    is_winner = 1
                else:
                    is_winner = 0

                result_list[i].append((horse_name, win_loss_rate, is_winner))

        return result_list


if __name__ == '__main__':

    import pprint

    test = HkhorseDbCtrl()
    test.start()
    try:
        pprint.pprint(test.get_win_loss_rate('09032016'))
    finally:
        test.stop()
