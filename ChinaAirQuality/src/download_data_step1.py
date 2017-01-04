#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: data_period_1
# @Date: 2017-01-03
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import time
import datetime
import logging

from download_data_urllib_ctrl import AIRDailyDownloadUrllib

output_path = '../data'


def download_data(start_date, end_date):
    download_api = AIRDailyDownloadUrllib()

    s_day = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    e_day = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    delta_time = datetime.timedelta(days=1)
    i = s_day
    failed_date_list = []
    while i <= e_day:
        download_api.start()
        try:
            date_str = i.strftime('%Y-%m-%d')
            df = download_api.get_target_day_date(date_str)
            save_file_name = 'air_data_{}'.format(''.join(date_str.split('-')))

            df.to_csv(os.path.join(output_path, '{}.csv'.format(save_file_name)), encoding='utf8')
            df.to_pickle(os.path.join(output_path, '{}.p'.format(save_file_name)))

        except Exception, err:
            import traceback

            traceback.print_exc()
            failed_date_list.append(i)

        finally:
            download_api.stop()
            time.sleep(3)
            i += delta_time

    return failed_date_list


def process_parameter(parameters):
    return download_data(parameters[0], parameters[1])


if __name__ == '__main__':
    import pathos

    process_num = 6

    date_list = [['2014-01-01', '2014-06-30'], ['2014-07-01', '2014-12-31'], ['2015-01-01', '2015-06-30'],
                 ['2015-07-01', '2015-12-31'], ['2016-01-01', '2016-06-30'], ['2016-07-01', '2016-12-31']]

    pool = pathos.multiprocessing.ProcessingPool(process_num)

    failed_list = pool.map(process_parameter, date_list)

    print failed_list
