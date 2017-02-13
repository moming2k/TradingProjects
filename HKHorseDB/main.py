#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: main
# @Date: 2017-02-13
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import sys
import logging

from download_system.horse_basic_downloader import HorseBasicDownloader

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

if __name__ == '__main__':
    test = HorseBasicDownloader(logger=logging)

    horse_basic_info = test.download_horse_info()
    horse_basic_info.to_pickle('horse_info.p')
    horse_basic_info.to_excel('horse_info.xlsx')
