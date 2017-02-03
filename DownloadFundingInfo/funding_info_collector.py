#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: funding_info_collector
# @Date: 2017-02-02
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

from DownloadFundingInfo.constants import Constants
from DownloadFundingInfo.util_function import get


class FundingInfoCollector(Constants):
    def __init__(self):
        pass

    def __get_all_funding_info(self):
        pass

    def __get_funding_details(self, funding_url):
        pass


if __name__ == '__main__':
    html = get(Constants.LIST_URL)
