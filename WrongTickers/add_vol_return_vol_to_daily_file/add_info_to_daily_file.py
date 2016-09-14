#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_info_to_daily_file
# Author: Mark Wang
# Date: 14/9/2016

import os

import pandas as pd
import numpy as np

from ..constants import *

parent_path = '/home/wangzg/Documents/WangYouan/research/Wrong_tickers'
data_dir = 'Stock_data'
result_dir = 'result_csv'

volatility_df = pd.read_csv(os.path.join(parent_path, data_dir, 'daily_stock_volatility.csv'), index_col=0)
volume_df = pd.read_csv(os.path.join(parent_path, data_dir, 'daily_volume.csv'), index_col=0)
return_df = pd.read_csv(os.path.join(parent_path, data_dir, 'daily_market_return.csv'), index_col=0)

if __name__ == "__main__":
    data_df = pd.read_csv(os.path.join(parent_path, result_dir, 'wrong_ticker_whole_daily_data_SDC.csv'),
                          dtype={CUSIP_WRONG: str, CUSIP_REAL: str})
    data_df[DAILY_MARKET_RETURN] = data_df[DATE].apply(
        lambda x: return_df.loc[x, DAILY_MARKET_RETURN] if x in return_df.index else np.nan)
    data_df[DAILY_MARKET_TRADING_VOL] = data_df[DATE].apply(
        lambda x: volume_df.loc[x, DAILY_MARKET_TRADING_VOL] if x in volume_df.index else np.nan)
    data_df[DAILY_VOLATILITY] = data_df[DATE].apply(
        lambda x: volatility_df.loc[x, DAILY_VOLATILITY] if x in volatility_df.index else np.nan)
    data_df.to_csv(os.path.join(parent_path, result_dir, 'wrong_ticker_whole_daily_data_SDC(add_daily).csv'),
                   index=False, encoding='utf8')
