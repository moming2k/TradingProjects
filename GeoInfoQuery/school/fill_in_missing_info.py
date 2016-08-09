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
detail_not_found_list = ['ChIJY2CzZkzfwFQRNrrQR7ZJzWo', 'ChIJg47w58c8hIARJ4aby_hr8VU', 'ChIJg47w58c8hIARXwD-Qof2qXI',
                         'ChIJE8YN5i5clVQREqS9-sLxyhs', 'ChIJMfq78-9slVQRWHwM61nTlRM', 'ChIJx0VLz1NzkVQRVE3SMkv-sLg',
                         'ChIJI5X9pTp1kVQRDDfwB3jr-zM', 'ChIJywQO8suglVQRj39QtAPy9HY', 'ChIJZ2J77dOglVQRwDq6WMOiYd0',
                         'ChIJ4cJx2jaglVQRlYdDFrhQbLk', 'ChIJR_2fWkZ1lVQRQHlf_11av1g', 'ChIJXz2wINd9j4ARo3YWMqqBv6w',
                         'ChIJpbMLP92GhYARP_xwCVB8RBE', 'ChIJjTLqHt6AhYARlqKc763sXXM', 'ChIJwcaBZSCbhYARmBgRK1Xs2B0',
                         'ChIJwZFJZJlehIAR41zifnvc1ds', 'ChIJh3Uw8_yqkVQRWdH20iY9uUg', 'ChIJ55ujpOF4j4ARLWOjXvtGP_c',
                         'ChIJC2spAbyAhYARoW_Dgi-3niY', 'ChIJ68UTYB_t0lQRFy3eFVSAMRA', 'ChIJxfKCDEb-kFQRkluuXoENZg8',
                         'ChIJ95zFVENWkFQRB2dMmRxglF4', 'ChIJ1TAscEoVkFQRs7cJCLw7oEo', 'ChIJ86IohRL-j1QRxiyNy8FECpk',
                         'ChIJjZwzUYF-hYAROxYnwrRLZM4', 'ChIJxeVMS9EGhYAReRyeU6kbvao', 'ChIJ6b4BJq3ikFQRLYVshG3hGBk',
                         'ChIJveBqwN0TkFQRQTckbX-Wwio', 'ChIJoXx_jtEPkFQRmXzSJ5o1Sh4', 'ChIJW5z9LtAPkFQRg8sg3WI9K9k',
                         'ChIJQe0EFXIFkFQRNhBw7jltTDQ', 'ChIJr5VZmdMRkFQRD4c8jYA9n_U', 'ChIJl0UWrpUShVQRynh31I_KqvU',
                         'ChIJhbCX2ISvj4ARERS0ntsI3hs', 'ChIJH80xr9ykj4ARiCQpF4GZeow', 'ChIJW1J8TQC7j4AR2yqaHS2OiPc',
                         'ChIJeyyS_dakj4AR-SYcphTHZ-w', 'ChIJE7gRANEThYAR3gKrFXOMuac', 'ChIJia6xjwNokFQRXgmtZmpB9U0',
                         'ChIJF1cFj4cSkFQRRzV3wFhmA9M']

fill_in_missing_information(file_path,
                            keys_to_fill={'detail_type'},
                            # keys_to_fill={'url', 'country'},
                            # start_index=124899,
                            start_index=13767,
                            index_to_fill=None)
