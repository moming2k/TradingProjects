#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: split_volume
# Author: Mark Wang
# Date: 15/8/2016

import os
from multiprocessing import Pool

import pandas as pd
import numpy as np

path = 'Stock_data'

def process_split_group_highlow(group):
    for key, df in group:
        ticker = df.ix[df.index[0], 'TICKER']
        df.to_csv(os.path.join(path, 'highlow', '{}_HL.csv'.format(ticker)), index=False)

    return 1


def process_split_group_volume(group):
    for key, df in group:
        ticker = df.ix[df.index[0], 'TICKER']
        df = df.dropna(axis=0, how='any')
        df['VOL'] = df['VOL'].apply(int)
        df.to_csv(os.path.join(path, 'volume', '{}_VOL.csv'.format(ticker)), index=False)

    return 1


if __name__ == "__main__":
    process_num = 16
    pool = Pool(process_num)

    # print 'Start to handle price high low'
    # price_high_low_df = pd.read_csv('Stock_data/highlow.csv', dtype={'date': str},
    #                                 usecols=['date', 'BIDLO', 'ASKHI', 'TICKER'])
    # price_high_low_group = price_high_low_df.groupby('TICKER')
    # print 'Start to split groups'
    # split_group = np.array_split(price_high_low_group, process_num)
    # print "Use {} processors to do this part".format(process_num)
    # pool.map(process_split_group_highlow, split_group)

    print 'Start to handle volume'
    volume_df = pd.read_csv('Stock_data/Volume.csv', dtype={'date': str},
                                    usecols=['date', 'VOL', 'TICKER'])
    volume_group = volume_df.groupby('TICKER')
    print 'Start to split groups'
    split_group = np.array_split(volume_group, process_num)
    print "Use {} processors to do this part".format(process_num)
    pool.map(process_split_group_volume, split_group)
