#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: query_church
# Author: Mark Wang
# Date: 24/7/2016

import os

from ..google_maps.query_us_place_information import query_information_from_google_maps

path = '/'.join(__file__.split('/')[:-1])
# print path

# raise Exception('hahah')

boundary = {'west': -124.6205424892261,
            'east': -66.885444,
            'north': 49.384358,
            'south': 42.4}

query_information_from_google_maps(query_type='church', country_code='usa', radius=5000.0, save_path=path,
                                   boundary=boundary, require_detail=False,
                                   # previous_file=os.path.join(path, 'usa_church_information.csv')
                                   )
