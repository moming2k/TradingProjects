#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: query_us_place_information
# Author: Mark Wang
# Date: 25/7/2016

import os
import math
import sys
import logging

import pandas as pd
from vincenty import vincenty

from ..util import *
from pleace_nearby import PlaceNearby

us_west_lng = -124.848974
us_east_lng = -66.885444
us_north_lat = 49.384358
us_south_lat = 24.396308

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')
logger = logging.getLogger(os.uname()[0])

# us_west_lng = -73.95
# us_east_lng = -73.9
# us_north_lat = 40.71
# us_south_lat = 40.66


def save_df(save_path, df_to_save):
    if df_to_save.empty:
        logger.warn('empty df, nothing to save')
        return
    elif os.path.isfile(save_path):
        logger.info('File already exits, load previous file first')
        df = pd.read_csv(save_path)
        df_to_save = pd.concat([df, save_path], axis=0, ignore_index=True).drop_duplicates(['place_id'])
    df_to_save.to_csv(save_path, encoding='utf8')


def query_information_from_google_maps(query_type='church', country_code='usa', file_name=None, boundary=None,
                                       save_path='.', radius=5000.0):
    if file_name is None:
        file_name = "{}_{}_info".format(country_code, query_type)

    logger.info('Country code is {}, query type is {}'.format(country_code, query_type))

    # query = PlaceNearby('AIzaSyAgjJTaPvtfaWYK9WDggkvHZkNq1X3mM7Y') # wangyouan3
    # query = PlaceNearby('AIzaSyD517iPlsqV3MXoXBm_WPfB1rjKf55l6MY') # wangyouan6
    if os.uname()[0] == 'Darwin':
        logger.info('Current computer is your mac, ues key 6')
        query = PlaceNearby(key='AIzaSyBXa08GfK8XERZ-BKxVzDzIVALIN3Ov93c')
    elif os.uname()[1] == 'ewin3011':
        logger.info('Current computer is Prof. Wang, use key 3')
        query = PlaceNearby(key='AIzaSyAgjJTaPvtfaWYK9WDggkvHZkNq1X3mM7Y')
    else:
        logger.info('Other computer, use key6')
        query = PlaceNearby(key='AIzaSyD517iPlsqV3MXoXBm_WPfB1rjKf55l6MY')

    if boundary is None:
        north_lat = us_north_lat
        south_lat = us_south_lat
        east_lng = us_east_lng
        west_lng = us_west_lng
    elif isinstance(boundary, dict):
        north_lat = boundary['north']
        south_lat = boundary['south']
        east_lng = boundary['east']
        west_lng = boundary['west']
    elif isinstance(boundary, dict) and len(boundary) == 4:
        north_lat = boundary[0]
        south_lat = boundary[1]
        west_lng = boundary[2]
        east_lng = boundary[3]
    else:
        logger.error('boundary {} cannot be recognized'.format(boundary))
        raise ValueError('boundary {} cannot be recognized'.format(boundary))

    lat_partition_number = max(int(vincenty((north_lat, west_lng), (south_lat, west_lng)) /
                                   (math.sqrt(2) * float(radius) / 1000)) + 1, 2)
    lng_partition_number = max(int(vincenty((south_lat, west_lng), (south_lat, east_lng)) /
                                   (math.sqrt(2) * float(radius) / 1000)) + 1, 2)

    delta_lat = (north_lat - south_lat) / (lat_partition_number - 1)
    delta_lng = (east_lng - west_lng) / (lng_partition_number - 1)

    radius = max(vincenty((north_lat, west_lng), (south_lat, west_lng)) / (lat_partition_number - 1),
                 vincenty((south_lat, west_lng), (south_lat, east_lng)) / (lng_partition_number - 1)) \
             * 1000 / math.sqrt(2)

    logger.info(
        'Actual query radius is {:.2f}, lat_partitions is {}, lng_partitions is {}'.format(radius, lat_partition_number,
                                                                                           lng_partition_number))

    save_file = os.path.join(save_path, '{}.csv'.format(file_name))

    logger.info('Create an empty data frame to store information')
    df = pd.DataFrame(
        columns=['name', 'address', 'zip_code', 'state', 'phone_number', 'lat', 'lng', 'website', 'place_id'])

    index = 0
    max_fault_time = 10
    for j in range(lng_partition_number):
        for i in range(lat_partition_number):
            location = (south_lat + i * delta_lat, west_lng + j * delta_lng)
            try:
                if i % 50 == 0:
                    logger.info("Current location is {}".format(location))
                if not is_geocode_in_target_country(location, 'usa'):
                    continue

                place_id_df = query.radar_search(location=location, radius=radius, query_type='hospital')
                if place_id_df.empty:
                    continue
                for place_id in place_id_df['place_id']:
                    time.sleep(1)
                    result = query.place_detail(place_id)
                    # print result
                    df.loc[index] = result
                    index += 1

                if index > 10000:
                    logger.info('Current df size is larger than 10000, save it first')
                    save_df(save_file, df)
                    index = 0
                    df = pd.DataFrame(
                        columns=['name', 'address', 'zip_code', 'state', 'phone_number', 'lat', 'lng', 'website',
                                 'place_id'])
            except Exception:
                traceback.print_exc()
                max_fault_time -= 1
                logger.warn('location {} has exception, left permit fail time is {}'.format(str(location),
                                                                                            max_fault_time))
                if max_fault_time < 0:
                    break

    save_df(save_file, df)

    logger.info('Test finished')
    #
    # msg_body = "Your project finished, the below is the machine information\n{}".format('\n'.join(os.uname()))
    # send_email_through_gmail('Test finished', msg_body, to_addr='markwang@connect.hku.hk')
