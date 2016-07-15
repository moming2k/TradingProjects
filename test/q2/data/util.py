#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: util
# Author: Mark Wang
# Date: 12/7/2016

import re
import urllib
import urllib2

import geocoder
import googlemaps
import numpy as np
import pandas as pd
from vincenty import vincenty
from BeautifulSoup import BeautifulSoup


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


def get_location_distance(info, keys):
    gmaps = googlemaps.Client('AIzaSyAudxQLIC7XflSnljlLDthXpOYcIgP3czU')
    location = '{}, {}'.format(info[keys[0]], info[keys[1]])
    g = gmaps.geocode(location)

    if not g:

        location = info[keys[1]].lower()

        # format some place in bermuda
        if re.findall(r'pembroke|hamilton', location):
            location = re.sub(r'(pembroke|hamilton)[\s\S]+', r'\1, Bermuda', location)

        # format address in Dublin
        if 'dublin' in location:
            location = re.sub(r'(dublin)[\s\S]+', r'\1, Ireland', location)

        g = gmaps.geocode(location)
        while not g:
            location = u','.join(location.split(',')[1:])
            g = gmaps.geocode(location)
            if not location:
                return pd.Series({'lat': np.nan, 'lng': np.nan, 'distance': np.nan})

    white_house_location = (38.8976763, 77.0387185)
    lat = g[0]['geometry']['location']['lat']
    lng = g[0]['geometry']['location']['lng']

    return lat, lng, vincenty((lat, lng), white_house_location)


def get_location_distance_geocoder(location):
    g = geocoder.arcgis(location)

    location = location.lower()

    if not g.ok:

        # format some place in bermuda
        if re.findall(r'pembroke|hamilton', location):
            location = re.sub(r'(pembroke|hamilton)[\s\S]+', r'\1, Bermuda', location)

        # format address in Dublin
        if 'dublin' in location:
            location = re.sub(r'(dublin)[\s\S]+', r'\1, Ireland', location)

        while not g.ok:
            g = geocoder.arcgis(location)
            if g.ok:
                break

            g = geocoder.bing(location, key='AgwupPLCge7gXDhl4q7D0gnhTlHtjLY03Y5vPHaui5uT3XqCMi-G1o7L1jjUv5Dp')
            if g.ok:
                break

            g = geocoder.yahoo(location)
            if g.ok:
                break

            g = geocoder.osm(location)
            if g.ok:
                break

            location = u','.join(location.split(',')[1:])
            if not location:
                return pd.Series({'lat': np.nan, 'lng': np.nan, 'distance': np.nan})

    white_house_location = (38.8976763, 77.0387185)
    lat = g.lat
    lng = g.lng

    return pd.Series({'lat': lat, 'lng': lng, 'distance': vincenty((lat, lng), white_house_location)})
