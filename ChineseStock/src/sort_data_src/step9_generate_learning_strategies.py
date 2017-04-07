#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step9_generate_learning_strategies
# @Date: 2017-04-07
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime
import calendar
from dateutil.relativedelta import relativedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class Constant(object):
    # trading market type
    SHANGHAI_A = 1
    SHANGHAI_B = 2
    SHENZHEN_A = 4
    SHENZHEN_B = 8
    GEM = 16  # Growth Enterprises Market Board

    working_days = 251
    initial_wealth = 10000.0

    # Other information
    ALL = 'all'
    OVERWEIGHT = u'增持'
    REDUCTION = u'减持'
    SENIOR = u'高管'
    COMPANY = u'公司'
    DIRECTOR = u'董事'
    PERSON = u'个人'
    SUPERVISOR = u'监事'

    SPOUSE = u'配偶'
    SELF = u'本人'
    PARENTS = u'父母'
    FATHER = u'父亲'
    MOTHER = u'母亲'
    OTHERS = u'其他'
    BROTHERS = u'兄弟姐妹'
    OTHER_RELATIONS = u'其他关联'

    CONTROLLED_CORPORATION = u'受控法人'
    LISTED_COMPANY = u'上市公司'

    REPORT_TICKER = 'VAR1'
    REPORT_COMPANY_NAME = 'VAR2'
    REPORT_ANNOUNCE_DATE = 'anndate'
    REPORT_ACTION = 'VAR10'
    REPORT_RELATIONSHIP = 'relation'
    REPORT_TYPE = 'type'
    REPORT_CHANGER_NAME = 'name'
    REPORT_AVERAGE_PRICE = 'average_price'
    REPORT_REASON = 'reason'
    REPORT_POSITION = 'position'
    REPORT_CHANGE_NUMBER = 'number'

    REPORT_SELL_DATE = 'sell_date'
    REPORT_RETURN_RATE = 'return'
    REPORT_BUY_DATE = 'buy_date'
    REPORT_MARKET_TICKER = 'market_ticker'
    REPORT_MARKET_TYPE = 'market_type'
    REPORT_BUY_PRICE = 'buy_price'
    REPORT_BUY_TYPE = 'buy_type'
    REPORT_SELL_TYPE = 'sell_type'

    STOCK_TICKER = 'Stkcd'
    STOCK_DATE = 'Trddt'
    STOCK_OPEN_PRICE = 'Opnprc'
    STOCK_OPEN_PRICE2 = 'Opnprc2'
    STOCK_HIGH_PRICE = 'Hiprc'
    STOCK_LOW_PRICE = 'Loprc'
    STOCK_CLOSE_PRICE = 'Clsprc'
    STOCK_CLOSE_PRICE2 = 'Clsprc2'
    STOCK_VOLUME = 'Dnshrtrd'
    STOCK_MARKET_TYPE = 'Markettype'
    STOCK_ADJPRCWD = 'Adjprcwd'
    STOCK_ADJPRCND = 'Adjprcnd'

    HOLDING_DAYS = 'holding_days'
    PORTFOLIO_NUM = 'portfolio_num'
    STOPLOSS_RATE = 'stoploss_rate'
    INFO_TYPE = 'info_type'
    TRANSACTION_COST = 'transaction_cost'
    REPORT_RETURN_PATH = 'report_return_path'
    WEALTH_DATA_PATH = 'wealth_data_path'

    WEALTH_DATAFRAME = 'raw_strategy_df'
    RETURN_DATAFRAME = 'return_df'

    REPORT_PATH = 'report path'
    TRADING_SIGNAL_PATH = 'trading signal path'

    # report between this period would be neglected
    neglect_period = [datetime.datetime(2015, 7, 8), datetime.datetime(2016, 2, 1)]

    RUN_UP_DAY_X_LIST = [5, 10, 15, 20]
    RUN_UP_STOP_TRADE_RATE = range(3, 21)

    SAVE_TYPE_PICKLE = 'pickle'
    SAVE_TYPE_EXCEL = 'excel'
    SAVE_TYPE_CSV = 'csv'

    ALPHA_STRATEGY_LEGENDS = ['Raw Strategy', 'Beta Strategy', 'Alpha Strategy']

    BEST_RAW_SHARPE_RATIO = 'best_raw_sharpe_ratio'
    BEST_RAW_ANNUALIZED_RETURN = 'best_raw_ann_return'
    BEST_ALPHA_RETURN = 'best_alpha_return'
    BEST_ALPHA_SHARPE = 'best_alpha_sharpe'
    MINIMAL_ALPHA_DRAWDOWN = 'minimal_alpha_drawdown'
    MINIMAL_RAW_DRAWDOWN = 'minimal_raw_drawdown'
    PICTURE_PATH = 'pic_path'
    VALUE = 'value'

    SHARPE_RATIO = 'sharpe_ratio'
    ANNUALIZED_RETURN = 'ann_return'
    RETURN = 'return'

    RAW_STRATEGY = 'raw'
    ALPHA_STRATEGY = 'alpha'
    BETA_STRATEGY = 'beta'

    RUN_UP_RATE = 'run_up'
    RUN_UP_X = 'run_up_x'
    RUN_UP_Y = 'run_up_y'


