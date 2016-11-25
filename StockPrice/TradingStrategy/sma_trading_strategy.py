#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: sma_trading_strategy
# Author: Mark Wang
# Date: 24/11/2016

import os
import datetime

import pandas as pd
from talib import abstract
import numpy as np
import pathos

from calculate_strategy_performance import calculate_strategy_performance
from all_stock_list import stock_list

if os.uname()[0] == 'Darwin':
    root_path = '/Users/warn/PycharmProjects/QuestionFromProfWang/StockPrice'
else:
    root_path = '/home/wangzg/Documents/WangYouan/research/HongKongStock'

data_path = 'YahooStockPrice'
result_path = '{}SimulateResult'.format(datetime.datetime.today().strftime('%Y%m%d'))
if not os.path.isdir(os.path.join(root_path, result_path)):
    os.makedirs(os.path.join(root_path, result_path))

start_cash = 1
delay = 30
transaction_cost = 0.01


def sma_trading_strategy(file_name):
    stock_price = pd.read_csv(os.path.join(root_path, data_path, file_name), index_col=0)
    stock_price.dropna(subset=['Volume'], inplace=True)
    stock_price['Volume'] = stock_price['Volume'].apply(int)
    stock_price = stock_price[stock_price['Volume'] != 0]
    rename_dict = {'Volume': 'volume', 'Adj Close': 'close', 'Open': 'open', 'High': 'high', 'Low': 'low'}
    stock_price.rename(columns=rename_dict, inplace=True)

    stock_price.loc[:, 'date'] = stock_price.index
    stock_price['date'] = stock_price['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
    stock_price.set_index('date', inplace=True)

    stock_price = stock_price[stock_price.index >= datetime.datetime(2006, 11, 20)]
    if stock_price.empty or stock_price.shape[0] < 1500:
        return 0
    for period1 in range(14, 4, -2):
        for period2 in range(period1 * 2, 31, 2):
            for period3 in range(7, 21, 2):
                if os.uname()[0] == 'Darwin':
                    print 'period 1 {} period 2 {} period 3 {}'.format(period1, period2, period3)
                sma_s = abstract.SMA(stock_price, timeperiod=period1) if period1 != 1 else stock_price['close']
                sma_l = abstract.SMA(stock_price, timeperiod=period2)

                dma = sma_s - sma_l
                ama = abstract.SMA(dma.to_frame('close'), timeperiod=period3)
                diff_ama_dma = dma - ama
                for threshold in range(1, 82, 10):
                    threshold = float(threshold) / 10
                    long_position = [0] * diff_ama_dma.shape[0]
                    short_position = [0] * diff_ama_dma.shape[0]
                    for i in range(delay, diff_ama_dma.shape[0]):
                        if diff_ama_dma[i - 1] < threshold < diff_ama_dma[i]:
                            long_position[i] = 1
                            short_position[i - 1] = -1

                        elif diff_ama_dma[i] < -threshold < diff_ama_dma[i - 1]:
                            long_position[i - 1] = -1
                            short_position[i] = 1

                    wealth, sharpe, stock_long, stock_short, cash_list, pnl, trade_operation = calculate_strategy_performance(
                        stock_price=stock_price['close'], start_cash=start_cash,
                        delay=delay, long_position=long_position,
                        short_position=short_position, transaction_cost=transaction_cost
                    )

                    if os.uname()[0] == 'Darwin':
                        print sharpe

                    if sharpe > 0:
                        stock_price['wealth'] = wealth
                        stock_price['short'] = stock_short
                        stock_price['long'] = stock_long
                        stock_price['cash'] = cash_list
                        stock_price['pnl'] = pnl
                        stock_price['long_pos'] = long_position
                        stock_price['short_pos'] = short_position
                        stock_price['operation'] = trade_operation

                        save_file_name = 'p1_{}_p2_{}_p3_{}_th_{}_sharpe_{:.4f}.csv'.format(period1,
                                                                                            period2,
                                                                                            period3,
                                                                                            threshold,
                                                                                            sharpe)
                        save_path = os.path.join(root_path, result_path, 'data', file_name[:-4])
                        if not os.path.isdir(save_path):
                            os.makedirs(save_path)
                        stock_price.to_csv(os.path.join(save_path, save_file_name))

    return 0


def process_list(split):
    for i in split:
        sma_trading_strategy(i)

    return 0


if __name__ == '__main__':
    process_num = 10
    pool = pathos.multiprocessing.ProcessingPool(process_num)
    split_list = np.array_split(stock_list, process_num)
    pool.map(process_list, split_list)
