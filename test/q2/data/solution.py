#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: solution
# Author: Mark Wang
# Date: 13/7/2016

import re
import urllib
import urllib2

import GeoInfoQuery
import pandas
import numpy as np
from vincenty import vincenty
from BeautifulSoup import BeautifulSoup


def check_nan(name):
    """
    Check whether current value is none or not
    """
    if isinstance(name, float):
        return np.isnan(name)
    elif isinstance(name, str) or isinstance(name, unicode):
        return len(name) == 0
    elif name:
        return False
    else:
        return True


def get_business_address(company_name):
    """
    Using data from U.S. Securities and Exchange Commission to get address information
    :param company_name: the company that need to query
    :return: the detail address info
    """
    append_data = [('company', company_name),
                   ('owner', 'exclude'),
                   ('action', 'getcompany')]
    url = 'https://www.sec.gov/cgi-bin/browse-edgar?{}'.format(urllib.urlencode(append_data))
    req = urllib2.Request(url)
    rep = urllib2.urlopen(req)
    soup = BeautifulSoup(rep.read())
    rep.close()
    try:
        address_list = soup.find(id='contentDiv').findAll('div')[0].findAll('div')[1].findAll('span')
    except Exception, e:
        return ''
    else:
        new_address_info = []
        for item in address_list[:-1]:
            new_address_info.append(item.text.strip())

        return u', '.join(new_address_info)


def get_geocode_info(address):
    gmaps = GeoInfoQuery.Client('AIzaSyBTgAXoG24tG1ixSlvz_ZdhuTAxKo5JuDc')
    location = address.lower()
    g = gmaps.geocode(location)

    # format some place in bermuda
    if re.findall(r'pembroke|hamilton', location):
        location = re.sub(r'(pembroke|hamilton)[\s\S]+', r'\1, Bermuda', location)

    # format address in Dublin
    if 'dublin' in location:
        location = re.sub(r'(dublin)[\s\S]+', r'\1, Ireland', location)

    if not g:
        g = gmaps.geocode(location)

    while not g:
        location = u','.join(location.split(',')[1:])
        if not location:
            return pandas.Series({'lat': np.nan, 'lng': np.nan, 'distance': np.nan})
        g = gmaps.geocode(location)

    white_house_location = (38.8976763, 77.0387185)
    lat = g[0]['geometry']['location']['lat']
    lng = g[0]['geometry']['location']['lng']

    return pandas.Series({'lat': lat, 'lng': lng, 'distance': vincenty((lat, lng), white_house_location)})


if __name__ == "__main__":
    df = pandas.read_excel('coname_addresses.xlsx')

    empty_address = df['address'].apply(check_nan)
    empty_address_index = empty_address[empty_address == True].index
    for index in empty_address_index:
        df.ix[index, 'address'] = get_business_address(df.get_value(index, 'CONAME'))

    geo_info = df['address'].apply(get_geocode_info)
    df = pandas.concat([df, geo_info['lat'], geo_info['lng'], geo_info['distance']], axis=1)

    df.to_excel('output.xlsx')
