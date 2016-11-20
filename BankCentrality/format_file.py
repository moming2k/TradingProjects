#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: format_file
# Author: Mark Wang
# Date: 20/11/2016

import os

import pandas as pd
import numpy as np

path = '/home/wangzg/Documents/WangYouan/research/BankCentrality'

data_path = 'data'
result_path = 'result'

df = pd.read_csv(os.path.join(path, data_path, '20161119CAR_centrality.csv'),
                 dtype={'Year': int, 'AcquirerCUSIP': str, 'TargetCUSIP': str, 'Cash_deal_dummy': int,
                        'Stock_deal_dummy': int, 'Attitude_dummy': int, 'Tender_offer_dummy': int,
                        'Target_public_dummy': int},
                 index_col=0)

ind_var = ['all_dc', 'all_nc', 'all_nb', 'all_ec', 'all_dc_last_year', 'all_nc_last_year', 'all_nb_last_year',
           'all_ec_last_year', 'board_dc', 'board_nc', 'board_nb', 'board_ec', 'board_dc_last_year',
           'board_nc_last_year', 'board_nb_last_year', 'board_ec_last_year', 'ceochairman_dc', 'ceochairman_nc',
           'ceochairman_nb', 'ceochairman_ec', 'ceochairman_dc_last_year', 'ceochairman_nc_last_year',
           'ceochairman_nb_last_year', 'ceochairman_ec_last_year', 'ceo_dc', 'ceo_nc', 'ceo_nb', 'ceo_ec',
           'ceo_dc_last_year', 'ceo_nc_last_year', 'ceo_nb_last_year', 'ceo_ec_last_year', 'chairman_dc', 'chairman_nc',
           'chairman_nb', 'chairman_ec', 'chairman_dc_last_year', 'chairman_nc_last_year', 'chairman_nb_last_year',
           'chairman_ec_last_year']


def to_float(x):
    try:
        return float(x)
    except Exception:
        return np.nan


for var in ind_var:
    df[var] = df[var].replace(' ', np.nan)
    df[var] = df[var].apply(to_float)

df = df.dropna(subset=ind_var, how='all')

df.to_csv(os.path.join(path, result_path, 'Car_Centrality_dropna.csv'), index=False)
df.to_stata(os.path.join(path, result_path, 'Car_Centrality_dropna.dta'), write_index=False)
