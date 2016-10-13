#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: sentiment-analysis
# Author: Mark Wang
# Date: 12/10/2016

import os

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


if __name__ == '__main__':
    df = pd.read_csv(os.path.join(PARENT_PATH, RESULT_PATH, r'review_commun.csv'),
                     usecols=['prosCommun', 'consCommun', 'adviceCommun', 'allCommun'],
                     nrows=100)
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

    except Exception, err:
        print err
        print i

    finally:
        result_df.to_csv(result_df_path, encoding='utf8')
