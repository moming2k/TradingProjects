#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: query_us_bar_from_google_maps
# Author: Mark Wang
# Date: 31/7/2016

from xvfbwrapper import Xvfb

from ..google_maps.query_us_place_information import query_information_from_google_maps

path = '/'.join(__file__.split('/')[:-1])

boundary = {'west': -89.30153992287849,
            'east': -66.885444,
            'north': 48.493175,
            'south': 24.396308}
vdisplay = Xvfb(width=1366, height=768)
vdisplay.start()
query_information_from_google_maps(query_type='bar', country_code='usa', radius=6000.0, save_path=path,
                                   boundary=boundary
                                   )
vdisplay.stop()
