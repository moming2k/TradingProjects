#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: query_target_type_place_from_google_maps
# Author: Mark Wang
# Date: 16/7/2016

import os
import math
import time
import traceback
import urllib2
import datetime

try:
    import simplejson as json
except ImportError:
    import json

import googlemaps
import pandas as pd
from vincenty import vincenty

GOOGLE_API_LIST = [
    'AIzaSyAudxQLIC7XflSnljlLDthXpOYcIgP3czU',  # 1
    'AIzaSyAPpxW_0ZXY7iZI7TO5gi9TksHUDp3SQso',
    'AIzaSyAgjJTaPvtfaWYK9WDggkvHZkNq1X3mM7Y',  # 3 used by my mac
    'AIzaSyDNsXvr28Y1Su5AqSFuv3Gej3SQ9nei3N4',
    'AIzaSyBTgAXoG24tG1ixSlvz_ZdhuTAxKo5JuDc',
    'AIzaSyD517iPlsqV3MXoXBm_WPfB1rjKf55l6MY',  # 7 used by linux
    'AIzaSyCsx8IfzepWaH26ruD5ydPqBcfJEYmdcuU',
    'AIzaSyAetD6cVbROS248tY4vyJG4eQavL8i94mk',
    'AIzaSyBXa08GfK8XERZ-BKxVzDzIVALIN3Ov93c',  # 6 used by wzg office
]


