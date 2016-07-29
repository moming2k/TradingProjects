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
import re

import pandas as pd
from vincenty import vincenty

from GeoInfoQuery.util import *
from pleace_nearby import PlaceNearby
from google_map_spider import GoogleMapSpider

us_west_lng = -124.848974
us_east_lng = -66.885444
us_north_lat = 49.384358
us_south_lat = 24.396308

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')
logger = logging.getLogger(os.uname()[0])

columns = ['name', 'address', 'zip_code', 'city', 'state', 'country', 'phone_number', 'lat', 'lng', 'website',
           'place_id', 'url',
           'detail_type'
           ]

# us_west_lng = -74.75
# us_east_lng = -74.7
# us_north_lat = 40.71
# us_south_lat = 40.66

proxy = "117.135.250.71:80"

if os.uname()[0] == 'Darwin':
    logger.info('Current computer is your mac, ues key 6')
    query = PlaceNearby(key='AIzaSyBXa08GfK8XERZ-BKxVzDzIVALIN3Ov93c', proxy=proxy)
elif os.uname()[1] == 'ewin3011':
    logger.info('Current computer is Prof. Wang, use key 3')
    query = PlaceNearby(key='AIzaSyAgjJTaPvtfaWYK9WDggkvHZkNq1X3mM7Y', proxy=proxy)
else:
    logger.info('Other computer, use key6')
    query = PlaceNearby(key='AIzaSyD517iPlsqV3MXoXBm_WPfB1rjKf55l6MY', proxy=proxy)

country_dict = {'usa': 'United States'}


def save_df(save_path, df_to_save):
    if df_to_save.empty:
        logger.warn('empty df, nothing to save')
        return
    elif os.path.isfile(save_path):
        logger.info('File already exits, load previous file first')
        df = pd.read_csv(save_path, index_col=0)
        df_to_save = pd.concat([df, df_to_save], axis=0, ignore_index=True).drop_duplicates(['place_id']).reset_index(
            drop=True)
    df_to_save.to_csv(save_path, encoding='utf8')


def query_information_from_google_maps(query_type='church', country_code='usa', file_name=None, boundary=None,
                                       save_path='.', radius=5000.0):
    if file_name is None:
        file_name = "{}_{}_info".format(country_code, query_type)

    logger.info('Country code is {}, query type is {}'.format(country_code, query_type))

    # query = PlaceNearby('AIzaSyAgjJTaPvtfaWYK9WDggkvHZkNq1X3mM7Y') # wangyouan3
    # query = PlaceNearby('AIzaSyD517iPlsqV3MXoXBm_WPfB1rjKf55l6MY') # wangyouan6

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
    df = pd.DataFrame(columns=columns)

    index = 0
    failed_location = []
    if 'detail_type' in columns:
        spider = GoogleMapSpider(spider_type="mechanize")
        spider.start()
    else:
        spider = None

    percentage = 0

    for j in range(lng_partition_number):
        for i in range(lat_partition_number):
            location = (south_lat + i * delta_lat, west_lng + j * delta_lng)
            try:
                if i % 50 == 0:
                    logger.info("Current location is {}".format(location))
                if not is_geocode_in_target_country(location, 'usa'):
                    continue

                place_id_df = query.radar_search(location=location, radius=radius, query_type=query_type)
                if place_id_df.empty:
                    continue
                for place_id in place_id_df['place_id']:
                    time.sleep(0.5)

                    # If this place ID has been queried before, then there is no need to query it again
                    if not df[df['place_id'] == place_id].empty:
                        continue
                    result = query.place_detail(place_id)
                    if result['country'] != country_dict[country_code]:
                        logger.debug("Country {} not in target country".format(result['country']))
                        continue

                    if 'detail_type' in columns:
                        result['detail_type'] = spider.get_detail_type(result.get('url', None))
                        if not result['detail_type']:
                            result['detail_type'] = query_type
                    df.loc[index] = result
                    index += 1

                if index > 10000:
                    logger.info('Current df size is larger than 10000, save it first')
                    save_df(save_file, df)
                    index = 0
                    df = pd.DataFrame(columns=columns)
            except Exception:
                traceback.print_exc()
                logger.warn('location {} has exception'.format(str(location)))
                failed_location.append(location)
            except KeyboardInterrupt:
                if failed_location:
                    import pickle
                    logger.info('Save failed locations to "failed_{}.p"'.format(query_type))
                    save_data = {'location': failed_location,
                                 'radius': radius}
                    with open(os.path.join(save_path, 'failed_{}.p'.format(query_type)), 'w') as f:
                        pickle.dump(save_data, f)

                if spider is not None:
                    spider.stop()

                save_df(save_file, df)
                msg_body = "Your project finished by Interrupt, the below is the machine information\n{}".format(
                    '\n'.join(os.uname()))
                msg_body = "{}\ncurrent location is {}".format(msg_body, str(location))
                send_email_through_gmail('Test finished', msg_body, to_addr='markwang@connect.hku.hk')
                return

            finally:
                current_percentage = int(100 * (float(j) + float(i) / lat_partition_number) / lng_partition_number)
                if current_percentage - percentage >= 1:
                    logger.info("{}% complete".format(current_percentage))
                    percentage = current_percentage

    if failed_location:
        import pickle
        logger.info('Save failed locations to "failed_{}.p"'.format(query_type))
        save_data = {'location': failed_location,
                     'radius': radius}
        with open(os.path.join(save_path, 'failed_{}.p'.format(query_type)), 'w') as f:
            pickle.dump(save_data, f)

    if spider is not None:
        spider.stop()
    save_df(save_file, df)

    logger.info('Test finished')

    msg_body = "Your project finished, the below is the machine information\n{}".format('\n'.join(os.uname()))
    send_email_through_gmail('Test finished', msg_body, to_addr='markwang@connect.hku.hk')


