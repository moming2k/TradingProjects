#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: constant
# @Date: 2017-01-03
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

from parameters import Parameters


class Constant(Parameters):
    URL = 'http://datacenter.mep.gov.cn/report/air_daily/air_dairy.jsp'

    # define some query parameters
    END_DATE = 'enddate'
    START_DATE = 'startdate'
    PAGE = 'page'
    CITY = 'city'
    DATE = "date"
    AQI = 'AQI'
    AIR_QUALITY_LEVEL = 'AirQualityLevel'
    PRIMARY_POLLUTANT = 'PrimaryPollutant'

    COLUMNS = [CITY, AQI, AIR_QUALITY_LEVEL, DATE, PRIMARY_POLLUTANT]


if __name__ == '__main__':
    # prefix = 'python download_data_step1.py'
    data_prefix = '''2014-01-01	2014-06-30
2014-07-01	2014-12-31
2015-01-01	2015-06-30
2015-07-01	2015-12-31
2016-01-01	2016-06-30
2016-07-01	2016-12-31'''.split('\n')

    result_list = []
    for row in data_prefix:
        result_list.append(row.split('\t'))

    print result_list
