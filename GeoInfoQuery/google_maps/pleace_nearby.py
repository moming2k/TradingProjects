#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: pleace_nearby
# Author: Mark Wang
# Date: 24/7/2016

import json
import time

import numpy as np
import pandas as pd

from base_class import BaseClass
from vincenty_directy import vinc_pt


class PlaceNearby(BaseClass):
    def __init__(self, key, proxy=None):
        BaseClass.__init__(self, proxy=proxy, key=key)

    def _nearby_search(self, location, radius, query_type=None, page_token=None):
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
        parameters = [('location', '{0[0]},{0[1]}'.format(location)),
                      ('radius', radius)]
        if query_type is not None:
            parameters.append(('type', query_type))

        if page_token is not None:
            parameters.append(('pagetoken', page_token))

        parameters.append(('language', 'en'))
        parameters.append(('key', self._api_key))
        query_result = self.http_get(url=url, parameters=parameters)
        json_result = json.loads(query_result, encoding='utf8')
        return json_result

    def nearby_search(self, location, radius, query_type=None):
        query_result = self._nearby_search(location, radius, query_type)
        results = []
        if 'results' in query_result:
            results.extend(query_result['results'])

        while 'next_page_token' in query_result:
            time.sleep(2)
            query_result = self._nearby_search(location, radius, page_token=query_result['next_page_token'])
            if 'results' in query_result:
                results.extend(query_result['results'])
        return results

    def _radar_search(self, location, radius, query_type=None):
        url = 'https://maps.googleapis.com/maps/api/place/radarsearch/json'
        parameters = [('location', '{0[0]},{0[1]}'.format(location)),
                      ('radius', radius)]
        if query_type is not None:
            parameters.append(('type', query_type))

        parameters.append(('language', 'en'))
        parameters.append(('key', self._api_key))
        query_result = self.http_get(url=url, parameters=parameters)
        json_result = json.loads(query_result, encoding='utf8')
        return json_result

    def radar_search(self, location, radius, query_type=None):
        query_result = self._radar_search(location, radius, query_type)
        if 0 < len(query_result['results']) < 200:
            return pd.DataFrame(query_result['results'])
        elif len(query_result['results']) == 0:
            return pd.DataFrame(columns=['geometry', 'id', 'place_id', 'reference'])
        else:
            new_radius = float(radius) / 2
            angle = 45
            df_list = []
            for i in range(4):
                time.sleep(2)
                new_location = vinc_pt(location[0], location[1], angle, new_radius)
                df_list.append(self.radar_search(new_location, new_radius, query_type=query_type))
                angle += 90

            df = pd.concat(df_list, axis=0, ignore_index=True)
            return df.drop_duplicates(['place_id'])

    def _place_detail_query(self, place_id):
        url = 'https://maps.googleapis.com/maps/api/place/details/json'
        parameters = [('placeid', place_id), ('language', 'en'), ('key', self._api_key)]

        query_result = self.http_get(url=url, parameters=parameters)
        json_result = json.loads(query_result, encoding='utf8')
        return json_result

    def place_detail(self, place_id):
        query_result = self._place_detail_query(place_id=place_id)

        max_try = 5
        while query_result['status'] != 'OK' and max_try > 0:
            time.sleep(5)
            query_result = self._place_detail_query(place_id)
            max_try -= 1

        query_result = query_result['result']
        place_detail = {
                        # 'formatted_address': query_result.get('formatted_address', ''),
                        # 'phone_number': query_result.get('formatted_phone_number', ''),
                        'lat': query_result.get('geometry', {}).get('location', {}).get('lat', np.nan),
                        'lng': query_result.get('geometry', {}).get('location', {}).get('lng', np.nan),
                        'place_id': place_id,
                        'name': query_result['name'],
                        'website': query_result.get('website', ''),
                        }

        if 'formatted_phone_number' in query_result:
            place_detail['phone_number'] = query_result['formatted_phone_number']
        elif 'international_phone_number' in query_result:
            place_detail['phone_number'] = query_result['international_phone_number']
        else:
            place_detail['phone_number'] = ''

        if 'vicinity' in query_result:
            place_detail['address'] = query_result['vicinity']
        elif 'formatted_address' in query_result:
            place_detail['address'] = query_result['formatted_address']
        else:
            place_detail['address'] = ''

        place_detail['zip_code'] = ''
        place_detail['state'] = ''

        for address_component in query_result.get('address_components', []):
            if "postal_code" in address_component['types']:
                place_detail['zip_code'] = address_component['long_name']

            if "administrative_area_level_1" in address_component['types']:
                place_detail['state'] = address_component['short_name']
        return place_detail

