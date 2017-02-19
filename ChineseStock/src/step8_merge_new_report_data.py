#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step8_merge_new_report_data
# @Date: 2017-02-05
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from ChineseStock.src.constants.path_info import buy_only_report_data_path, report_20170205_path, report_20170214_path
from constants import Constant as const

report_path = report_20170205_path
ticker_sep_report_path = os.path.join(report_path, 'ticker_sep')

# start_time = datetime.datetime(2013, 7, 22)
# end_time = datetime.datetime(2016, 7, 20)

# Sort cd_dividend info
cd_report_df = pd.read_excel(os.path.join(report_path, 'CD_Dividend.xlsx'))
cd_df = cd_report_df.drop([0, 1])
# cd_df = cd_df[cd_df.Ppdadt >= start_time]
# cd_df = cd_df[cd_df.Ppdadt <= end_time]

cd_result_df = pd.DataFrame(index=cd_df.index)

cd_result_df[const.REPORT_ANNOUNCE_DATE] = cd_df.Ppdadt
cd_result_df[const.REPORT_MARKET_TICKER] = cd_df.Stkcd.apply(lambda x: '{:06d}'.format(x))
cd_result_df.loc[:, const.REPORT_TYPE] = 'CD_Dividend'
cd_result_df[const.REPORT_RELATIONSHIP] = cd_df.Ppcont
cd_result_df.to_pickle(os.path.join(report_20170214_path, 'sorted_cd_dividend.p'))
cd_result_df.to_csv(os.path.join(report_20170214_path, 'sorted_cd_dividend.csv'), encoding='utf8')

# Sort employee_ownership_plan info
own_report_df = pd.read_excel(os.path.join(report_path, 'employee_ownership_plan.xlsx'))
own_df = own_report_df.drop(0)

# own_df = own_df[own_df.plandate >= start_time]
# own_df = own_df[own_df.plandate <= end_time]

own_result_df = pd.DataFrame(index=cd_df.index)

own_result_df[const.REPORT_ANNOUNCE_DATE] = own_df.plandate
own_result_df[const.REPORT_MARKET_TICKER] = own_df.stkcd
own_result_df.loc[:, const.REPORT_TYPE] = own_df.stock_source
own_result_df[const.REPORT_RELATIONSHIP] = own_df.capital_source
own_result_df.to_pickle(os.path.join(report_20170214_path, 'sorted_own.p'))
own_result_df.to_csv(os.path.join(report_20170214_path, 'sorted_own.csv'), encoding='utf8')

# Sort stock_issurance info
si_report_df = pd.read_excel(os.path.join(report_20170205_path, 'stock_issurance.xlsx'))
si_df = si_report_df.drop(0)

# si_df = si_df[si_df.anndate >= start_time]
# si_df = si_df[si_df.anndate <= end_time]

si_result_df = pd.DataFrame(index=cd_df.index)

si_result_df[const.REPORT_ANNOUNCE_DATE] = si_df.anndate
si_result_df[const.REPORT_MARKET_TICKER] = si_df.stkcd
si_result_df.loc[:, const.REPORT_TYPE] = 'stock issurance'
si_result_df[const.REPORT_RELATIONSHIP] = si_df.purpose
si_result_df.to_pickle(os.path.join(report_20170214_path, 'sorted_si.p'))
si_result_df.to_csv(os.path.join(report_20170214_path, 'sorted_si.csv'), encoding='utf8')

# Sort insider report information
insider_df_list = []
for file_name in os.listdir(buy_only_report_data_path):
    insider_df_list.append(pd.read_pickle(os.path.join(buy_only_report_data_path, file_name)))

insider_report_df = pd.concat(insider_df_list, axis=0, ignore_index=True)

insider_result_df = pd.DataFrame(index=insider_report_df.index)
insider_result_df[const.REPORT_ANNOUNCE_DATE] = insider_report_df.anndate
insider_result_df[const.REPORT_MARKET_TICKER] = insider_report_df.VAR1.apply(lambda x: x[:6])
insider_result_df.loc[:, const.REPORT_TYPE] = insider_report_df.type
insider_result_df[const.REPORT_RELATIONSHIP] = insider_report_df.relation
insider_result_df.to_pickle(os.path.join(report_20170214_path, 'sorted_insider.p'))
insider_result_df.to_csv(os.path.join(report_20170214_path, 'sorted_insider.csv'), encoding='utf8')

merged_report = pd.concat([insider_result_df, own_result_df, si_result_df, cd_result_df],
                          axis=0, ignore_index=True)
sorted_merged_df = merged_report.sort_values('anndate').dropna(subset=['anndate']).reset_index(drop=True)
sorted_merged_df.to_pickle(os.path.join(report_20170214_path, 'sorted_merged.p'))
# sorted_merged_df = sorted_merged_df[sorted_merged_df.anndate >= start_time]
# sorted_merged_df = sorted_merged_df[sorted_merged_df.anndate < end_time]

save_path = os.path.join(report_20170214_path, 'si_cd_own_insider')
merged_report_groups = sorted_merged_df.groupby('market_ticker')

for ticker in merged_report_groups.groups.keys():
    merged_report_groups.get_group(ticker).to_pickle(os.path.join(save_path, '{}.p'.format(ticker)))
