#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: query_church_from_google_maps
# Author: Mark Wang
# Date: 16/7/2016

import pickle

import googlemaps


class QueryUSPlaceInfoFromGoogleMaps(object):
    """
    This class used to get the information of a specific type of some thing in united states, like "restaurant",
    "church", etc.
    """
    def __init__(self, place_type='church', country_code='US'):
        """
        initialize the class, include the place typa information

        :param place_type: possible value can be found in https://developers.google.com/places/supported_types
        """
        self.place_type = place_type
        self.country_code = country_code


if __name__ == "__main__":
    gmaps = googlemaps.Client('AIzaSyBTgAXoG24tG1ixSlvz_ZdhuTAxKo5JuDc')
    result = gmaps.places_nearby(location=(39.5584725, -119.9919577), type='church', open_now=False, radius=100000)
    with open("test.p", 'w') as f:
        pickle.dump(result, f)

    print result
