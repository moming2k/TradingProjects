#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: plot_picture
# @Date: 2017-01-31
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_sub_date_picture(return_series, picture_title, picture_save_path, period=1):
    wealth_series = (return_series + 1).cumprod()
    date_series = return_series.index

    # plot file and save picture
    plt.clf()
    fig = plt.figure(figsize=(15, 6))

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.plot(date_series, wealth_series, 'r-')
    min_date = date_series[0]
    max_date = date_series[-1]
    plt.gca().set_xlim(min_date, max_date)
    fig.autofmt_xdate()
    fig.suptitle(picture_title)
    # plt.axvline(time_sep[period], color='b')
    # print dir(fig)
    fig.text(0.28, 0.6, 'In-sample', fontsize=15)
    fig.text(0.7, 0.4, 'Out-of-sample', fontsize=15)
    fig.savefig(picture_save_path)


def plot_output_data(df, sharpe, save_path, title):
    # get some information
    date_index = df.index

    text = '{}\nPnL 5, max: {}, min: {}, mean: {}, [.25, .5, .75]: [{}, {}, {}]'
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
