#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: download_sh_report
# @Date: 2017-02-16
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime

from .report_downloader.sh_report_downloader import SHReportDownloader

if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')
    downloader = SHReportDownloader()

    result_df = downloader.main_downloader()

    result_df.to_pickle('{}_sh_report.p'.format(datetime.datetime.today().strftime('%Y%m%d')))
    result_df.to_excel('{}_sh_report.xlsx'.format(datetime.datetime.today().strftime('%Y%m%d')), index=False)