if __name__ == '__main__':
    test = PlaceNearby(key='AIzaSyAudxQLIC7XflSnljlLDthXpOYcIgP3czU', proxy='218.202.111.10:80')
    # result = test.radar_search((40.710000, -73.960000), radius=1250, query_type='church')
    import pickle
    import pprint
    #
    # place_id = result.ix[0, 'place_id']
    places = """ChIJ9Z07y-RawokRxnSJAFzcgjo
ChIJ4c8DrvxawokRduV6blFdLw0
ChIJiw6O20RawokRMGA7m42Aj9o
ChIJE_iIieNawokRCUBKaO4o3Sw
ChIJuaCzSbhawokRqobbtFMJ08U
ChIJJfTDGuZawokRX81Ym3nCCVU
ChIJRS6t1uVawokR0_UfYABqQQg
ChIJq1nCw-hawokRBWzaJoApR4E
ChIJsVVLT-ZawokRJrD67YVIRqI
ChIJdYrCBelawokR_mCWxObKP8w
ChIJs4PzwMZawokRLyxkeO7KA_k
ChIJo5L64eRawokRK6wd6fGP_D4
ChIJkboP1MdawokR4DrWnTyoLvw
ChIJZ7JirMBawokRHv4xuhFGjwA
ChIJKeOQxulawokR-Cf5I1BJbd0
ChIJnTwoz8JawokRMmj2BXvnjxA
ChIJdy8S8VtZwokRWflAlKltReY
ChIJkXpRncpawokRcXiab3e0SXI
ChIJzZ_sX_tawokR7bIGc7am4uI
ChIJ74FjCbdawokRT53jFZrZhc8
ChIJjcyL8R1bwokRA0jSSwSWS98
ChIJEcS4MrZawokRih2Id-ZJo5Y
ChIJfRFm4-hawokRQammQSMQeIA
ChIJIVwj2h9bwokRnhdfwouusaA
ChIJ6aY1D7dawokR71IbBf7jzPI
ChIJzZ_sX_tawokR-5HEe1nz8ZQ
ChIJObPkbx1bwokRUQczYlvf9II
ChIJadOp2elawokR_gaL4BtbmOw
ChIJmedv6-hawokRV_Fy7lckr1w
ChIJC-MTYeZawokR5ATkp1yI_6o
ChIJk18AxsZawokRClGkY9fagI4
ChIJ6TGzaMdawokRXE-3otfXvbs
ChIJBUlEx_pawokR4UGpDcCd_3U
ChIJ3fHAtORawokRthSuTg6MRQQ
ChIJBRCzAdxawokRsu6EnFyr6Ng
ChIJhccQlblawokRFFQIBNh93nE
ChIJ4Q1bX_FawokR6uxEH6RxBlQ
ChIJJXNKEM9awokRktRm3Om8UZU
ChIJx2FgLM9awokRlfekQTfDL6c
ChIJv8b12vtawokRKS9b8NCkP4o
ChIJDVXXrbBawokR_0QnJ3XyOzk
ChIJ9Z07y-RawokRxnSJAFzcgjo"""
    place_id_list = places.split('\n')
    place_result = []
    for place_id in place_id_list:
        place_result.append(test.place_detail(place_id=place_id))
    # pprint.pprint(place_result)
    # df = pd.read_csv('test.csv')
    df = pd.DataFrame(
        columns=['name', 'address', 'zip_code', 'state', 'phone_number', 'lat', 'lng', 'website', 'place_id'])
    for i in range(len(place_id_list)):
        pprint.pprint(place_result[i])
        df.loc[i] = place_result[i]
    df.to_csv('test.csv', encoding='utf8')

    # with open('radar_result.p', 'w') as f:
    #     pickle.dump(result, f)

    # with open('place_result.p', 'w') as f:
    #     pickle.dump(place_result, f)
