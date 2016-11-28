#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: functions
# Author: Mark Wang
# Date: 25/11/2016

import datetime
from dateutil.relativedelta import relativedelta

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def calculate_strategy_performance(stock_price, long_position, short_position, start_cash, transaction_cost, delay,
                                   long_stock=0, short_stock=0):
    cash_list = [start_cash] * delay
    stock_long = [long_stock] * delay
    stock_short = [short_stock] * delay
    start_wealth = start_cash + long_stock + short_stock
    wealth = [start_wealth] * stock_price.shape[0]
    pnl = [0] * stock_price.shape[0]

    long_transaction = 0
    short_transaction = 0
    for i in range(delay, stock_price.shape[0]):
        if long_position[i] == 1 and cash_list[-1] > 0:
            stock_long.append(cash_list[i - 1] * (1 - transaction_cost))
            stock_short.append(stock_short[-1])
            cash_list.append(0)

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

        elif short_position[i] == 1 and cash_list[-1] > 0:
            stock_short.append(cash_list[-1] * (1 - transaction_cost))
            stock_long.append(stock_long[-1])
            cash_list.append(0)

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
        sharpe = np.mean(pnl[delay:]) / np.std(pnl[delay:])

    return wealth, sharpe, stock_long, stock_short, cash_list, pnl


def format_decimal(decimal_num):
    if abs(decimal_num) > 0.1:
        return '{:.2f}'.format(decimal_num)
    elif abs(decimal_num) < 1e-8:
        return '0'
    else:
        return '{:.2e}'.format(decimal_num)


def format_pnl(pnl):
    return '{:.2f}%'.format(pnl * 100)


def plot_output_data(df, sharpe, save_path, title):
    # get some information
    wealth5 = df['wealth'].shift(5)
    pnl5 = df['wealth'] / wealth5 - 1

    date_index = map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'), df.index)

    delta = relativedelta(date_index[-1], date_index[0])
    years_between = delta.years + float(delta.months) / 12
    buy_hold = (df.close[-1] / df.close[0] - 1) / years_between * 100
    daily_trade_frequency = format_decimal(df[df.operation != 0].shape[0] / float(df.shape[0]))

    pnl_max = format_pnl(df.pnl.max())
    pnl_min = format_pnl(df.pnl.min())
    pnl_mean = format_pnl(df.pnl.mean())
    pnl_25 = format_pnl(df.pnl.describe()['25%'])
    pnl_50 = format_pnl(df.pnl.describe()['50%'])
    pnl_75 = format_pnl(df.pnl.describe()['75%'])

    text = 'Sharpe: {}, Annualized Return: {:.2f}%'.format(format_decimal(sharpe), df.pnl.mean() * 247 * 100)
    text = '{}\nBuy-and-hold annualized return: {:.2f}%, Daily trades: {}'.format(text, buy_hold,
                                                                                     daily_trade_frequency)
    text = '{}\nPnL 1, max: {}, min: {}, mean: {}, [.25, .5, .75]: [{}, {}, {}]'.format(text, pnl_max, pnl_min,
                                                                                        pnl_mean, pnl_25, pnl_50,
                                                                                        pnl_75)

    pnl_max = format_pnl(pnl5.max())
    pnl_min = format_pnl(pnl5.min())
    pnl_mean = format_pnl(pnl5.mean())
    pnl_25 = format_pnl(pnl5.describe()['25%'])
    pnl_50 = format_pnl(pnl5.describe()['50%'])
    pnl_75 = format_pnl(pnl5.describe()['75%'])
    text = '{}\nPnL 5, max: {}, min: {}, mean: {}, [.25, .5, .75]: [{}, {}, {}]'.format(text, pnl_max, pnl_min,
                                                                                        pnl_mean, pnl_25, pnl_50,
                                                                                        pnl_75)

    # fig, ax = plt.subplots()
    fig = plt.figure()

    left = 0.1
    bottom = 0.3
    width = 0.75
    height = 0.60
    ax = fig.add_axes([left, bottom, width, height])
    ax.set_title(title)
    # ax.subplots_adjust(left=0.5, bottom=0.5, right=1, top=1, wspace=0, hspace=0)

    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    yearsFmt = mdates.DateFormatter('%Y')

    ln1 = ax.plot(date_index, df['close'], 'b-', label='Stock Price')
    ax.set_ylabel('Stock Price')
    ax.set_xlabel('Date')

    ax2 = ax.twinx()
    ln2 = ax2.plot(date_index, df.wealth, 'r-', label='Wealth')
    ax2.set_ylabel('Wealth')

    lns = ln1 + ln2
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=0)

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)
    # ax.legend(loc=0)
    plt.figtext(0.01, 0.01, text, horizontalalignment='left')
    # plt.tight_layout()

    fig.autofmt_xdate()

    fig.savefig(save_path)
    plt.close()


if __name__ == '__main__':
    import pandas as pd
    import os

    file_path = '/Users/warn/Documents/RAForWangZG/HKStockPrice/result/p1_14_p2_30_p3_15_th_2.1_sharpe_0.0444.csv'
    output_path = '/Users/warn/PycharmProjects/QuestionFromProfWang/StockPrice/TradingStrategy/grapth'
    input_df = pd.read_csv(file_path, index_col=0, skiprows=31,
                           names=['open', 'high', 'low', 'Close', 'volume', 'close', 'wealth', 'short', 'long', 'cash',
                                  'pnl', 'long_pos', 'short_pos', 'operation']
                           )

    plot_output_data(input_df, 0.0444, os.path.join(output_path, 'test.png'), title='0027.HK')
