#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: pleace_nearby
# Author: Mark Wang
# Date: 24/7/2016

import re
import json
import time

import numpy as np
import pandas as pd

from base_class import BaseClass
from vincenty_directy import vinc_pt


class PlaceNearby(BaseClass):
    def __init__(self, key, proxy=None, logger=None):
        BaseClass.__init__(self, proxy=proxy, key=key, logger=logger)

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
        if radius < 1:
            self.logger.warn(
                'radius is too small, stop continue query, location{}, radius {}'.format(str(location), radius))
            if len(query_result['results']) == 0:
                return pd.DataFrame(columns=['geometry', 'id', 'place_id', 'reference'])
            else:
                return pd.DataFrame(query_result['results'])
        if 0 < len(query_result['results']) < 200:
            return pd.DataFrame(query_result['results'])
        elif len(query_result['results']) == 0:
            return pd.DataFrame(columns=['geometry', 'id', 'place_id', 'reference'])
        else:
            new_radius = round(float(radius) / 2, 5)
            angle = 45
            df_list = []
            for i in range(4):
                time.sleep(1)
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

        if query_result.get('status') == 'NOT_FOUND':
            self.logger.warn('Current place ID {} is not found on google maps'.format(place_id))
            raise ValueError('Current place ID {} is not found on google maps'.format(place_id))

        max_try = 5
        while query_result['status'] != 'OK' and max_try > 0:
            time.sleep(5)
            query_result = self._place_detail_query(place_id)
            max_try -= 1

        if query_result.get('status') != 'OK' or 'result' not in query_result:
            # return {
            #     'address': "",
            #     'phone_number': "",
            #     'lat': 0.0,
            #     'lng': 0.0,
            #     'place_id': place_id,
            #     'name': "",
            #     'website': "",
            #     'zip_code': '',
            #     'state': '',
            #     'city': '',
            #     'url': ''
            # }
            self.logger.warn('current query result is {}'.format(str(query_result)))
            raise Exception("Current status is {}".format(query_result.get('status')))

        query_result = query_result['result']
        place_detail = {
            # 'formatted_address': query_result.get('formatted_address', ''),
            # 'phone_number': query_result.get('formatted_phone_number', ''),
            'lat': query_result.get('geometry', {}).get('location', {}).get('lat', np.nan),
            'lng': query_result.get('geometry', {}).get('location', {}).get('lng', np.nan),
            'place_id': place_id,
            'name': query_result['name'],
            'website': query_result.get('website', ''),
            'url': query_result.get('url', '')
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

        place_detail['zip_code'] = ""
        place_detail['state'] = ''
        place_detail['city'] = ''
        place_detail['country'] = ''

        for address_component in query_result.get('address_components', []):
            if "postal_code" in address_component['types']:
                if isinstance(address_component['long_name'], unicode):
                    place_detail['zip_code'] = address_component['long_name']
                else:
                    place_detail['zip_code'] = str(address_component['long_name'])

            if "administrative_area_level_1" in address_component['types']:
                place_detail['state'] = address_component['short_name']

            if "administrative_area_level_2" in address_component['types']:
                place_detail['city'] = address_component['long_name']

            if "country" in address_component['types']:
                place_detail['country'] = address_component['long_name']

        return place_detail

    def get_place_detail_type(self, url, place_name):
        if not url or not place_name:
            self.logger.warn('No url ({}) or name ({}) provide'.format(url, place_name))
            return ''

        html = self.http_get(url=url)
        result = re.findall(ur'cacheResponse\((.*)\)', html)
        if not result:
            self.logger.warn('Cannot find target information of given url')
            return ""
        info = unicode(result[0], encoding='utf8')

        brace_num = -1
        new_info_list = []
        index = 0
        for c in info:
            if c == '[':
                brace_num += 1
            if c == ']':
                brace_num -= 1

            if brace_num == 0 and c == ',':
                index += 1
            elif index > 9:
                new_info = u"".join(new_info_list)
                break
            elif index == 9:
                new_info_list.append(c)
        else:
            self.logger.warn('Can not find target information')
            self.logger.debug('information is {}'.format(info))
            return ""

        try:
            b = json.loads(new_info, encoding='utf8')
            return b[-16]
        except Exception, err:
            import traceback
            traceback.print_exc()
            self.logger.warn('translate json file failed as {}'.format(err))
            return ""


if __name__ == '__main__':
    test = PlaceNearby(key='AIzaSyAudxQLIC7XflSnljlLDthXpOYcIgP3czU', proxy='218.202.111.10:80')
    # result = test.radar_search((40.710000, -73.960000), radius=1250, query_type='church')
    import pickle
    import pprint
    import sys
    import logging

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    #
    # place_id = result.ix[0, 'place_id']
    places = """ChIJlcJyLk1bkFQR6qD8ViM7yX8
ChIJFWWBbJnU2lQR8j8I7-Wm6iw
ChIJX7UNV-NzxVQRPznqMwFLD9A
ChIJA1segeNzxVQR_y2kTIOWcYU
ChIJdfN1SlZxxVQRFojSg9v1MAg
ChIJ-xvOZjxuxVQRQYZz4wZvHIs
ChIJOTAfLst2xVQR95DQukcjJCY
ChIJy6VMVtx2xVQREcfLCSRXgrE
ChIJXTA3J5l2xVQR5mnS_rg2cZ4
ChIJx_6BbP55xVQRFdK0XV0LYf8
ChIJwZSvaf2CxVQRrbs30agSrJA
ChIJLVNdqFCga4gRW8ZU41gNpks
ChIJLfjc_PSxUoYR6Gu2py52ZCg
ChIJw4r55wyea4cRXuJviqyCUd8
ChIJYS5i6t59hYARP3cZYLRsMYU
ChIJ0Ujyk1ObrYcRYycNGS_pn58
ChIJWxK6dpaJf4gRnE9CQGczh6I
ChIJn4cR3P-MOIgRelm8TtOW62o
ChIJ2XsNIVjB3oYR-ctcRTHgknM
ChIJW4LXbBJhtYAR6siID5aF4Ug
ChIJSasZjw2DV4gRqTu0YL_1K6w"""
    place_id_list = places.split('\n')
    place_info = test.radar_search((32.52125677300614, -117.02671119591241), radius=6000, query_type='bar')
    place_id_list = place_info['place_id']
    place_result = []
    for place_id in place_id_list:
        time.sleep(2)
        result = test.place_detail(place_id=place_id)
        place_result.append(result)
        # place_result.append(
        #     [result['name'], test.get_place_detail_type(result['url'], result['name']), result['place_id']])
    pprint.pprint(place_result)
    # df = pd.read_csv('test.csv')
    # df = pd.DataFrame(
    #     columns=['name', 'address', 'zip_code', 'state', 'phone_number', 'lat', 'lng', 'website', 'place_id'])
    # for i in range(len(place_id_list)):
    #     pprint.pprint(place_result[i])
    #     df.loc[i] = place_result[i]
    # df.to_csv('test.csv', encoding='utf8')

    # with open('radar_result.p', 'w') as f:
    #     pickle.dump(result, f)

    # with open('place_result.p', 'w') as f:
    #     pickle.dump(place_result, f)
