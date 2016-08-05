#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: fill_in_missing_info
# Author: Mark Wang
# Date: 2/8/2016

from ..google_maps.query_us_place_information import fill_in_missing_information

file_path = '/Users/warn/PycharmProjects/QuestionFromProfWang/GeoInfoQuery/school/usa_school_info0.csv'
not_found_list = [11639, 13698, 13711, 14588, 16599, 17646, 19105, 19448, 28810, 32246, 34318, 35014, 41208, 42111,
                  42610, 44694, 51210, 62994, 68618]

fill_in_missing_information(file_path, keys_to_fill={'url', 'country'}, start_index=70487,
                            index_to_fill=None)