def fill_in_missing_information(file_path):
    df = pd.read_csv(file_path, index_col=0)
    place_type = re.findall(r'_(\w+)_', file_path)[0]
    column_set = set(columns)
    df_keys = set(df.keys())
    for key in df_keys.difference(column_set):
        del df[key]
    keys_to_fill = column_set.difference(df_keys)
    if keys_to_fill:
        for key in keys_to_fill:
            df[key] = None

        if len(keys_to_fill) == 1 and 'detail_type' in keys_to_fill:
            need_detail_type = True
            require_place_detail = False
        elif 'detail_type' not in keys_to_fill:
            need_detail_type = False
            require_place_detail = True
        else:
            need_detail_type = True
            require_place_detail = True

        if need_detail_type:
            spider = GoogleMapSpider(spider_type="selenium")
            spider.start()
        else:
            spider = None
        miss_detail_place_list = []
        for index in df.index:
            time.sleep(1)
            if require_place_detail:
                result = query.place_detail(df.ix[index, 'place_id'])
                for key in keys_to_fill:
                    if key == 'detail_type':
                        continue
                    df.ix[index, key] = result[key]

            if need_detail_type:
                detail_type = spider.get_detail_type(df.ix[index, 'url'])

                if not detail_type:
                    logger.debug("current place {} has no detail_type".format(df.ix[index, 'place_id']))
                    logger.debug("its url is {}".format(df.ix[index, 'url']))
                    miss_detail_place_list.append(df.ix[index, 'place_id'])
                    df.ix[index, 'detail_type'] = place_type

                else:
                    df.ix[index, 'detail_type'] = detail_type
                    logger.debug("detail type is {}".format(detail_type))

        if need_detail_type:
            spider.stop()
        if miss_detail_place_list:
            with open('miss_detail_place.p', 'w') as f:
                import pickle
                pickle.dump(miss_detail_place_list, f)

    df.to_csv(file_path, encoding='utf8')


if __name__ == "__main__":
    # current = 31.41826635443038
    # print (current - us_south_lat) / (us_north_lat - us_south_lat)
    # current = -122.68395250594227
    # print (current - us_west_lng) / (us_east_lng - us_west_lng)
    fill_in_missing_information('usa_school_info.csv')
