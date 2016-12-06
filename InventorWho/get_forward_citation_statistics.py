#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: get_forward_citation_statistics
# @Date: 2016-12-06
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

root_path = '/home/wangzg/Documents/WangYouan/research/InventorWho'

data_path = os.path.join(root_path, 'data')

result_path = os.path.join(root_path, 'citation_result')
patent_count_result_path = os.path.join(root_path, 'result')

# generate forward_citation_count
# forward_citation_count = pd.read_csv(os.path.join(data_path, 'inventorYearCitationImmigrate.csv'),
#                                      dtype={'patent_id': int, 'year': int})
#
# forward_citation_count['forwardCitationCountToSampleEnd'] = forward_citation_count[
#     'forwardCitationCountToSampleEnd'].apply(int)
#
# forward_citation_count.to_pickle(os.path.join(result_path, 'inventorYearCitationImmigrate.p'))

forward_citation_count = pd.read_pickle(os.path.join(result_path, 'inventorYearCitationImmigrate.p'))
patent_count = pd.read_pickle(os.path.join(patent_count_result_path, 'inventor_patent_count.p'))

inventor_citation = forward_citation_count[['inventor_id', 'forwardCitationCountToSampleEnd']]
groups = inventor_citation.groupby('inventor_id')

keys = groups.groups.keys()

patent_count.loc[:, 'fc_greater_1'] = 0
patent_count.loc[:, 'fc_greater_5'] = 0
patent_count.loc[:, 'fc_greater_10'] = 0
patent_count.loc[:, 'fc_greater_20'] = 0
patent_count.loc[:, 'fc_greater_50'] = 0
patent_count.loc[:, 'fc_greater_100'] = 0

for inventor_id in patent_count.index:
    if inventor_id not in keys:
        continue

    df = groups.get_group(inventor_id)

    for citation_num in [1, 5, 10, 20, 50, 100]:
        patent_count.loc[inventor_id, 'fc_greater_{}'.format(citation_num)] = \
            df[df.forwardCitationCountToSampleEnd > citation_num].shape[0]

patent_count.to_csv(os.path.join(result_path, 'forward_citation_count.csv'))
patent_count.to_pickle(os.path.join(result_path, 'forward_citation_count.p'))
