#!/usr/bin/env python
# -*- coding: utf-8 -*-

# File Name: merge_csv_file
# Created by warn on 8/5/16

import pandas

if __name__ == '__main__':
    df = pandas.concat([pandas.read_csv('usa_hospital_info.csv', index_col=0),
                        pandas.read_csv('../google_maps/usa_hospital_info.csv', index_col=0)],
                       axis=0, ignore_index=True)
    df = df.drop_duplicates(['place_id']).reset_index(drop=True)
    df.to_csv('us_hospital_info.csv', encoding='utf8')
