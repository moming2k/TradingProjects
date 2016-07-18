#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: get_church_data_from_google_maps
# Author: Mark Wang
# Date: 17/7/2016

import os

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
    df_list = []
    try:
        # this for prof wang's office computer
        # for i in range(1, 50, process_num):

        # use for my own one
        for i in range(200, 277, process_num):
            print "Start test time {}".format(i / process_num)
            lat = south_lat + delta_lat * i
            part_df = get_church_info_along_latitude(latitude=lat)
            part_df.drop_duplicates(['place_id'])
            df_list.append(part_df)

            # lat_list = []
            # for j in range(i, min(i + process_num, 277)):
            #     lat_list.append(south_lat + delta_lat * j)
            #
            # pool = Pool(len(lat_list))
            # result_df = pool.map(get_church_info_along_latitude, lat_list)
            # df_list.append(pd.concat(result_df, ignore_index=True, axis=0))
            # df_list[-1].drop_duplicates(['place_id'])
            # time.sleep(20)
    except Exception, err:
        import traceback

        traceback.print_exc()
        print err
    finally:
        if df_list:
            if os.path.isfile('us_church_information.p'):
                df = pd.read_pickle('us_church_information.p')
                df_list.insert(0, df)

            df = pd.concat(df_list, ignore_index=True, axis=0)
            df.drop_duplicates(['place_id'], inplace=True)
            df.to_pickle('us_church_information.p')
            df.to_csv('us_church_information.csv', encoding='utf8')

        from send_email import send_email_through_126

        msg_body = "Your project finished, the below is the machine information\n{}".format('\n'.join(os.uname()))
        send_email_through_126('Test finished', msg_body, to_addr='markwang@connect.hku.hk')
