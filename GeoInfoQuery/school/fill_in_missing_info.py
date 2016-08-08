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
not_found_list = ['ChIJY2CzZkzfwFQRNrrQR7ZJzWo', 'ChIJg47w58c8hIARJ4aby_hr8VU', 'ChIJg47w58c8hIARXwD-Qof2qXI',
                  'ChIJE8YN5i5clVQREqS9-sLxyhs', 'ChIJMfq78-9slVQRWHwM61nTlRM', 'ChIJx0VLz1NzkVQRVE3SMkv-sLg',
                  'ChIJI5X9pTp1kVQRDDfwB3jr-zM']

fill_in_missing_information(file_path,
                            keys_to_fill={'detail_type'},
                            # keys_to_fill={'url', 'country'},
                            # start_index=124899,
                            start_index=4671,
                            index_to_fill=None)
