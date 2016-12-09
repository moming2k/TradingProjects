#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: query_uspto
# Author: warn
# Date: warn

import time
import urllib
import urllib2
import datetime
import re

import BeautifulSoup


def get(url, data_list=None, max_try=3):
    if data_list:
        url = "{}?{}".format(url, urllib.urlencode(data_list))
    query = urllib2.Request(url)
    current_try = 0
    while current_try < max_try:
        try:
            response = urllib2.urlopen(query)
            html = response.read()
            response.close()
            return html
        except Exception, e:
            return None
    raise Exception("Cannot open page {}".format(url))


def get_inventor_info(patent_id):
    try:
        target_url = 'http://patft.uspto.gov/netacgi/nph-Parser'
        data_list = [['Sect1', 'PTO2'],
                     ['Sect2', 'HITOFF'],
                     ['u', '/netahtml/PTO/search-adv.htm'],
                     ['r', '1'],
                     ['p', '1'],
                     ['f', 'G'],
                     ['l', '50'],
                     ['d', 'PTXT'],
                     ['S1', '{}.PN.'.format(patent_id)],
                     ['OS', 'PN/{}'.format(patent_id)],
                     ['RS', 'PN/{}'.format(patent_id)]]
        html = get(target_url, data_list=map(tuple, data_list))
        myMassage = [(re.compile('<!-([^-])'), lambda match: '<!--' + match.group(1))]
        soup = BeautifulSoup.BeautifulSoup(html, markupMassage=myMassage)
        tr_list = soup.findAll('tr')
        for tr in tr_list:
            if 'Inventors:' in tr.text:
                inventor_text = tr.text[10:]
                return inventor_text
        else:
            return None
    except Exception, err:
        return None


def process_df(input_df):
    new_df = input_df.copy()
    new_df['inventor_text'] = input_df['patent_id'].apply(get_inventor_info)
    return new_df


if __name__ == '__main__':
    import os

    import pandas as pd
    import numpy as np
    import pathos

    process_num = 10

    root_path = '/home/wangzg/Documents/WangYouan/research/InventorWho'

    data_path = os.path.join(root_path, 'data')
    tmp_path = os.path.join(root_path, 'temp')
    google_data_path = os.path.join(root_path, 'GooglePatentData')
    samput_data_path = os.path.join(root_path, 'SampatData')
    result_path = os.path.join(root_path, 'result')

    df_5 = pd.read_pickle(os.path.join(tmp_path, 'inventor_p_5_fc_10_new.p'))

    pool = pathos.multiprocessing.ProcessingPool(process_num)

    result_dfs = []
    split_df_5 = np.array_split(df_5, process_num * 10)
    print 'start calculation'
    for i in range(0, process_num * 10, process_num):
        return_result = pool.map(process_df, split_df_5[i: i + process_num])
        result_dfs.append(pd.concat(return_result, axis=0))
        print i
    result_df = pd.concat(result_dfs, axis=0)

    result_df.to_pickle(os.path.join(tmp_path, 'df_5_add_inventor_text.p'))
