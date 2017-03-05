#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step2_generate_run_up_report_from_forecast
# @Date: 2017-03-05
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from ..constants.constants import Constant as const
from ..report_sorter.report_sorter import ReportSorter

report_path = const.FORECAST_REPORT_PATH
save_path = const.FORECAST_RUN_UP_REPORT_PATH

if not os.path.isdir(save_path):
    os.makedirs(save_path)


def process_report_df(report_name):
    df = pd.read_pickle(os.path.join(report_path, report_name))
    sorter = ReportSorter(stock_price_path=const.STOCK_PRICE_20170214_PATH, index_data_path=const.SZ_399300_PATH)

    y = 1
    col_list = []
    for x in [5, 10, 15, 20]:
        col_name = '{}_{}x_{}y'.format(const.RUN_UP_RATE, x, y)
        df[col_name] = sorter.add_run_up_data(df, x=x, y=y, price_type=const.STOCK_CLOSE_PRICE)
        col_list.append(col_name)

    df = df.dropna(subset=col_list, how='all')
    if df.empty:
        return 1

    else:
        df.to_pickle(os.path.join(save_path, report_name))
        return 0


if __name__ == '__main__':
    import sys
    import logging

    import pathos

    process_num = 18

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    file_list = os.listdir(report_path)
    pool = pathos.multiprocessing.ProcessingPool(process_num)

    pool.map(process_report_df, file_list)
