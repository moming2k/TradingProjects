#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: query_church_info_from_google_maps
# Author: Mark Wang
# Date: 24/7/2016

import os
import math
import datetime

import pandas as pd
from vincenty import vincenty

from ..util import *
from ..google_maps.pleace_nearby import PlaceNearby

us_west_lng = -124.848974
us_east_lng = -66.885444
us_north_lat = 49.384358
us_south_lat = 24.396308
lng_partition_number = 833
lat_partition_number = 396

save_file_name = "usa_church_information"

query = PlaceNearby('AIzaSyAgjJTaPvtfaWYK9WDggkvHZkNq1X3mM7Y')

delta_lat = (us_north_lat - us_south_lat) / (lat_partition_number - 1)
delta_lng = (us_east_lng - us_west_lng) / (lng_partition_number - 1)

radius = max(vincenty((us_north_lat, us_west_lng), (us_south_lat, us_west_lng)) / (lat_partition_number - 1),
             vincenty((us_south_lat, us_west_lng), (us_south_lat, us_east_lng)) / (lng_partition_number - 1)) \
         * 1000 / math.sqrt(2)

if os.path.isfile('{}.csv'.format(save_file_name)):
    df = pd.read_csv('{}.csv'.format(save_file_name))

else:
    df = pd.DataFrame(
        columns=['name', 'address', 'zip_code', 'state', 'phone_number', 'lat', 'lng', 'website', 'place_id'])

index = df.shape[0]
for i in range(lat_partition_number):
    for j in range(lng_partition_number):
        location = (us_south_lat + i * delta_lat, us_west_lng + j * delta_lng)
        if not is_geocode_in_target_country(location, 'usa'):
            continue
        if j % 100 == 0:
            print datetime.datetime.today(), location

        place_id_df = query.radar_search(location=location, radius=radius, query_type='church')
        if place_id_df.empty:
            continue

        for place_id in place_id_df['place_id']:
            df.loc[index] = query.place_detail(place_id)
            index += 1

        if j % 100 == 0:
            df = df.drop_duplicates(['place_id']).reset_index()
            df.to_csv('{}.csv'.format(save_file_name))

df = df.drop_duplicates(['place_id']).reset_index()
df.to_csv('{}.csv'.format(save_file_name))

msg_body = "Your project finished, the below is the machine information\n{}".format('\n'.join(os.uname()))
send_email_through_gmail('Test finished', msg_body, to_addr='markwang@connect.hku.hk')
