#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: report_sorter
# @Date: 2017-03-03
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

# import logging

import pandas as pd

from ..constants.constants import Constant
from ..util_functions.util_function import calculate_stock_run_up_rate


class ReportSorter(Constant):
    def __init__(self, stock_price_path=None, index_data_path=None):

        # if logger is None:
        #     self.logger = logging.getLogger(self.__class__.__name__)
        #
        # else:
        #     self.logger = logger.getLogger(self.__class__.__name__)

        self.index_price_path = self.SZ_399300_PATH if index_data_path is None else index_data_path
        self.stock_price_path = self.STOCK_PRICE_20170214_PATH if stock_price_path is None else stock_price_path

    def add_run_up_data(self, report_df, x=20, y=1, price_type=None):
        """ Add run up to input report df, run up is the how many rates this stock over performance the index
            run_up = (P_stock_y - P_stock_x) / P_stock_x - (P_index_y - P_index_x) / P_index_x
            @:param report_df import report df, should have
            @:param x the former date usually choose from 5, 10, 15, 20
            @:param y the later date usually yesterday
            @:return report df add run up info
        """
        # self.logger.info('Start to calculate report_df, x is {}, y is {}'.format(x, y))
        index_df = pd.read_pickle(self.index_price_path)
        price_type = self.STOCK_CLOSE_PRICE

        def process_row_info(row):
            if self.REPORT_TICKER in row:
                ticker = row[self.REPORT_TICKER]

            else:
                ticker = row[self.REPORT_MARKET_TICKER]

            query_date = row[self.REPORT_ANNOUNCE_DATE]
            return calculate_stock_run_up_rate(ticker=ticker, query_date=query_date, x=x, y=y,
                                               stock_price_path=self.stock_price_path, index_price_df=index_df,
                                               price_type=price_type)

        return report_df.apply(process_row_info, axis=1)


if __name__ == '__main__':
    import os

    test = ReportSorter()

    report_df = pd.read_pickle(os.path.join(Constant.INSIDER_EXE_GT2_PATH, '600507.p'))
    y = 1
    for x in [5, 10, 15, 20]:
        col_name = '{}_{}x_{}y'.format(test.RUN_UP_RATE, x, y)
        report_df[col_name] = test.add_run_up_data(report_df, x, y)

    report_df.to_csv(os.path.join(test.TEMP_PATH, 'test.csv'), encoding='utf8')