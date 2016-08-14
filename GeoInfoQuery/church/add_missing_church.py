#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_missing_church
# Author: Mark Wang
# Date: 14/8/2016

import os
import sys
import time
import logging

import pandas as pd

from ..google_maps.pleace_nearby import PlaceNearby

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logger = logging.getLogger('test')

path = '/'.join(__file__.split('/')[:-1])
query = PlaceNearby(key='AIzaSyAgjJTaPvtfaWYK9WDggkvHZkNq1X3mM7Y')


df = pd.read_csv(os.path.join(path, 'usa_church_info.csv'), index_col=0)
df2 = pd.read_csv(os.path.join(path, 'temp', 'us_church_information(whole).csv'), index_col=0)

df_place_id = set(df['place_id'])
df2_place_id = set(df2['place_id'])

diff = df2_place_id.difference(df_place_id)

index = max(df.index) + 1

for place_id in diff:
    try:
        result = query.place_detail(place_id)
        if result['country'] in {u'Mexico'}:
            continue
    except Exception, err:
        logger.warn(err)

    else:
        df.ix[index] = result
        index += 1

    finally:
        time.sleep(0.3)

df.to_csv(os.path.join(path, 'usa_church_info.csv'), encoding='utf8')
