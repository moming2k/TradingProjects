#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: query_school_info_from_google_maps
# Author: Mark Wang
# Date: 24/7/2016

from ..google_maps.query_us_place_information import query_information_from_google_maps

path = '/'.join(__file__.split('/')[:-1])

boundary = {'west': -121.79826189473684,
           'east': -120.81416121561969,
           'north': 49.384358,
           'south': 24.396308}

query_information_from_google_maps(query_type='gym', country_code='usa', radius=10000.0, save_path=path,
                                   # boundary=boundary,
                                   # previous_file='/Users/warn/PycharmProjects/QuestionFromProfWang/GeoInfoQuery/school/usa_school_info0.csv')
                                   )