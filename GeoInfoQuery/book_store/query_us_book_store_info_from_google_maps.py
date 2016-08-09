#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: query_us_book_store_info_from_google_maps
# Author: Mark Wang
# Date: 31/7/2016

from ..google_maps.query_us_place_information import query_information_from_google_maps

path = '/'.join(__file__.split('/')[:-1])

boundary = {'west': -76.81818755368654,
            'east': -66.885444,
            'north': 49.384358,
            'south': 24.396308}

query_information_from_google_maps(query_type='book_store', country_code='usa', radius=10000.0, save_path=path,
                                   boundary=boundary
                                   )
