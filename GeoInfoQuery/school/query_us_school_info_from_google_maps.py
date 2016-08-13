#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: query_school_info_from_google_maps
# Author: Mark Wang
# Date: 24/7/2016

import os

from xvfbwrapper import Xvfb

from GeoInfoQuery.google_maps.query_us_place_information import query_information_from_google_maps

path = '/'.join(__file__.split('/')[:-1])
# print path

# raise Exception('hahah')

boundary = {'west': -73.14966136549927,
            'east': -66.885444,
            'north': 47.406239,
            'south': 40.638763}

vdisplay = Xvfb(width=1366, height=768)
vdisplay.start()

query_information_from_google_maps(query_type='school', country_code='usa', radius=7000.0, save_path=path,
                                   boundary=boundary,
                                   previous_file=os.path.join(path, 'usa_school_info0.csv'))
vdisplay.stop()
