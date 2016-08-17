#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_real_info_compu_info_to_sdc_bloomberg
# Author: Mark Wang
# Date: 17/8/2016

from multiprocessing import Pool

from add_info_to_wrong_ticker import *


def process_df(data_df):
    return pd.concat([data_df, data_df.apply(add_cusip_and_real_volume, axis=1)], axis=1)


if __name__ == '__main__':
    process_num = 10
    pool = Pool(processes=process_num)

    print "Read SDC file from path"
    sdc_df = pd.read_csv('result_csv/wrong_tickers_from_SDC_target_name.csv', index_col=0)

    print "Split file"
    split_df = np.array_split(sdc_df, process_num)

    print "Split finished start to process files"
    result_dfs = pool.map(process_df, split_df)
    sdc_df = pd.concat(result_dfs, axis=0)
    # sdc_df = process_df(sdc_df)

    print "Process finished, start to save file"
    sdc_df.to_csv('result_csv/wrong_tickers_from_SDC_target_name.csv', encoding='utf8')

    del sdc_df

    print "Read SDC file from path"
    bloomberg_dg = pd.read_csv('result_csv/wrong_tickers_from_Bloomberg_large_ES.csv', index_col=0)

    print "Split file"
    split_df = np.array_split(sdc_df, process_num)

    print "Split finished start to process files"
    result_dfs = pool.map(process_df, split_df)
    bloomberg_dg = pd.concat(result_dfs, axis=0)
    # sdc_df = process_df(sdc_df)

    print "Process finished, start to save file"
    bloomberg_dg.to_csv('result_csv/wrong_tickers_from_Bloomberg_large_ES.csv', encoding='utf8')
