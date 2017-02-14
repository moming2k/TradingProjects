#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: jockey_main
# @Date: 2017-02-14
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import sys
import logging
import datetime

from download_system.jockey_basic_downloader import JockeyBasicDownloader

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

if __name__ == '__main__':
    path = '/home/wangzg/Documents/WangYouan/Trading/HKHorse/CollectedData'
    today_str = datetime.datetime.today().strftime('%Y%m%d')
    test = JockeyBasicDownloader(logger=logging)

    basic_info = test.download_jockey_info()

    print basic_info
    # basic_info.to_pickle('{}_jockey_info.p'.format(today_str))
    # basic_info.to_excel('{}_jockey_info.xlsx'.format(today_str))
    basic_info.to_pickle(os.path.join(path, '{}_jockey_info.p'.format(today_str)))
    basic_info.to_excel(os.path.join(path, '{}_jockey_info.xlsx'.format(today_str)))
