#!/usr/bin/env python
# -*- coding: utf-8 -*-

# File Name: xvfbwrapper_test
# Created by warn on 8/8/16

import os
import time

from xvfbwrapper import Xvfb
from selenium import webdriver

if __name__ == '__main__':
    vdisplay = Xvfb(width=1366, height=768)
    vdisplay.start()
    if os.uname()[0] == 'Darwin':
        # self.browser = webdriver.Chrome("/Users/warn/chromedriver", chrome_options=chrome_options)
        br = webdriver.Chrome("/Users/warn/chromedriver")
        # self.browser = webdriver.PhantomJS()
        # self.browser.set_window_size(1124, 850)
    elif os.uname()[1] == 'warn-Inspiron-3437':
        br = webdriver.Chrome("/home/warn/chromedriver")
    elif os.uname()[1] == 'ewin3011':
        br = webdriver.Chrome("/home/wangzg/chromedriver")

    br.implicitly_wait(30)
    br.get('https://maps.google.com/?cid=4441111789754827753')
    time.sleep(10)
    detail_type = br.find_elements_by_xpath(
        '//*[@id="pane"]/div/div[1]/div/div/div[1]/div[2]/div[2]/div[2]/span/span[1]/button')
    if detail_type:
        print detail_type
        print detail_type[0].text
    else:
        print 'no such element'

    br.quit()
    vdisplay.stop()
