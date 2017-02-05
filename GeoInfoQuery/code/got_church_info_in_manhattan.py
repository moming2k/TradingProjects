#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: got_data_in_manhattan
# Author: Mark Wang
# Date: 20/7/2016

import os
import pandas as pd

from query_target_type_place_from_google_maps import QueryPlaceInfoFromGoogleMaps

if __name__ == '__main__':
    north_lat = 40.89
    south_lat = 40.66
    west_lng = -74.1
    east_lng = -74.1

    n_parts = 70
    df_list = []
    file_name = 'Manhattan_church_information'
    if os.path.isfile('{}.p'.format(file_name)):
        df = pd.read_pickle('{}.p'.format(file_name))

    else:
        df = pd.DataFrame(columns=['name', 'vicinity', 'lat', 'lng', 'place_id'])
    try:
        query_gmaps = QueryPlaceInfoFromGoogleMaps()
        delta_lat = (north_lat - south_lat) / (n_parts - 1)

        # use for my own one
        for i in range(n_parts):
            lat = south_lat + i * delta_lat
            new_df = query_gmaps.get_target_places_along_latitude(lat, [west_lng, east_lng][1], n_steps=30,
                                                                        check_location=False, radius=400.0)
            df = pd.concat([df, new_df], ignore_index=True, axis=0)

    except Exception, err:
        import traceback

        traceback.print_exc()
        print err
    finally:
        # if df_list:
            # if os.path.isfile('Manhattan_church_information.p'):
            #     own_report_df = pd.read_pickle('Manhattan_church_information.p')
            #     df_list.insert(0, own_report_df)
            #
            # own_report_df = pd.concat(df_list, ignore_index=True, axis=0)
        df.drop_duplicates(['place_id'], inplace=True)
        df.to_pickle('{}.p'.format(file_name))
        df.to_csv('{}.csv'.format(file_name), encoding='utf8')

        from send_email import send_email_through_gmail

        msg_body = "Your project finished, the below is the machine information\n{}".format('\n'.join(os.uname()))
        send_email_through_gmail('Test finished', msg_body, to_addr='markwang@connect.hku.hk')