const = Constant()


def generate_review_strategies(alpha_data, raw_data, base_df_type='alpha', review=6, forward=6):
    daily_alpha_return = alpha_data / alpha_data.shift(1) - 1
    daily_raw_return = raw_data / raw_data.shift(1) - 1

    date_index = alpha_data.index

    start_date = datetime.datetime(year=date_index[0].year, month=date_index[0].month, day=1)
    middle_date = start_date + relativedelta(months=review)
    end_date = start_date + relativedelta(months=(review + forward))

    if end_date > date_index[-1]:
        end_date = date_index[-1] + relativedelta(days=1)

    if base_df_type == 'alpha':
        base_df = daily_alpha_return

    else:
        base_df = daily_raw_return

    learning_alpha_series = pd.Series(index=date_index)
    learning_raw_series = pd.Series(index=date_index)

    while middle_date < date_index[-1]:
        trading_index = date_index[date_index >= start_date]
        trading_index = trading_index[trading_index < middle_date]

        filling_index = date_index[date_index < end_date]
        filling_index = filling_index[filling_index >= middle_date]

        sub_learning_strategy_name = base_df.loc[trading_index].mean().idxmax()

        learning_alpha_series.loc[filling_index] = daily_alpha_return.loc[filling_index, sub_learning_strategy_name]
        learning_raw_series.loc[filling_index] = daily_raw_return.loc[filling_index, sub_learning_strategy_name]

        middle_date = end_date
        start_date = middle_date - relativedelta(months=review)
        end_date = middle_date + relativedelta(months=forward)

        if end_date > date_index[-1]:
            end_date = date_index[-1] + relativedelta(days=1)

    learning_alpha_wealth = (learning_alpha_series.fillna(0) + 1).cumprod() * 10000
    learning_raw_wealth = (learning_raw_series.fillna(0) + 1).cumprod() * 10000

    return learning_alpha_wealth, learning_raw_wealth


def get_max_draw_down(data_series):
    max_wealth = data_series[0]
    draw_back_rate = float('-inf')

    for i in data_series[1:]:
        draw_back_rate = max(draw_back_rate, 1 - i / max_wealth)
        max_wealth = max(max_wealth, i)

    return draw_back_rate


def plot_multiline_alpha(data_list, legend_list, picture_title, picture_save_path, text1, text2):
    """ Draw data series info """

    # plot file and save picture
    fig = plt.figure(figsize=(15, 8))

    left = 0.1
    bottom = 0.3
    width = 0.75
    height = 0.60
    ax = fig.add_axes([left, bottom, width, height])
    ax.set_title(picture_title)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.figtext(0.01, 0.01, text1, horizontalalignment='left')
    plt.figtext(0.51, 0.01, text2, horizontalalignment='left')

    date_series = data_list[0].index

    color_list = ['r-', 'b-', 'y-', 'g-']

    for i, data_series in enumerate(data_list):
        # get data series info
        plt.plot(date_series, data_series, color_list[i], label=legend_list[i])

    min_date = date_series[0]
    max_date = date_series[-1]
    plt.gca().set_xlim(min_date, max_date)
    plt.legend(loc=0)
    fig.autofmt_xdate()
    # fig.suptitle(picture_title)

    # print dir(fig)
    fig.savefig(picture_save_path)
    plt.close()


def get_sharpe_ratio(df, df_type=None, working_days=None):
    """ Input should be return own_report_df """
    if df_type is None:
        df_type = const.RETURN_DATAFRAME

    if working_days is None:
        working_days = 252

    if df_type == const.RETURN_DATAFRAME:
        return df.mean() / df.std() * np.sqrt(working_days)

    elif df_type == const.WEALTH_DATAFRAME:
        return_df = (df - df.shift(1)) / df.shift(1)
        # return_df.loc[return_df.first_valid_index(), :] = 0.0
        return get_sharpe_ratio(return_df, df_type=const.RETURN_DATAFRAME, working_days=working_days)

    else:
        raise ValueError('Unknown dataframe type {}'.format(df_type))


def date_as_float(dt):
    size_of_day = 1. / 366.
    size_of_second = size_of_day / (24. * 60. * 60.)
    days_from_jan1 = dt - datetime.datetime(dt.year, 1, 1)
    if not calendar.isleap(dt.year) and days_from_jan1.days >= 31 + 28:
        days_from_jan1 += datetime.timedelta(1)
    return dt.year + days_from_jan1.days * size_of_day + days_from_jan1.seconds * size_of_second


def get_annualized_return(df, df_type=None):
    """ input should be wealth own_report_df """
    if df_type is None:
        df_type = const.WEALTH_DATAFRAME

    if df_type == const.WEALTH_DATAFRAME:
        start_date = df.first_valid_index()
        end_date = df.last_valid_index()
        return (df.ix[end_date] / df.ix[start_date]) ** (
            1 / (date_as_float(end_date) - date_as_float(start_date))) - 1

    elif df_type == const.RETURN_DATAFRAME:
        wealth_df = (df + 1).cumprod()
        return get_annualized_return(wealth_df, df_type=const.WEALTH_DATAFRAME)

    else:
        raise ValueError('Unknown dataframe type {}'.format(df_type))


