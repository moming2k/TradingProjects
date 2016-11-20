#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: format_csv_file
# Author: Mark Wang
# Date: 20/11/2016

import os

import pandas as pd
import numpy as np

ind_vars = ['prosComNum1k', 'advComNum1k', 'allComNum1k', 'consComNum1k']
path = '/home/wangzg/Documents/WangYouan/research/Glassdoor'
data_path = '20161119new_dep_var'
output_path = 'result'


dd_df = pd.read_csv(os.path.join(path, data_path, 'dd_commun.csv'),
                    dtype={'fyear': str, 'gvkey': str, 'sic2': str})

dd_df = dd_df.dropna(subset=ind_vars, how='all')
dd_df = dd_df.dropna(subset=['sic2'])
dd_df['fyear'] = dd_df['fyear'].apply(lambda x: int(x) if x else np.nan)
dd_df['sic2'] = dd_df['sic2'].apply(lambda x: int(x) if x else np.nan)

dep_vars = ['da', 'da_cfo', 'da_btm', 'absda', 'absda_cfo', 'absda_btm', 'da_win', 'da_win_cfo', 'da_win_btm',
            'absda_win', 'absda_win_cfo', 'absda_win_btm', 'da_ff48', 'da_ff48_cfo', 'da_ff48_btm', 'absda_ff48',
            'absda_ff48_cfo', 'absda_ff48_btm', 'da_ff48_win', 'da_ff48_win_cfo', 'da_ff48_win_btm', 'absda_ff48_win',
            'absda_ff48_win_cfo', 'absda_ff48_win_btm', 'resid', 'resid_loss', 'resid_loss_spi', 'resid_cfo',
            'absresid', 'absresid_loss', 'absresid_loss_spi', 'absresid_cfo', 'resid_std', 'resid_loss_std',
            'resid_lossspi_std', 'resid_cfo_std', 'resid_stddec', 'resid_loss_stddec', 'resid_lossspi_stddec',
            'resid_cfo_stddec', 'resid_win', 'resid_win_loss', 'resid_win_loss_spi', 'resid_win_cfo', 'absresid_win',
            'absresid_win_loss', 'absresid_win_loss_spi', 'absresid_win_cfo', 'resid_win_std', 'resid_win_loss_std',
            'resid_win_lossspi_std', 'resid_win_cfo_std', 'resid_win_stddec', 'resid_win_loss_stddec',
            'resid_win_lossspi_stddec', 'resid_win_cfo_stddec']

dd_dep_vars = []

dd_keys = dd_df.keys()

for key in dd_keys:
    if key in dep_vars:
        dd_dep_vars.append(key)

    elif key.lower() in dep_vars:
        dd_dep_vars.append(key)

print dd_dep_vars

da_df = pd.read_csv(os.path.join(path, data_path, 'da_commun.csv'),
                    dtype={'fyear': str, 'gvkey': str, 'sic2': str})

da_df = da_df.dropna(subset=ind_vars, how='all')
dd_df = dd_df.dropna(subset=['sic2'])
da_df['fyear'] = da_df['fyear'].apply(int)
da_df['sic2'] = da_df['sic2'].apply(int)

da_dep_vars = []

da_keys = da_df.keys()

for key in da_keys:
    if key in dep_vars or key.lower() in dep_vars:
        da_dep_vars.append(key)

print da_dep_vars

da_df.to_csv(os.path.join(path, output_path, 'da_commun_dropna.csv'), index=False)
dd_df.to_csv(os.path.join(path, output_path, 'dd_commun_dropna.csv'), index=False)

set(map(lambda x: x.lower(), da_dep_vars)).union(dd_dep_vars).difference(dep_vars)

da_df.to_stata(os.path.join(path, output_path, 'da_commun_dropna.dta'), write_index=False)
dd_df.to_stata(os.path.join(path, output_path, 'dd_commun_dropna.dta'), write_index=False)