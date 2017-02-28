#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step22_sort_20170224_report
# @Date: 2017-02-24
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd

from constants.constants import Constant as const
from constants.path_info import Path

report_path = os.path.join(Path.REPORT_DATA_PATH, 'report_data_20170224')

# the following code are used to calculate forecast info
forecast_report_path = os.path.join(report_path, 'forecast_report')
forecast_df = pd.read_sas(os.path.join(report_path, 'forecast.sas7bdat'))

forecast_df['type'] = forecast_df['type'].apply(lambda x: x.decode('gbk'))
forecast_df = forecast_df[forecast_df['type'] == u'预增']

result_df = pd.DataFrame(index=forecast_df.index)

result_df[const.REPORT_MARKET_TICKER] = forecast_df['code'].apply(lambda x: x[:-3])
result_df[const.REPORT_ANNOUNCE_DATE] = forecast_df['forecastdate'].apply(
    lambda x: datetime.datetime(1960, 1, 1) + datetime.timedelta(days=int(x)))

result_df.loc[:, const.REPORT_TYPE] = 'preannouncement'
result_df.loc[:, const.REPORT_RELATIONSHIP] = u'预增'


def save_ticker_group(df):
    name = df.ix[df.first_valid_index(), const.REPORT_MARKET_TICKER]
    df.to_pickle(os.path.join(forecast_report_path, '{}.p'.format(name)))


result_df.groupby(const.REPORT_MARKET_TICKER).apply(save_ticker_group)

# the following code are used to calculate incentive info
incentive_path_info = os.path.join(report_path, 'incentives_report')
incentive_df = pd.read_excel(os.path.join(report_path, 'Incentives.xlsx')).drop([1413, 1414])

result_df = pd.DataFrame(index=incentive_df.index)

data_type = u'预案公告日'

result_df[const.REPORT_MARKET_TICKER] = incentive_df[u'代码'].apply(lambda x: x[:-3])
result_df[const.REPORT_ANNOUNCE_DATE] = incentive_df[data_type]

result_df.loc[:, const.REPORT_TYPE] = 'stock_incentives'
result_df.loc[:, const.REPORT_RELATIONSHIP] = data_type


def save_ticker_group(df):
    name = df.ix[df.first_valid_index(), const.REPORT_MARKET_TICKER]
    df.to_pickle(os.path.join(incentive_path_info, '{}.p'.format(name)))


result_df.groupby(const.REPORT_MARKET_TICKER).apply(save_ticker_group)

# generate_forecast_si_own_cd_insider mixed report
import shutil

si_own_cd_insider_path = os.path.join(Path.REPORT_DATA_PATH, 'report_data_20170214', 'si_cd_own_insider')
fsoci_report_path = os.path.join(report_path, 'fscioi_report')

si_own_cd_insider_list = os.listdir(si_own_cd_insider_path)
forecast_list = os.listdir(forecast_report_path)
incentive_list = os.listdir(incentive_path_info)

total_set = set(si_own_cd_insider_list).union(forecast_list).union(incentive_list)

for file_name in total_set:
    df_dict = {}

    if file_name in si_own_cd_insider_list:
        df_dict[si_own_cd_insider_path] = file_name

    if file_name in forecast_list:
        df_dict[forecast_report_path] = file_name

    if file_name in incentive_list:
        df_dict[incentive_path_info] = file_name

    if len(df_dict) == 1:
        origin_path = df_dict.keys()[0]
        shutil.copy(os.path.join(origin_path, file_name), os.path.join(fsoci_report_path, file_name))

    else:

        df_list = []

        for key in df_dict:
            df_list.append(pd.read_pickle(os.path.join(key, df_dict[key])))

        pd.concat(df_list, axis=0, ignore_index=True).to_pickle(os.path.join(fsoci_report_path, file_name))