def plot_multiline_picture_text(pic_title, data_list, legends, save_path, stop_loss_rate):
    line1 = 'Transaction cost 0.2% SR {}%'.format(stop_loss_rate)

    info_list = [line1]

    raw_strategy = data_list[0]
    alpha_strategy = data_list[1]

    time_period = ['all', '09_14', '13_16', 'after_16']
    period_list = [(None, None), (datetime.datetime(2009, 1, 1), datetime.datetime(2015, 1, 1)),
                   (datetime.datetime(2013, 7, 22), datetime.datetime(2016, 7, 20)),
                   (datetime.datetime(2016, 2, 1), None)]

    def generate_line_info(i, date_tuple):
        current_line = 'Date {}'.format(time_period[i])
        result_list = [current_line]

        def get_line_not_alpha(data_series, prefix_info):
            if date_tuple[0] is not None:
                sub_data_series = data_series[data_series.index > date_tuple[0]]
            else:
                sub_data_series = data_series

            if date_tuple[1] is not None:
                sub_data_series = sub_data_series[sub_data_series.index < date_tuple[1]]

            sharpe_ratio = get_sharpe_ratio(sub_data_series, df_type=const.WEALTH_DATAFRAME)
            ann_return = get_annualized_return(sub_data_series, df_type=const.WEALTH_DATAFRAME) * 100
            max_draw_down = get_max_draw_down(sub_data_series) * 100

            current_line = '{}: Sharpe Ratio {:.3f}, Annualized Return {:.2f}%, Max Drawdown rate {:.2f}%'.format(
                prefix_info, sharpe_ratio, ann_return, max_draw_down
            )
            return current_line

        for prefix in ['Raw', 'Alpha']:

            if prefix == 'Raw':
                result_list.append(get_line_not_alpha(raw_strategy, prefix))

            # elif prefix == 'Beta':
            #     result_list.append(get_line_not_alpha(beta_strategy, prefix))

            else:
                result_list.append(get_line_not_alpha(alpha_strategy, prefix))

        return result_list

    for i, date_tuple in enumerate(period_list[:2]):
        info_list.extend(generate_line_info(i, date_tuple))

    text1 = '\n'.join(info_list)

    info_list = []
    for i, date_tuple in enumerate(period_list[2:]):
        info_list.extend(generate_line_info(i + 2, date_tuple))

    text2 = '\n'.join(info_list)

    plot_multiline_alpha(data_list,
                         legend_list=legends,
                         picture_title=pic_title,
                         picture_save_path=save_path,
                         text1=text1, text2=text2)


if __name__ == '__main__':
    from xvfbwrapper import Xvfb

    vdisplay = Xvfb(1366, 768)
    vdisplay.start()

    result_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen/result'

    learning_result_path = os.path.join(result_path, 'forecast_learning_result')

    alpha_df = pd.read_pickle(os.path.join(learning_result_path, 'merged_forecast_alpha_drop_unuseful.p'))
    raw_df = pd.read_pickle(os.path.join(learning_result_path, 'merged_forecast_raw_drop_unuseful.p'))
    # transaction_cost = 0.002
    # max_draw_down_limit = float('inf')
    # suffix = 'insider_exe_gt2'
    # report_path = const.INSIDER_EXE_GT2_RUN_UP_PATH
    #
    # util = ReportGenerator(transaction_cost=transaction_cost, report_path=report_path,
    #                        folder_suffix=suffix, trading_days_list_path=const.TRADING_DAYS_20170228_PATH,
    #                        stock_price_path=const.STOCK_PRICE_20170214_PATH)

    # review = 6
    # forward = 6
    base_df_type = 'raw'

    go_over_list = []

    for r in range(1, 13):
        for f in range(1, r + 1):
            go_over_list.append((r, f))

    alpha_learning_df = pd.DataFrame(index=alpha_df.index)
    raw_learning_df = pd.DataFrame(index=raw_df.index)

    for review, forward in go_over_list:
        print(datetime.datetime.today(), review, forward)
        name = 'learning_r{}_f{}_{}'.format(review, forward, base_df_type)

        alpha_series, raw_series = generate_review_strategies(alpha_df, raw_df, base_df_type=base_df_type,
                                                              review=review, forward=forward)

        plot_multiline_picture_text(name, [raw_series, alpha_series],
                                    ['Raw Strategy', 'Alpha Strategy'],
                                    save_path=os.path.join(learning_result_path, '{}.png'.format(name)),
                                    stop_loss_rate='NaN')

        alpha_learning_df[name] = alpha_series
        raw_learning_df[name] = raw_series

    alpha_learning_df.to_pickle(os.path.join(learning_result_path, '20170407_alpha_learning.p'))
    raw_learning_df.to_pickle(os.path.join(learning_result_path, '20170407_raw_learning.p'))

    vdisplay.stop()