class QueryPlaceInfoFromGoogleMaps(object):
    """
    This class used to get the information of a specific type of some thing in united states, like "restaurant",
    "church", etc.
    """

    def __init__(self, place_type='church', country_code='usa'):
        """
        initialize the class, include the place_id typa information

        :param place_type: possible value can be found in https://developers.google.com/places/supported_types
        """
        self.place_type = place_type
        self.country_code = country_code
        # self._key_index = 0
        if os.uname()[0] == 'Darwin':
            self._gmap_client = googlemaps.Client(key='AIzaSyAgjJTaPvtfaWYK9WDggkvHZkNq1X3mM7Y')
        elif os.uname()[1] == 'ewin3011':
            self._gmap_client = googlemaps.Client(key='AIzaSyBXa08GfK8XERZ-BKxVzDzIVALIN3Ov93c')
        else:
            self._gmap_client = googlemaps.Client(key='AIzaSyD517iPlsqV3MXoXBm_WPfB1rjKf55l6MY')

    def get_target_places_along_latitude(self, latitude, longitude_range=None, n_steps=None, radius=5000.0,
                                         check_location=True):

        church_df = pd.DataFrame(columns=['name', 'vicinity', 'lat', 'lng', 'place_id'])
        church_df_size = 0

        # the following range is used for the us.
        if longitude_range is None:
            west_longitude = -124.848974
            east_longitude = -66.885444

        elif hasattr(longitude_range, '__len__') and len(longitude_range) > 1:
            west_longitude = longitude_range[0]
            east_longitude = longitude_range[1]
        else:
            church_result = self.get_location_nearby_places((latitude, longitude_range), radius=radius)

            for church_info in church_result:
                lat = church_info['geometry']['location']['lat']
                lng = church_info['geometry']['location']['lng']
                if not self._is_geocode_in_target_country((lat, lng)):
                    continue
                church_df.loc[church_df_size] = {'name': church_info['name'],
                                                 'place_id': church_info['place_id'],
                                                 'vicinity': church_info.get('vicinity', ''),
                                                 'lat': lat,
                                                 'lng': lng,
                                                 }
                church_df_size += 1
            return church_df

        if n_steps is None:
            n_steps = 583

        delta_longitude = (east_longitude - west_longitude) / (n_steps - 1)

        radius = vincenty((latitude, west_longitude), (latitude, east_longitude)) / (
            (n_steps - 1) * math.sqrt(2)) * 1000

        for i in range(n_steps):
            coordinate = (latitude, west_longitude + i * delta_longitude)
            print datetime.datetime.today()
            if not check_location or self._is_geocode_in_target_country(coordinate=coordinate):
                try:
                    church_result = self.get_location_nearby_places(location=coordinate, radius=radius)
                except Exception, err:
                    traceback.print_exc()
                    print 'Current coordinate %s' % str(coordinate)
                    print 'Current radius %s' % str(radius)
                    break

                for church_info in church_result:
                    lat = church_info['geometry']['location']['lat']
                    lng = church_info['geometry']['location']['lng']
                    if not self._is_geocode_in_target_country((lat, lng)):
                        continue
                    church_df.loc[church_df_size] = {'name': church_info['name'],
                                                     'place_id': church_info['place_id'],
                                                     'vicinity': church_info.get('vicinity', ''),
                                                     'lat': lat,
                                                     'lng': lng,
                                                     }
                    church_df_size += 1

        return church_df.drop_duplicates(['place_id'])

    def _query_google_map_places_nearby(self, location, radius=None, page_token=None):
        result = self._gmap_client.places_nearby(location=location, type=self.place_type, open_now=False, radius=radius,
                                                 page_token=page_token)

        return result

    def get_location_nearby_places(self, location, radius=5000.0):
        """Using specific location to find nearby places"""
        church_result = []
        result = self._query_google_map_places_nearby(location=location, radius=radius)

        if result['status'] != "OK":
            return church_result

        church_result.extend(result['results'])
        while 'next_page_token' in result:
            # print result['next_page_token']
            time.sleep(2)
            result = self._query_google_map_places_nearby(location=location, radius=radius,
                                                          page_token=result['next_page_token'])
            if result['status'] != "OK":
                return church_result

            church_result.extend(result['results'])

        # maximum results get from google
        if len(church_result) == 60:
            if os.path.isfile('over_60.p'):
                df = pd.read_pickle('over_60.p')
            else:
                df = pd.DataFrame(columns=['lat', 'lng'])
            index = df.shape[0]
            df.loc[index] = {'lat': location[0], 'lng': location[1]}
            df.to_pickle('over_60.p')
        return church_result

    def _is_geocode_in_target_country(self, coordinate):
        """ Check given coordinate is in the U.S. or not """
        try:
            api_url = 'http://www.datasciencetoolkit.org/coordinates2politics'
            api_body = json.dumps(coordinate)
            response_string = urllib2.urlopen(api_url, api_body).read()
            query_result = json.loads(response_string, encoding='utf8')

            if 'error' in query_result:
                print coordinate
                print query_result['error']
                response_string = urllib2.urlopen(api_url, api_body).read()
                query_result = json.loads(response_string, encoding='utf8')
                if 'error' in query_result:
                    raise Exception(query_result['error'])

        except Exception, err:
            traceback.print_exc()
            print coordinate
            time.sleep(10)
            api_url = 'http://www.datasciencetoolkit.org/coordinates2politics'
            api_body = json.dumps(coordinate)
            response_string = urllib2.urlopen(api_url, api_body).read()
            query_result = json.loads(response_string, encoding='utf8')
            if 'error' in query_result:
                print coordinate
                print query_result['error']
                response_string = urllib2.urlopen(api_url, api_body).read()
                query_result = json.loads(response_string, encoding='utf8')
                if 'error' in query_result:
                    raise Exception(query_result['error'])

        query_result = query_result[0]
        if query_result['politics']:
            for info in query_result['politics']:
                if info['friendly_type'] == 'country':
                    return info['code'] == self.country_code
        return False


if __name__ == "__main__":
    # gmaps = googlemaps.Client('AIzaSyBTgAXoG24tG1ixSlvz_ZdhuTAxKo5JuDc')
    # result = gmaps.places_nearby(location=(48.384358, -122.36340238765008), type='church', open_now=False, radius=5000)
    # with open("zero.p", 'w') as f:
    #     pickle.dump(result, f)

    # print result
    test = QueryPlaceInfoFromGoogleMaps()

    # df = test.get_target_places_along_latitude(27.56508245652174)
    # test._is_geocode_in_target_country((25.482744956521742, -81.10291362264152))
    result = test.get_location_nearby_places((25.482744956521742, -81.10291362264152), radius=6885.75129564)
    print result
    # df.drop_duplicates(['place_id'])
    # df.to_csv('output.csv', encoding='utf8')
