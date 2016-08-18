#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_all_require_info
# Author: Mark Wang
# Date: 18/8/2016

""" Include Volume, Price, High, Low, Price Range, Compustat Info, IBES Info """

import os
import datetime

import pandas as pd
import numpy as np
import pathos.multiprocessing as multitask

from constants import *

DATA_PATH = 'Stock_data'


def get_vol_price_information_from_saved_file(row_info, data_type=WRONG, info_type=VOLUME):
    if data_type.lower() == WRONG:
        ticker = row_info[TICKER_WRONG]
        cusip = row_info[CUSIP_WRONG]
    else:
        ticker = row_info[TICKER_REAL]
        cusip = row_info[CUSIP_REAL]

    date_today = ''.join(row_info[DATE_TODAY].split('-'))
    date_tomorrow = ''.join(row_info[DATE_TOMORROW].split('-'))
    date_yesterday = ''.join(row_info[DATE_YESTERDAY].split('-'))
    information_result = {}
    if info_type == VOLUME:
        cus_path = os.path.join(DATA_PATH, 'volume_cusip', '{}_VOL.csv'.format(cusip))
        tic_path = os.path.join(DATA_PATH, 'volume', '{}_VOL.csv'.format(ticker))
        if os.path.isfile(cus_path):
            path = cus_path
        elif os.path.isfile(tic_path):
            path = tic_path
        else:
            information_result = {
                'Volume_{}'.format(data_type): np.nan,
                'VolumeTomorrow_{}'.format(data_type): np.nan,
                'VolumeYesterday_{}'.format(data_type): np.nan,
                'PriorVolSum_{}'.format(data_type): np.nan,
            }
            path = None

        if path is not None:
            df = pd.read_csv(path, usecols=['date', 'VOL'], dtype={'date': str, 'VOL': str})
            info_df = df[df['date'] == date_today]
            if info_df.empty:
                information_result['Volume_{}'.format(data_type)] = np.nan
            else:
                try:
                    information_result['Volume_{}'.format(data_type)] = int(info_df.ix[info_df.index[0], 'VOL'])
                except Exception, err:
                    information_result['Volume_{}'.format(data_type)] = np.nan

            info_df = df[df['date'] == date_tomorrow]
            if info_df.empty:
                information_result['VolumeTomorrow_{}'.format(data_type)] = np.nan
            else:
                try:
                    information_result['VolumeTomorrow_{}'.format(data_type)] = int(info_df.ix[info_df.index[0], 'VOL'])
                except Exception, err:
                    information_result['VolumeTomorrow_{}'.format(data_type)] = np.nan

            info_df = df[df['date'] == date_yesterday]
            if info_df.empty:
                information_result['VolumeYesterday_{}'.format(data_type)] = np.nan
            else:
                try:
                    information_result['VolumeYesterday_{}'.format(data_type)] = int(
                        info_df.ix[info_df.index[0], 'VOL'])
                except Exception, err:
                    information_result['VolumeYesterday_{}'.format(data_type)] = np.nan

            # Add prior one year date
            df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y%m%d'))
            current_date = datetime.datetime.strptime(row_info[DATE_TODAY], '%Y-%m-%d')
            df = df[df.date < current_date].tail(252)
            if df.empty:
                information_result['PriorVolSum_{}'.format(data_type)] = np.nan
            else:
                information_result['PriorVolSum_{}'.format(data_type)] = df['VOL'].sum()

    elif info_type in {PRICE, LOG_RETURN, SIMPLE_RETURN, PRICE_LOW, PRICE_HIGH}:
        if info_type in {PRICE, LOG_RETURN, SIMPLE_RETURN}:
            tic_path = os.path.join(DATA_PATH, "{}{}".format(info_type[0].lower(), info_type[1:]),
                                    '{}_{}.csv'.format(ticker, required_value_dict[info_type]))
            cus_path = os.path.join(DATA_PATH, "{}{}_cusip".format(info_type[0].lower(), info_type[1:]),
                                    '{}_{}.csv'.format(cusip, required_value_dict[info_type]))
        else:
            cus_path = os.path.join(DATA_PATH, "highlow_cusip", '{}_HL.csv'.format(cusip))
            tic_path = os.path.join(DATA_PATH, "highlow", '{}_HL.csv'.format(ticker))

        information_result = {"{}_{}".format(info_type, data_type): np.nan,
                              "{}Tomorrow_{}".format(info_type, data_type): np.nan,
                              "{}Yesterday_{}".format(info_type, data_type): np.nan,
                              }
        if os.path.isfile(cus_path):
            path = cus_path
        elif os.path.isfile(tic_path):
            path = tic_path
        else:
            path = None
        if path is not None:
            df = pd.read_csv(path, usecols=['date', required_value_dict[info_type]], dtype={'date': str})
            info_df = df[df['date'] == date_today]
            if not info_df.empty:
                try:
                    information_result["{}_{}".format(info_type, data_type)] = info_df.ix[
                        info_df.index[0], required_value_dict[info_type]]
                except Exception:
                    information_result["{}_{}".format(info_type, data_type)] = np.nan

            info_df = df[df['date'] == date_tomorrow]
            if not info_df.empty:
                try:
                    information_result["{}Tomorrow_{}".format(info_type, data_type)] = info_df.ix[
                        info_df.index[0], required_value_dict[info_type]]
                except Exception:
                    information_result["{}Tomorrow_{}".format(info_type, data_type)] = np.nan

            info_df = df[df['date'] == date_yesterday]
            if not info_df.empty:
                try:
                    information_result["{}Yesterday_{}".format(info_type, data_type)] = info_df.ix[
                        info_df.index[0], required_value_dict[info_type]]
                except Exception:
                    information_result["{}Yesterday_{}".format(info_type, data_type)] = np.nan

    return information_result


