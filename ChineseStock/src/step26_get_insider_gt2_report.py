#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step26_get_insider_gt2_report
# @Date: 2017-02-28
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from constants import Constant as const
from constants.path_info import Path


def process_file_name(file_name):
    df = pd.read_pickle(os.path.join(Path.INSIDER_REPORT_PATH, file_name))
    df = df[[const.REPORT_TICKER, const.REPORT_ANNOUNCE_DATE, const.REPORT_RELATIONSHIP,
             const.REPORT_TYPE]]
    df = df[df[const.REPORT_TYPE] == const.SENIOR]

    df_group_count = df.groupby(const.REPORT_ANNOUNCE_DATE).count()
    result_df = pd.DataFrame(columns=[const.REPORT_MARKET_TICKER, const.REPORT_ANNOUNCE_DATE, const.REPORT_RELATIONSHIP,
                                      const.REPORT_TYPE])

    index = df_group_count[df_group_count[const.REPORT_TICKER] >= 2].index

    if len(index) == 0:
        return None

    row_num = 0
    for i in index:
        result_df.loc[row_num] = {const.REPORT_MARKET_TICKER: file_name[:6],
                                  const.REPORT_ANNOUNCE_DATE: i,
                                  const.REPORT_RELATIONSHIP: df_group_count.ix[i, const.REPORT_TICKER],
                                  const.REPORT_TYPE: const.SENIOR
                                  }
        row_num += 1

    if not result_df.empty:
        result_df.to_pickle(os.path.join(Path.INSIDER_EXE_GT2_PATH, '{}.p'.format(file_name[:6])))
    return 1


if __name__ == '__main__':
    import pathos

    file_list = os.listdir(Path.INSIDER_REPORT_PATH)
    pool = pathos.multiprocessing.ProcessingPool(18)

    pool.map(process_file_name, file_list)
