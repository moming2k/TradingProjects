#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: q2_geocoder
# Author: Mark Wang
# Date: 4/7/2016

import numpy as np
import pandas

from util import get_business_address, get_location_distance_geocoder


if __name__ == "__main__":
    df = pandas.read_excel('coname_addresses.xlsx')
    df = df.sample(10)

    def check_nan(name):
        if isinstance(name, float):
            return np.isnan(name)
        elif isinstance(name, str) or isinstance(name, unicode):
            return len(name) == 0
        elif name:
            return False
        else:
            return True

    empty_address = df['address'].apply(check_nan)
    empty_address_index = empty_address[empty_address == True].index
    for index in empty_address_index:
        df.ix[index, 'address'] = get_business_address(df.get_value(index, 'CONAME'))

    geo_info = df['address'].apply(get_location_distance_geocoder)
    df = pandas.concat([df, geo_info['lat'], geo_info['lng'], geo_info['distance']], axis=1)

    df.to_excel('output_geocoder2.xlsx')
