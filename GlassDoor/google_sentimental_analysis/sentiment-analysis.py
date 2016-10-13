#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: sentiment-analysis
# Author: Mark Wang
# Date: 12/10/2016

import os
import datetime
import time

import pathos
import httplib2
import pandas as pd
import numpy as np
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

DISCOVERY_URL = ('https://{api}.googleapis.com/'
                 '$discovery/rest?version={apiVersion}')

PARENT_PATH = '/home/wangzg/Documents/WangYouan/research/Glassdoor'
GOOGLE_API_PATH = 'google_nlp'
CREDENTIAL_FILE = os.path.join(PARENT_PATH, GOOGLE_API_PATH, 'markwang.json')
RESULT_PATH = 'output'

GOOGLE_NLP_MAG = 'GNLPMag'
GOOGLE_NLP_POL = 'GNLPPol'


def query_sentiment_infomation(text_str, credential_path=CREDENTIAL_FILE):
    """Run a sentiment analysis request on text within a passed filename"""

    credentials = GoogleCredentials.from_stream(credential_path).create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform']
    )
    http = httplib2.Http()
    credentials.authorize(http)

    service = discovery.build('language', 'v1beta1',
                              http=http, discoveryServiceUrl=DISCOVERY_URL)

    service_request = service.documents().analyzeSentiment(
        body={
            'document': {
                'type': 'PLAIN_TEXT',
                'content': text_str,
            }
        })

    response = service_request.execute()
    return response['documentSentiment']['polarity'], response['documentSentiment']['magnitude']


def process_df(df_path, result_df_path, process_num=16):
    df = pd.read_csv(df_path, index_col=0)
    if os.path.isfile(result_df_path):
        previous_df = pd.read_csv(result_df_path, index_col=0)
        df = df.ix[df.index.difference(previous_df.index)]
    else:
        previous_df = None

    pool = pathos.multiprocessing.ProcessingPool(process_num)
    split_dfs = np.array_split(df, process_num)

    result_dfs = pool.map(process_csv_df, split_dfs)
    new_result = pd.concat(result_dfs, axis=0)
    if previous_df is not None:
        new_result = pd.concat([new_result, previous_df], axis=0)

    new_result = new_result.sort_index()

    new_result.to_csv(result_df_path)


def process_csv_df(input_df):
    new_index_list = ['prosCommunGNLPMag', 'consCommunGNLPMag', 'adviceCommunGNLPMag', 'allCommunGNLPMag',
                      'prosCommunGNLPPol', 'consCommunGNLPPol', 'adviceCommunGNLPPol', 'allCommunGNLPPol']
    result_df = pd.DataFrame(columns=new_index_list)
    range_index = input_df.index

    for i in range_index:
        row_dict = {}
        for col_name in ['prosCommun', 'consCommun', 'adviceCommun', 'allCommun']:
            mag_key = '{}{}'.format(col_name, GOOGLE_NLP_MAG)
            pol_key = '{}{}'.format(col_name, GOOGLE_NLP_POL)
            info = input_df.ix[i, col_name]
            if not hasattr(info, 'decode'):
                row_dict[mag_key] = np.nan
                row_dict[pol_key] = np.nan
            else:
                try:
                    row_dict[pol_key], row_dict[mag_key] = query_sentiment_infomation(info)
                    time.sleep(0.01)
                except Exception, err:
                    print err
                    print i
                    if 'Insufficient tokens' in str(err):
                        return result_df
                    else:
                        row_dict[pol_key], row_dict[mag_key] = np.nan, np.nan

        result_df.loc[i] = row_dict

    return result_df


def handle_all_info():
    df = pd.read_csv(os.path.join(PARENT_PATH, RESULT_PATH, r'review_commun.csv'),
                     usecols=['prosCommun', 'consCommun', 'adviceCommun', 'allCommun'])
    new_index_list = ['prosCommunGNLPMag', 'consCommunGNLPMag', 'adviceCommunGNLPMag', 'allCommunGNLPMag',
                      'prosCommunGNLPPol', 'consCommunGNLPPol', 'adviceCommunGNLPPol', 'allCommunGNLPPol']
    result_df_path = os.path.join(PARENT_PATH, RESULT_PATH, 'google_nlp_result.csv')
    if os.path.isfile(result_df_path):
        result_df = pd.read_csv(result_df_path, index_col=0)
        range_index = list(set(df.index).difference(set(result_df.index)))
        range_index.sort()
    else:
        result_df = pd.DataFrame(columns=new_index_list)
        range_index = df.index

    print min(range_index)

    percent = 0
    new_percent = 0
    print datetime.datetime.today()
    i = 0
    try:
        for i in range_index:
            row_dict = {}
            for col_name in ['prosCommun', 'consCommun', 'adviceCommun', 'allCommun']:
                mag_key = '{}{}'.format(col_name, GOOGLE_NLP_MAG)
                pol_key = '{}{}'.format(col_name, GOOGLE_NLP_POL)
                info = df.ix[i, col_name]
                if not hasattr(info, 'decode'):
                    row_dict[mag_key] = np.nan
                    row_dict[pol_key] = np.nan
                else:
                    row_dict[pol_key], row_dict[mag_key] = query_sentiment_infomation(info)
            result_df.loc[i] = row_dict
            percent += 1
            new_percent_tmp = int(float(percent) / len(range_index) * 100)
            if new_percent_tmp - new_percent >= 1:
                print datetime.datetime.today(), '{}% finished'.format(new_percent_tmp)
                new_percent = new_percent_tmp
                result_df.to_csv(result_df_path, encoding='utf8')

    except Exception, err:
        print err
        print i

    finally:
        result_df.to_csv(result_df_path, encoding='utf8')


if __name__ == '__main__':
    # pool = pathos.multiprocessing.ProcessingPool(4)
    # df_names = ['comments_part_1.csv', 'comments_part_3.csv',
    #             'comments_part_2.csv', 'comments_part_4.csv']
    #
    # pool.map(process_df, df_names)
    # check_string = "ameliorer la communication reguliere et la transparence a tous les niveaux de l'organisation."
    # try:
    #     print query_sentiment_infomation(check_string,
    #                                  credential_path='/Users/warn/Documents/RAForWangZG/GoogleNLP/wangyouan3-c44912dbac7f.json')
    #
    # except Exception, err:
    #     print 'language' in str(err)
    #     print str(err)
    #     raise Exception(err)
    process_df(os.path.join(PARENT_PATH, RESULT_PATH, 'all_commun.csv'),
               os.path.join(PARENT_PATH, RESULT_PATH, 'google_nlp_result.csv'),
               process_num=16)
