#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: query_target_type_place_from_google_maps
# Author: Mark Wang
# Date: 16/7/2016

import pickle
import math

import googlemaps
import dstk
import pandas as pd
from vincenty import vincenty

dstk_query = dstk.DSTK()

GOOGLE_API_LIST = ['AIzaSyAudxQLIC7XflSnljlLDthXpOYcIgP3czU',
                   'AIzaSyAPpxW_0ZXY7iZI7TO5gi9TksHUDp3SQso',
                   'AIzaSyAgjJTaPvtfaWYK9WDggkvHZkNq1X3mM7Y',
                   'AIzaSyDNsXvr28Y1Su5AqSFuv3Gej3SQ9nei3N4',
                   'AIzaSyBXa08GfK8XERZ-BKxVzDzIVALIN3Ov93c',
                   'AIzaSyBTgAXoG24tG1ixSlvz_ZdhuTAxKo5JuDc']


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
            n_steps = 500

        delta_longitude = (east_longitude - west_longitude) / n_steps

        radius = vincenty((latitude, west_longitude), (latitude, east_longitude)) / (n_steps * math.sqrt(2))

        church_df = pd.DataFrame(columns=['name', 'vicinity', 'lat', 'lng', 'place_id'])
        church_df_size = 0

        for i in range(n_steps):
            coordinate = (latitude, west_longitude + i * delta_longitude)
            if self._is_geocode_in_target_country(coordinate=coordinate):
                church_result = self.get_location_nearby_places(location=coordinate, radius=radius)
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

        return church_df

    def _query_google_map_places_nearby(self, location, radius=None, page_token=None):
        result = self._gmap_client.places_nearby(location=location, type=self.place_type, open_now=False, radius=radius,
                                                 page_token=page_token)

        while result['status'] == "OVER_QUERY_LIMIT":
            self._key_index += 1
            if self._key_index < len(GOOGLE_API_LIST):
                self._gmap_client = googlemaps.Client(key=GOOGLE_API_LIST[self._key_index])
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
            result = self._query_google_map_places_nearby(location=location, page_token=result['next_page_token'])
            if result['status'] != "OK":
                return church_result

            church_result.extend(result['results'])

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
    # result = gmaps.places_nearby(location=(39.5584725, -119.9919577), type='church', open_now=False, radius=1)
    # with open("zero.p", 'w') as f:
    #     pickle.dump(result, f)
    #
    # print result
    test = QueryPlaceInfoFromGoogleMaps()
    df = test.get_target_places_along_latitude(49.384358)
    df.to_pickle('output.p')
