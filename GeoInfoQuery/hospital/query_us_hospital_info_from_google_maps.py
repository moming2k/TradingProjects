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
# us_west_lng = -73.905
# us_east_lng = -73.9
# us_north_lat = 40.665
# us_south_lat = 40.66
# lng_partition_number = 2
# lat_partition_number = 2

save_file_name = "usa_hospital_information"
save_path = "~/Projects/QuestionFromProfWang/GeoInfoQuery/hospital"
columns = {'name', 'address', 'zip_code', 'state', 'phone_number', 'lat', 'lng', 'website', 'place_id'}

# query = PlaceNearby('AIzaSyAgjJTaPvtfaWYK9WDggkvHZkNq1X3mM7Y') # wangyouan3
# query = PlaceNearby('AIzaSyD517iPlsqV3MXoXBm_WPfB1rjKf55l6MY') # wangyouan6
if os.uname()[0] == 'Darwin':
    query = PlaceNearby(key='AIzaSyAgjJTaPvtfaWYK9WDggkvHZkNq1X3mM7Y')
elif os.uname()[1] == 'ewin3011':
    query = PlaceNearby(key='AIzaSyBXa08GfK8XERZ-BKxVzDzIVALIN3Ov93c')
else:
    query = PlaceNearby(key='AIzaSyD517iPlsqV3MXoXBm_WPfB1rjKf55l6MY')

delta_lat = (us_north_lat - us_south_lat) / (lat_partition_number - 1)
delta_lng = (us_east_lng - us_west_lng) / (lng_partition_number - 1)

radius = max(vincenty((us_north_lat, us_west_lng), (us_south_lat, us_west_lng)) / (lat_partition_number - 1),
             vincenty((us_south_lat, us_west_lng), (us_south_lat, us_east_lng)) / (lng_partition_number - 1)) \
         * 1000 / math.sqrt(2)

print radius

save_file = os.path.join(save_path, '{}.csv'.format(save_file_name))

if os.path.isfile(save_file):
    df = pd.read_csv(save_file)

else:
    df = pd.DataFrame(
        columns=['name', 'address', 'zip_code', 'state', 'phone_number', 'lat', 'lng', 'website', 'place_id'])

index = df.shape[0]
max_fault_time = 10
location = None
for j in range(lng_partition_number):
    for i in range(lat_partition_number):
        location = (us_south_lat + i * delta_lat, us_west_lng + j * delta_lng)
        try:
            if not is_geocode_in_target_country(location, 'usa'):
                continue
            if i % 50 == 0:
                print datetime.datetime.today(), location

            place_id_df = query.radar_search(location=location, radius=radius, query_type='hospital')
            if place_id_df.empty:
                continue
            for place_id in place_id_df['place_id']:
                time.sleep(1)
                result = query.place_detail(place_id)
                # print result
                keys = result.keys()
                for key in keys:
                    if key not in columns:
                        del result[key]

                df.loc[index] = result
                index += 1

            if i % 50 == 0:
                df = df.drop_duplicates(['place_id'])
                df.to_csv(save_file, encoding='utf8')
        except Exception:
            traceback.print_exc()
            print location
            max_fault_time -= 1
            if max_fault_time < 0:
                break

    print datetime.datetime.today(), location

df.drop_duplicates(['place_id']).to_csv(save_file, encoding='utf8')

msg_body = "Your project finished, the below is the machine information\n{}".format('\n'.join(os.uname()))
send_email_through_gmail('Test finished', msg_body, to_addr='markwang@connect.hku.hk')
