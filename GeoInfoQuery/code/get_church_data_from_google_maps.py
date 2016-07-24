#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: get_church_data_from_google_maps
# Author: Mark Wang
# Date: 17/7/2016

import os
import datetime

import pandas as pd

from query_target_type_place_from_google_maps import QueryPlaceInfoFromGoogleMaps


def get_church_info_along_latitude(latitude):
    query = QueryPlaceInfoFromGoogleMaps(place_type='church', country_code='usa')
    return query.get_target_places_along_latitude(latitude=latitude, n_steps=583)


if __name__ == "__main__":
    process_num = 1

    # data got from us census
    north_lat = 49.384358
    south_lat = 24.396308

    # as there are around 2770 KM from the north to the south
    n_steps = 277

    delta_lat = (north_lat - south_lat) / (n_steps - 1)
    file_name = 'us_church_information'
    if os.path.isfile('{}.p'.format(file_name)):
        df = pd.read_pickle('{}.p'.format(file_name))

    else:
        df = pd.DataFrame(columns=['name', 'vicinity', 'lat', 'lng', 'place_id'])

    try:
        for i in range(0, n_steps, process_num):
            print datetime.datetime.today(), "Start test time {}".format(i / process_num)
            lat = south_lat + delta_lat * i
            part_df = get_church_info_along_latitude(latitude=lat)
            df = pd.concat([df, part_df], axis=0, ignore_index=True).drop_duplicates(['place_id'])
            df.to_pickle('{}.p'.format(file_name))

    except Exception, err:
        import traceback

        traceback.print_exc()
        print err
    finally:
        df.to_csv('{}.csv'.format(file_name))

        from send_email import send_email_through_gmail

        msg_body = "Your project finished, the below is the machine information\n{}".format('\n'.join(os.uname()))
        send_email_through_gmail('Test finished', msg_body, to_addr='markwang@connect.hku.hk')
