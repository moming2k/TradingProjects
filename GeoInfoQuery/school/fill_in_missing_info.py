#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: fill_in_missing_info
# Author: Mark Wang
# Date: 2/8/2016

from ..google_maps.query_us_place_information import fill_in_missing_information

file_path = '/Users/warn/PycharmProjects/QuestionFromProfWang/GeoInfoQuery/school/usa_school_info0.csv'

fill_in_missing_information(file_path, keys_to_fill={'url', 'country'}, start_index=8535)
