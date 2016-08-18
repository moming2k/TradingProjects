#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_real_info_compu_info_to_sdc_bloomberg
# Author: Mark Wang
# Date: 17/8/2016

from multiprocessing import Pool

import pathos

from add_info_to_wrong_ticker import *


def process_df(data_df):
    df = pd.concat([data_df, data_df.apply(add_real_price_volume_return_info, axis=1)], axis=1)
    df = add_wrong_ticker_price_volume_return_info(df)
    return df


if __name__ == '__main__':
    process_num = 15
    # pool = Pool(processes=process_num)
    pool = pathos.multiprocessing.ProcessingPool(process_num)

    print "Read SDC file from path"
    # bloomberg_df = pd.read_csv('result_csv/wrong_tickers_from_SDC_target_name.csv', index_col=0,
    #                      dtype={'cusip_real': str, 'cusip_wrong': str})
    #
    # print "Split file"
    # split_dfs = np.array_split(bloomberg_df, process_num)
    #
    # print "Split finished start to process files"
    # result_dfs = pool.map(process_bloomberg_df, split_dfs)
    # bloomberg_df = pd.concat(result_dfs, axis=0)
    # # bloomberg_df = process_bloomberg_df(bloomberg_df)
    #
    # print "Process finished, start to save file"
    # bloomberg_df.to_csv('result_csv/wrong_tickers_from_SDC_target_name.csv', encoding='utf8')
    #
    # del bloomberg_df

    add_original_file_info('result_csv/wrong_tickers_from_Bloomberg_large_ES.csv', 'Bloomberg',
                           dtype={'cusip_real': str, 'cusip_wrong': str, 'Ticker': str})
    # print "Read Bloomberg file from path"
    # bloomberg_dg = pd.read_csv('result_csv/wrong_tickers_from_Bloomberg_large_ES.csv', index_col=0,
    #                            dtype={'cusip_real': str, 'cusip_wrong': str, 'Ticker': str})
    #
    # print "Split file"
    # split_dfs = np.array_split(bloomberg_dg, process_num)
    # #
    # print "Split finished start to process files"
    # result_dfs = pool.map(process_bloomberg_df, split_dfs)
    # bloomberg_dg = pd.concat(result_dfs, axis=0)
    # # bloomberg_dg = process_bloomberg_df(bloomberg_dg)
    #
    # print "Process finished, start to save file"
    # bloomberg_dg.to_csv('result_csv/wrong_tickers_from_Bloomberg_large_ES.csv', encoding='utf8')
