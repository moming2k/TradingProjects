#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: fill_in_missing_info
# Author: Mark Wang
# Date: 2/8/2016

import os

from ..google_maps.query_us_place_information import fill_in_missing_information

path = '/'.join(__file__.split('/')[:-1])
file_path = os.path.join(path, 'usa_school_info0.csv')
not_found_list = [11639, 13698, 13711, 14588, 16599, 17646, 19105, 19448, 28810, 32246, 34318, 35014, 41208, 42111,
                  42610, 44694, 51210, 62994, 68618, 86637, 88927, 92524, 93457, 94609, 96780, 96781, 104845, 113014,
                  120585, 120665, 122283, 124833, 135889, 138857, 140235, 141836, 144530, 153492, 156245, 157037,
                  159701]

fill_in_missing_information(file_path,
                            # keys_to_fill={'detail_type'},
                            keys_to_fill={'url', 'country'},
                            start_index=124899,
                            # start_index=87858,
                            index_to_fill=None)
