#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: download_stock_report
# @Date: 2017-02-16
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime

from .report_downloader.sz_report_downloader import SZReportDownloader


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')
    downloader = SZReportDownloader()

    result_df = downloader.main_downloader()

    result_df.to_pickle('{}_sz_report.p'.format(datetime.datetime.today().strftime('%Y%m%d')))
    result_df.to_excel('{}_sz_report.xlsx'.format(datetime.datetime.today().strftime('%Y%m%d')))
