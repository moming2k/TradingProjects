#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: calculate_strategy_performance
# Author: Mark Wang
# Date: 24/11/2016

import numpy as np


def calculate_strategy_performance(stock_price, long_position, short_position, start_cash, transaction_cost, delay,
                                   long_stock=0, short_stock=0):
    cash_list = [start_cash] * delay
    stock_long = [long_stock] * delay
    stock_short = [short_stock] * delay
    start_wealth = start_cash + long_stock + short_stock
    wealth = [start_wealth] * stock_price.shape[0]
    pnl = [0] * stock_price.shape[0]

    # 1 for buy long 2 for sell long -1 for buy short -2 for sell short
    trade_operation = [0] * stock_price.shape[0]

    long_transaction = 0
    short_transaction = 0
    for i in range(delay, stock_price.shape[0]):
        if long_position[i] == 1 and cash_list[-1] > 0:
            stock_long.append(cash_list[i - 1] * (1 - transaction_cost))
            stock_short.append(stock_short[-1])
            cash_list.append(0)
            trade_operation[i] = 1

        elif long_position[i] != -1 and stock_long[-1] > 0:
            profit = stock_long[-1] * stock_price[i] / stock_price[i - 1]
            stock_long.append(profit)
            stock_short.append(stock_short[-1])
            cash_list.append(cash_list[-1])

        elif long_position[i] == -1 and stock_long[-1] > 0:
            profit = stock_long[-1] * (stock_price[i] / stock_price[i - 1])
            cash_list.append(profit)
            stock_long.append(0)
            stock_short.append(stock_short[-1])
            long_transaction += 1
            trade_operation[i] = 2

        elif short_position[i] == 1 and cash_list[-1] > 0:
            stock_short.append(cash_list[-1] * (1 - transaction_cost))
            stock_long.append(stock_long[-1])
            cash_list.append(0)
            trade_operation[i] = -1

        elif short_position != -1 and stock_short[-1] > 0:
            profit = stock_short[-1] * (1 - stock_price[i] / stock_price[i - 1])
            stock_short.append(stock_short[-1] + profit)
            stock_long.append(stock_long[-1])
            cash_list.append(cash_list[-1])

        elif short_position[i] == -1 and stock_short[-1] > 0:
            profit = stock_short[-1] * (1 - stock_price[i] / stock_price[i - 1])
            cash_list.append(stock_short[-1] + profit)
            stock_short.append(0)
            stock_long.append(stock_long[-1])
            short_transaction += 1
            trade_operation[i] = -2

        else:
            cash_list.append(cash_list[-1])
            stock_long.append(stock_long[-1])
            stock_short.append(stock_short[-1])

        wealth[i] = cash_list[-1] + stock_long[-1] + stock_short[-1]
        pnl[i] = wealth[i] / wealth[i - 1] - 1

    std_result = np.std(pnl[delay:])
    if std_result < 0.01:
        sharpe = np.nan
    else:
        sharpe = np.mean(pnl[delay:]) / np.std(pnl[delay:]) * np.sqrt(247)

    return wealth, sharpe, stock_long, stock_short, cash_list, pnl, trade_operation