def get_comp_df_info(cusip, date_today, date_tomorrow, date_yesterday, data_type=REAL):
    df_path = os.path.join(DATA_PATH, 'Compustat_cusip', '{}_COMPU.csv'.format(cusip))
    if not os.path.isfile(df_path):
        data_df = None
    else:
        data_df = pd.read_csv(df_path, dtype={'cusip': str, 'iid': str, 'datadate': str})

    def read_info_from_df(date, date_type):
        if date_type == TODAY:
            pad = '_{}'.format(data_type)
        else:
            pad = '{}_{}'.format(date_type, data_type)
        if data_df is None:
            return {
                'gvkey{}'.format(pad): np.nan,
                'iid{}'.format(pad): np.nan,
                'divd{}'.format(pad): np.nan,
                'cshoc{}'.format(pad): np.nan,
                'eps{}'.format(pad): np.nan,
                'trfd{}'.format(pad): np.nan,
                'exchg{}'.format(pad): np.nan,
            }
        date = ''.join(date.split('-'))
        df = data_df[data_df['datadate'] == date]
        if df.empty:
            return {
                'gvkey{}'.format(pad): np.nan,
                'iid{}'.format(pad): np.nan,
                'divd{}'.format(pad): np.nan,
                'cshoc{}'.format(pad): np.nan,
                'eps{}'.format(pad): np.nan,
                'trfd{}'.format(pad): np.nan,
                'exchg{}'.format(pad): np.nan,
            }
        else:
            index = df.index[0]
            return {
                'gvkey{}'.format(pad): df.ix[index, 'gvkey'],
                'iid{}'.format(pad): df.ix[index, 'iid'],
                'divd{}'.format(pad): df.ix[index, 'divd'],
                'cshoc{}'.format(pad): df.ix[index, 'cshoc'],
                'eps{}'.format(pad): df.ix[index, 'eps'],
                'trfd{}'.format(pad): df.ix[index, 'trfd'],
                'exchg{}'.format(pad): df.ix[index, 'exchg'],
            }

    result = {}
    result.update(read_info_from_df(date_today, TODAY))
    result.update(read_info_from_df(date_tomorrow, TOMORROW))
    result.update(read_info_from_df(date_yesterday, YESTERDAY))
    return result


