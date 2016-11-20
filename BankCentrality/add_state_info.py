#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_state_info
# Author: Mark Wang
# Date: 20/11/2016

import os

import pandas as pd
import numpy as np

path = '/home/wangzg/Documents/WangYouan/research/BankCentrality'
data_path = 'data'
result_path = 'result'

state_df = pd.read_excel(os.path.join(path, data_path, '20151225USPubBankMnAName.xlsx'), index_col=0)
origin_df = pd.read_stata(os.path.join(path, result_path, 'Car_Centrality_dropna.dta'))

# state_df = state_df[[u'Acquirer\n CUSIP', u'Acquirer State', u'Year']]
state_df['AcquirerCUSIP'] = state_df['Acquirer\n CUSIP']
del state_df['Acquirer\n CUSIP']


def find_acquirer_state(cusip):
    tmp = state_df[state_df['AcquirerCUSIP'] == cusip]
    if tmp.empty:
        tmp = state_df[state_df['Target\nCUSIP'] == cusip]
        if tmp.empty:
            return np.nan
        else:
            return tmp['Target State'].tolist()[0]
    else:
        return tmp['Acquirer State'].tolist()[0]


origin_df['AcquirerState'] = origin_df['AcquirerCUSIP'].apply(find_acquirer_state)
origin_df.to_csv(os.path.join(path, result_path, 'Car_Centrality_add_state.csv'), index=False)
origin_df.to_stata(os.path.join(path, result_path, 'Car_Centrality_add_state.dta'), write_index=False)
