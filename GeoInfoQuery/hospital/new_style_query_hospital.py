#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: new_style_query_hospital
# Author: Mark Wang
# Date: 28/7/2016

from ..google_maps.query_us_place_information import query_information_from_google_maps

path = '/'.join(__file__.split('/')[:-1])

boudary = {'west': -124.848974,
           'east': -66.885444,
           'north': 49.384358,
           'south': 42.2418328}

query_information_from_google_maps(query_type='hospital', country_code='usa', radius=7000.0, save_path=path,
                                   boundary=boudary)