def get_ibes_info(cusip, ticker, detail_date):
    cus_path = os.path.join(DATA_PATH, 'ibes_cusip', '{}_IBES.csv'.format(cusip))
    tic_path = os.path.join(DATA_PATH, 'ibes', '{}_IBES.csv'.format(ticker))
    result = {'IBESNumber': 0,
              'IBESValueAvg': np.nan,
              'IBESValueStd': np.nan,
              'IBESValueMedian': np.nan,
              'IBESValueHigh': np.nan,
              'IBESValueLow': np.nan,
              }
    if os.path.isfile(cus_path):
        df = pd.read_csv(cus_path, usecols=['VALUE', 'FPEDATS'], dtype={'FPEDATS': str})
    elif os.path.isfile(tic_path):
        df = pd.read_csv(tic_path, usecols=['VALUE', 'FPEDATS'], dtype={'FPEDATS': str})
    else:
        return result

    df['date'] = df['FPEDATS'].apply(lambda x: x[:4])
    year = detail_date[:4]
    same_year = df[df['date'] == year]
    if not same_year.empty:
        result['IBESNumber'] = same_year.shape[0]
        result['IBESValueAvg'] = same_year['VALUE'].mean()
        result['IBESValueStd'] = same_year['VALUE'].std()
        result['IBESValueMedian'] = same_year['VALUE'].median()
        result['IBESValueHigh'] = same_year['VALUE'].max()
        result['IBESValueLow'] = same_year['VALUE'].min()
    return result


def generate_missing_info(row):
    missing_info = {}
    for info in [PRICE_HIGH, PRICE_LOW, PRICE, VOLUME, LOG_RETURN, SIMPLE_RETURN]:
        for data_type in [WRONG, REAL]:
            missing_info.update(get_vol_price_information_from_saved_file(row, data_type, info))

    missing_info.update(
        get_comp_df_info(row[CUSIP_REAL], row[DATE_TODAY], row[DATE_TOMORROW], row[DATE_YESTERDAY], REAL))
    missing_info.update(
        get_comp_df_info(row[CUSIP_REAL], row[DATE_TODAY], row[DATE_TOMORROW], row[DATE_YESTERDAY], WRONG))

    real_ibes = get_ibes_info(row[CUSIP_REAL], row[TICKER_REAL], row[DATE_TODAY])
    wrong_ibes = get_ibes_info(row[CUSIP_WRONG], row[TICKER_WRONG], row[DATE_TODAY])
    for key in real_ibes:
        missing_info['{}_{}'.format(key, REAL)] = real_ibes[key]
    for key in wrong_ibes:
        missing_info['{}_{}'.format(key, WRONG)] = real_ibes[key]

    return pd.Series(missing_info)


def process_df(df):
    new_df = df.apply(generate_missing_info, axis=1)
    new_df["{}_{}".format(PRICE_RANGE, REAL)] = new_df["{}_{}".format(PRICE_HIGH, REAL)] - \
                                                new_df["{}_{}".format(PRICE_LOW, REAL)]
    new_df["{}_{}".format(PRICE_RANGE, WRONG)] = new_df["{}_{}".format(PRICE_HIGH, WRONG)] - \
                                                 new_df["{}_{}".format(PRICE_LOW, WRONG)]
    new_df["IBESValueRange_{}".format(REAL)] = new_df["IBESValueHigh_{}".format(REAL)] - \
                                               new_df["IBESValueLow_{}".format(REAL)]
    new_df["IBESValueRange_{}".format(WRONG)] = new_df["IBESValueHigh_{}".format(WRONG)] - \
                                                new_df["IBESValueLow_{}".format(WRONG)]
    return new_df


if __name__ == '__main__':
    process_num = 16
    pool = multitask.ProcessingPool(process_num)
    file_path = 'result_csv/wrong_tickers_from_Bloomberg_large_ES_sample.csv'

    print "Read file"
    ori_df = pd.read_csv(file_path, dtype={CUSIP_REAL: str, CUSIP_WRONG: str})
    split_dfs = np.array_split(ori_df, process_num)
    result_dfs = pool.map(process_df, split_dfs)
    result_df = pd.concat(result_dfs, axis=0)
    result_df = pd.concat([ori_df, result_dfs], axis=1)
    result_df.to_csv(file_path, encoding='utf8')
