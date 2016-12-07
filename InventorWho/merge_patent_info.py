#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: merge_inv_fleming_citation
# @Date: 2016-12-06
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from functions import str2int, format_inventor_year

root_path = '/home/wangzg/Documents/WangYouan/research/InventorWho'
data_path = os.path.join(root_path, 'data')
citation_result_path = os.path.join(root_path, 'citation_result')
patent_count_result_path = os.path.join(root_path, 'result')


citation_df = pd.read_pickle(os.path.join(citation_result_path, 'inventorYearCitationImmigrate.p'))

inventor_year_df = pd.read_csv(os.path.join(data_path, 'inventorYearCitationImmigrate.csv'),
                               dtype={'year': int, 'patent_id': int})
inventor_year_df = inventor_year_df[['patent_id', 'year', 'permno']]
inventor_year_df['appyear'] = inventor_year_df['year'].apply(format_inventor_year)
inventor_year_df['permno'] = inventor_year_df['permno'].apply(str2int)

# organize data in patent
patent_zigan_df = pd.read_sas(os.path.join(data_path, 'patent_to_zigan2015116.sas7bdat'))
patent_zigan_df['patent_id'] = patent_zigan_df['patnum'].apply(str2int)
patent_zigan_df['permno'] = patent_zigan_df['permno'].apply(str2int)
patent_zigan_df['appyear'] = patent_zigan_df['appyear'].apply(str2int)

patent_zigan_df = patent_zigan_df[['patent_id', 'permno', 'appyear']]
