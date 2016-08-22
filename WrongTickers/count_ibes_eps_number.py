#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: CountIBESFile
# Author: Mark Wang
# Date: 19/8/2016

import numpy as np
import pandas as pd
from pathos.multiprocessing import ProcessingPool

print "Read CSV"
df = pd.read_csv('Stock_data/IBES_detail_1970_2016.csv', usecols=['CUSIP', 'OFTIC', 'MEASURE', 'VALUE', 'FPEDATS'],
                 dtype={'CUSIP': str, 'FPEDATS': str})

print "Only keep EPS value"
df = df[df['MEASURE'] == 'EPS']
del df['MEASURE']


def process_cusip_group_index(cusip_group):
    count_list = []
    for index in cusip_group:
        sub_df = df.ix[index]
        cusip = df.ix[index[0], 'CUSIP']
        sub_df_group = sub_df.groupby('FPEDATS')
        for announce_date, date_df in sub_df_group:
            ticker = date_df['OFTIC'].dropna()
            if ticker.empty:
                ticker = ''
            else:
                ticker = ticker.values[0]
            info_dict = {'CUSIP': cusip,
                         'DATE': announce_date,
                         'Ticker': ticker,
                         'EPS_NUM': int(date_df.shape[0])}
            count_list.append(info_dict)

    return pd.DataFrame(count_list)


if __name__ == "__main__":
    print "initial process pool"
    process_num = 16
    pool = ProcessingPool(process_num)

    print "Split groups"
    split_groups = np.array_split(df.groupby(['CUSIP']).groups.values(), process_num)

    print "Process dfs"
    result_dfs = pool.map(process_cusip_group_index, split_groups)

    print "Generate result"
    pd.concat(result_dfs, axis=0, ignore_index=True).to_csv('result_csv/IBES_EPS_Count.csv', encoding='utf8',
                                                            index=False)
