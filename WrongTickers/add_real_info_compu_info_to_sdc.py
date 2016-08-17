#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_real_info_compu_info_to_sdc
# Author: Mark Wang
# Date: 17/8/2016

from multiprocessing import Pool

from add_info_to_wrong_ticker import *


def add_cusip_and_real_volume(row):
    today = row['DateToday']
    tomorrow = row['DateTomorrow']
    yesterday = row['DateYesterday']
    cusip = row['cusip']
    cusip_wrong = row['cusip_wrong']

    result = {}

    info_to_add = ['Price', 'LogReturn', 'SimpleReturn', 'PriceHigh', 'PriceLow']
    for info in info_to_add:
        for required_time in ['Today', 'Tomorrow', 'Yesterday']:
            if required_time == 'Today':
                column_name = info
            else:
                column_name = "{}{}".format(info, required_time)

            column_name = '{}_real'.format(column_name)

            result[column_name] = get_wrong_ticker_information_from_saved_file(row, info, required_time)
    try:
        result['PriceRange_real'] = result['PriceHigh_real'] - result['PriceLow_real']
    finally:
        result['PriceRange_real'] = np.nan
    try:
        result['PriceRangeTomorrow_real'] = result['PriceHighTomorrow_real'] - result['PriceLowTomorrow_real']
    finally:
        result['PriceRangeTomorrow_real'] = np.nan
    try:
        result['PriceRangeYesterday_real'] = result['PriceHighYesterday_real'] - result['PriceLowYesterday_real']
    finally:
        result['PriceRangeYesterday_real'] = np.nan

    result.update(get_comp_df_info(cusip, today, date_type='Today', data_type='real'))
    result.update(get_comp_df_info(cusip, yesterday, date_type='Yesterday', data_type='real'))
    result.update(get_comp_df_info(cusip, tomorrow, date_type='Tomorrow', data_type='real'))

    result.update(get_comp_df_info(cusip_wrong, today, date_type='Today', data_type='wrong'))
    result.update(get_comp_df_info(cusip_wrong, yesterday, date_type='Yesterday', data_type='wrong'))
    result.update(get_comp_df_info(cusip_wrong, tomorrow, date_type='Tomorrow', data_type='wrong'))

    vol = get_prior_one_year_volume(today, cusip)
    vol_wrong = get_prior_one_year_volume(today, cusip_wrong)
    result['PriorVolSum_real'] = vol[0]
    result['PriorVolStd_real'] = vol[1]
    result['PriorVolSum_wrong'] = vol_wrong[1]
    result['PriorVolStd_wrong'] = vol_wrong[1]
    return pd.Series(result)


def process_df(data_df):
    return pd.concat([data_df, data_df.apply(add_cusip_and_real_volume, axis=1)], axis=1)


if __name__ == '__main__':
    process_num = 10
    pool = Pool(processes=process_num)

    print "Read SDC file from path"
    sdc_df = pd.read_csv('result_csv/wrong_tickers_from_SDC_target_name.csv', index_col=0)

    print "Split file"
    split_df = np.array_split(sdc_df, process_num)
    result_dfs = pool.map(process_df, split_df)
    sdc_df = pd.concat(result_dfs, axis=0)
    # sdc_df = process_df(sdc_df)
    sdc_df.to_csv('result_csv/wrong_tickers_from_SDC_target_name.csv', encoding='utf8')
