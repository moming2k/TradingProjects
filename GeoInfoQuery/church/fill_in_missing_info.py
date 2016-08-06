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
not_found_list = []

fill_in_missing_information(file_path, keys_to_fill={'url', 'city', 'country'},
                            # start_index=2227,
                            # end_index=87858,
                            index_to_fill=None)
