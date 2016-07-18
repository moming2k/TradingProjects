#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: query_target_type_place_from_google_maps
# Author: Mark Wang
# Date: 16/7/2016

import math
import time

import googlemaps
import dstk
import pandas as pd
from vincenty import vincenty

dstk_query = dstk.DSTK()

GOOGLE_API_LIST = [
    'AIzaSyAudxQLIC7XflSnljlLDthXpOYcIgP3czU',
    'AIzaSyBXa08GfK8XERZ-BKxVzDzIVALIN3Ov93c',
    'AIzaSyAPpxW_0ZXY7iZI7TO5gi9TksHUDp3SQso',
    'AIzaSyAgjJTaPvtfaWYK9WDggkvHZkNq1X3mM7Y',
    'AIzaSyDNsXvr28Y1Su5AqSFuv3Gej3SQ9nei3N4',
    'AIzaSyBTgAXoG24tG1ixSlvz_ZdhuTAxKo5JuDc',
    'AIzaSyD517iPlsqV3MXoXBm_WPfB1rjKf55l6MY',
    'AIzaSyCsx8IfzepWaH26ruD5ydPqBcfJEYmdcuU',
    'AIzaSyAetD6cVbROS248tY4vyJG4eQavL8i94mk']


class QueryPlaceInfoFromGoogleMaps(object):
    """
    This class used to get the information of a specific type of some thing in united states, like "restaurant",
    "church", etc.
    """

    def __init__(self, place_type='church', country_code='usa'):
        """
        initialize the class, include the place typa information

        :param place_type: possible value can be found in https://developers.google.com/places/supported_types
        """
        self.place_type = place_type
        self.country_code = country_code
        self._key_index = 0
        self._gmap_client = googlemaps.Client(key=GOOGLE_API_LIST[self._key_index])

    def get_target_places_along_latitude(self, latitude, longitude_range=None, n_steps=None):
        if longitude_range is None:
            west_longitude = -124.848974
            east_longitude = -66.885444

        elif hasattr(longitude_range, '__len__') and len(longitude_range) > 1:
            west_longitude = longitude_range[0]
            east_longitude = longitude_range[1]
        else:
            return self.get_location_nearby_places((latitude, longitude_range))

        if n_steps is None:
            n_steps = 583

        delta_longitude = (east_longitude - west_longitude) / n_steps

        radius = vincenty((latitude, west_longitude), (latitude, east_longitude)) / (
            (n_steps - 1) * math.sqrt(2)) * 1000

        church_df = pd.DataFrame(columns=['name', 'vicinity', 'lat', 'lng', 'place_id'])
        church_df_size = 0

        for i in range(n_steps):
            coordinate = (latitude, west_longitude + i * delta_longitude)
            if self._is_geocode_in_target_country(coordinate=coordinate):
                try:
                    church_result = self.get_location_nearby_places(location=coordinate, radius=radius)
                except Exception, err:
                    import traceback
                    traceback.print_exc()
                    # print coordinate
                    # print radius
                    # print err
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
                                                     'vicinity': church_info['vicinity'],
                                                     'lat': lat,
                                                     'lng': lng,
                                                     }
                    church_df_size += 1

        return church_df.drop_duplicates(['place_id'])

    def _query_google_map_places_nearby(self, location, radius=None, page_token=None):
        result = self._gmap_client.places_nearby(location=location, type=self.place_type, open_now=False, radius=radius,
                                                 page_token=page_token)

        while result['status'] == "OVER_QUERY_LIMIT":
            self._key_index += 1
            if self._key_index < len(GOOGLE_API_LIST):
                self._gmap_client = googlemaps.Client(key=GOOGLE_API_LIST[self._key_index])
            else:
                break
            result = self._gmap_client.places_nearby(location=location, type=self.place_type, open_now=False,
                                                     radius=radius, page_token=page_token)
        return result

    def get_location_nearby_places(self, location, radius=5000):
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
            # print location
            pass
        return church_result

    def _is_geocode_in_target_country(self, coordinate):
        """ Check given coordinate is in the U.S. or not """
        query_result = dstk_query.coordinates2politics(coordinate)[0]
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

    df = test.get_target_places_along_latitude(27.56508245652174)
    # result = test.get_location_nearby_places((27.56508245652174, -99.49614355403088), radius=6885.75129564)
    # print result
    df.drop_duplicates(['place_id'])
    df.to_csv('output.csv', encoding='utf8')
