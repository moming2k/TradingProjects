#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: fill_in_missing_info
# Author: Mark Wang
# Date: 2/8/2016

import os

from ..google_maps.query_us_place_information import fill_in_missing_information

path = '/'.join(__file__.split('/')[:-1])
file_path = os.path.join(path, 'usa_church_information.csv')
not_found_list = [996, 1387, 1428, 4148, 4592, 6084, 6173, 8790, 12606, 13616, 14575, 14826, 15736, 17353, 18255, 20410,
                  20503, 21899, 23243, 23450, 23714, 23728, 23732, 24746, 25046, 26550, 27486, 29175, 29224, 29573,
                  31440, 33718, 34615, 35504, 40233, 42699, 45085, 45965, 45969, 46354, 47968, 55173, 56927, 59193,
                  62441, 65794, 67913, 68568, 69606, 71088, 74374, 76019, 402483, 402491, 402515, 408022]

fill_in_missing_information(file_path, keys_to_fill={'url', 'city', 'country'},
                            start_index=(411020 - 50000),
                            end_index=(411020 - 10000),
                            index_to_fill=None)
