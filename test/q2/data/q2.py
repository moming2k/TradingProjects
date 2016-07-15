#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: q2
# Author: Mark Wang
# Date: 3/7/2016

import pandas
import numpy as np

from util import get_location_distance, get_business_address

if __name__ == "__main__":
    df = pandas.read_excel('coname_addresses.xlsx')
    location_list = []

    keys = df.keys()

    lat_list = np.zeros(df.index.max() + 1).astype(np.float)
    lng_list = np.zeros(df.index.max() + 1).astype(np.float)
    distance_list = np.zeros(df.index.max() + 1).astype(np.float)

    # used
    modify_list = []
    for index, row in df.iterrows():
        if not isinstance(df.get_value(index, keys[1]), str) and not isinstance(df.get_value(index, keys[1]), unicode):
            new_address = get_business_address(df.get_value(index, keys[0]))
            modify_list.append((index, new_address))
            row = {keys[0]: df.get_value(index, keys[0]),
                   keys[1]: new_address}
        lat_list[index], lng_list[index], distance_list[index] = get_location_distance(row, keys)

    # add address to those company who does not have an address
    for info in modify_list:
        df.set_value(info[0], keys[1], info[1])

    df['lat'] = pandas.Series(data=lat_list[df.index], index=df.index)
    df['lng'] = pandas.Series(data=lng_list[df.index], index=df.index)
    df['distance'] = pandas.Series(data=distance_list[df.index], index=df.index)

    df.to_excel('output.xlsx')
