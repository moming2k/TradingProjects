#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step5_generate_return_file
# @Date: 2017-01-12
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os
import datetime

import pandas as pd
import numpy as np

from constant import Constant
from functions import calculate_trade_info

const = Constant()

# Define some folder path
today_str = datetime.datetime.today().strftime('%Y%m%d')
root_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'
data_path = os.path.join(root_path, 'data')
temp_path = os.path.join(root_path, 'temp')
today_path = os.path.join(temp_path, today_str)
stock_price_path = os.path.join(root_path, 'stock_price')
report_action_path = os.path.join(data_path, 'report_info')

if not os.path.isdir(today_path):
    os.makedirs(today_path)

if not os.path.isdir(report_action_path):
    os.makedirs(report_action_path)

# read data file
trading_day_list = pd.read_pickle(os.path.join(temp_path, '20170108', '__trading_days_list.p'))

holding_days = 66


def calculate_return(file_name):
    if not os.path.isfile(os.path.join(report_action_path, file_name)):
        return pd.DataFrame()
    report = pd.read_pickle(os.path.join(report_action_path, file_name))
    ticker = file_name[:-5]
    market_type = file_name[-4:-2]

    ow_list = report[report[const.REPORT_ACTION] == const.OVERWEIGHT]
    rd_list = report[report[const.REPORT_ACTION] == const.REDUCTION]

    def process_ow_info(row):
        ann_date = row[const.REPORT_ANNOUNCE_DATE]
        trade_day = trading_day_list[trading_day_list > ann_date].head(holding_days)
        if trade_day.empty:
            temp_result = {const.REPORT_RETURN_RATE: np.nan, const.REPORT_SELL_DATE: np.nan,
                           const.REPORT_BUY_DATE: np.nan, const.REPORT_MARKET_TYPE: np.nan,
                           const.REPORT_MARKET_TICKER: np.nan, const.REPORT_BUY_PRICE: np.nan}
            return pd.Series(temp_result)
        sell_day = trade_day.tolist()[-1]
        temp_df = rd_list[rd_list[const.REPORT_ANNOUNCE_DATE] > ann_date]
        temp_df = temp_df[temp_df[const.REPORT_ANNOUNCE_DATE] < sell_day]

        if temp_df.empty:
            return calculate_trade_info(announce_date=ann_date, ticker_info=ticker, market_info=market_type,
                                        holding_days=holding_days, buy_price_type=const.STOCK_OPEN_PRICE,
                                        sell_price_type=const.STOCK_CLOSE_PRICE,
                                        after_price_type=const.STOCK_OPEN_PRICE)

        else:
            sell_date = temp_df.ix[temp_df.first_valid_index(), const.REPORT_ANNOUNCE_DATE]
            return calculate_trade_info(announce_date=ann_date, ticker_info=ticker, market_info=market_type,
                                        sell_date=sell_date, buy_price_type=const.STOCK_OPEN_PRICE,
                                        sell_price_type=const.STOCK_CLOSE_PRICE,
                                        after_price_type=const.STOCK_OPEN_PRICE)

    return ow_list.merge(ow_list.apply(process_ow_info, axis=1), left_index=True, right_index=True)


if __name__ == '__main__':
    import pathos

    processor_num = 10
    ticker_list = os.listdir(report_action_path)

    pool = pathos.multiprocessing.ProcessingPool(processor_num)

    result_dfs = pool.map(calculate_return, ticker_list)

    # result_dfs = []
    #
    # for file_name in ticker_list:
    #     result_dfs.append(calculate_return(file_name))

    result_df = pd.concat(result_dfs, axis=0)

    result_df.to_pickle(os.path.join(today_path, 'has_reduction_holding_days_{}.p'.format(holding_days)))
    result_df.to_excel(os.path.join(today_path, 'has_reduction_holding_days_{}.xlsx'.format(holding_days)))
    result_df.to_csv(os.path.join(today_path, 'has_reduction_holding_days_{}.csv'.format(holding_days)),
                     encoding='utf8')
