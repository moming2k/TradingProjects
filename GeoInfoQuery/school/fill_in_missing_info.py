#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: fill_in_missing_info
# Author: Mark Wang
# Date: 2/8/2016

import os

from xvfbwrapper import Xvfb

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
                         'ChIJF1cFj4cSkFQRRzV3wFhmA9M', 'ChIJpaHwUDS0j4ARXty4gMq6W5Y', 'ChIJc-gh31u0j4ARdlF-l-3BNXI',
                         'ChIJI2wZZD23j4ARm6eGi6L9b-c', 'ChIJOxBe7mlhhYARufYQY8FdYV0', 'ChIJwWbHywPKj4ARaL5mv9LbD9g',
                         'ChIJ9b3wLEC1j4ARhz0f69010uM', 'ChIJC1fp0EG1j4ARqsGrNFeUDRA', 'ChIJWVV_70pehYAR74ODbskDfAw',
                         'ChIJh5nBykpehYARu1e64xPOmoM', 'ChIJ93-5qgGnmlQRkPrtQ0ehdu8', 'ChIJYx24O9nOj4AR6QCYLFlDfzs',
                         'ChIJeaO2bYFe7IARxKBrnB8sc2M', 'ChIJQXGEtLRclIARAIfbinvDc94', 'ChIJWXXFFeoslYARn--RfeBTL8w',
                         'ChIJ3xjSCDXgmFQRa3dS_7g72MQ', 'ChIJd5nRCDXgmFQREdw0mIhutbo', 'ChIJsdd4Eqq16YARinPC1cOAkMY',
                         'ChIJQ1XORo-_6oARKimKLJ9Fl20', 'ChIJp4W-l68i6IARm6jHitxlgeY', 'ChIJqQDzPGgY6IAR_hv4JfM4eck',
                         'ChIJUSsBAjaZwoARW55ooB2bJCQ', 'ChIJORTsWySGwoARyb9yUZVLjVY', 'ChIJL49B-o6HwoARVX6-eq8J76k',
                         'ChIJx4MrcZW7woAR9ZZTt4DBNbc', 'ChIJxyjIrh66woARTuaGbUwnFA4', 'ChIJO9890UKWwoARI187YU4wx54',
                         'ChIJbSsv4FyWwoARQrU4QV8jEK4', 'ChIJwbSf3rSRwoARPoqg3sif93I', 'ChIJm-UuI4PKwoARu7u14XfxLJA',
                         'ChIJf1UjoOm2woARtgcARauRbPY', 'ChIJI9iM0EfKwoARTk2bmxXy6AE', 'ChIJVbaBJwLGwoARcV6lzYq0BoE',
                         'ChIJle9xmIjIwoARC2g8vM3KOFw', 'ChIJ4b4YqK7HwoAR1U1sP8RRpy8', 'ChIJJRhIrPxawoARCs6eAYqS0vw',
                         'ChIJ5_Bey0Ap3YARwEEy0f1QswQ', 'ChIJQ8Tny8HTwoARqfG-88eLFkk', 'ChIJQS3S7gcp3YARU9JV6dMOIRQ',
                         'ChIJEQxBeGjY3IARZqVJ0aOqYJc', 'ChIJAf69UPnT3IARWu5bfIF2x_A', 'ChIJ7SVqirTX3IARB4YMFFhZ9DI',
                         'ChIJ5wBY6M4xw4ARBP_Lti-8Gbk', 'ChIJRRk6AS8vw4AR9p5TmVD4mZU', 'ChIJh9amJH_03IARjOnF8xYdUj0',
                         'ChIJ7c8YQf7M3IARQ3tmsb9omX4', 'ChIJW4znk8fJ3IARMtD4O-RoSGM', 'ChIJVY7RQgw2w4ARYEnbGkK_4oM',
                         'ChIJvajSoKer3oARlgvtKcClMWY', 'ChIJyW4dHd4D3IARV6VAG4T_rao', 'ChIJoUnW8sQG3IARyq11DLxOfzU',
                         'ChIJs7zLh6kL3IARdz48pN77ZQk']
vdisplay = Xvfb(width=1366, height=768)
vdisplay.start()
fill_in_missing_information(file_path,
                            keys_to_fill={'detail_type'},
                            # keys_to_fill={'url', 'country'},
                            # start_index=124899,
                            start_index=37844,
                            index_to_fill=None)
vdisplay.stop()
