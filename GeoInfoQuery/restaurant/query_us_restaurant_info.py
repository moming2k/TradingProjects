#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: query_us_restaurant_info
# Author: Mark Wang
# Date: 10/8/2016

from xvfbwrapper import Xvfb

from ..google_maps.query_us_place_information import query_information_from_google_maps

path = '/'.join(__file__.split('/')[:-1])

boundary = {'west': -122.31755397867973,
            'east': -66.885444,
            'north': 49.384358,
            'south': 24.396308}

vdisplay = Xvfb(width=1366, height=768)
vdisplay.start()

query_information_from_google_maps(query_type='restaurant', country_code='usa', radius=5000.0, save_path=path,
                                   boundary=boundary,
                                   )
vdisplay.stop()