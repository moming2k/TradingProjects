#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: get_fc_10_p_10_inventors
# Author: warn
# Date: warn

import os

import pandas as pd

root_path = '/home/wangzg/Documents/WangYouan/research/InventorWho'

data_path = os.path.join(root_path, 'data')

result_path = os.path.join(root_path, 'citation_result')
tmp_path = os.path.join(root_path, 'temp')
patent_count_result_path = os.path.join(root_path, 'result')

forward_citation_count = pd.read_csv(os.path.join(data_path, 'inventorYearCitationImmigrate.csv'),
                                     dtype={'patent_id': int, 'year': int}
                                     )

forward_citation_count['forwardCitationCountToSampleEnd'] = forward_citation_count[
    'forwardCitationCountToSampleEnd'].apply(int)

groups = forward_citation_count[forward_citation_count.forwardCitationCountToSampleEnd > 10].groupby('inventor_id')
fc_count = groups.count()

forward_citation_count.sort_values('year', inplace=True)

df = forward_citation_count.drop_duplicates(subset='inventor_id', keep='last').set_index('inventor_id')
df = df[['patent_id', 'state', 'permno', 'year']]
df['patent_num'] = fc_count['patent_id']
df['state'] = df['state'].apply(lambda x: x.upper() if hasattr(x, 'upper') else x)

merged_join_df = pd.read_pickle(os.path.join(tmp_path, 'merged_join.p'))
# merged_join_groups = merged_join_df.groupby('inventor_id')

new_df = merged_join_df[merged_join_df.forwardCitationCountToSampleEnd > 10].sort_values(
    'year').drop_duplicates('inventor_id', keep='last').set_index('inventor_id')

name_df = df.merge(new_df[['name_first', 'name_last', 'zipcode', 'city', 'country']], left_index=True, right_index=True,
                   how='left')

has_state_df = merged_join_df.dropna(subset=['state']).drop_duplicates('inventor_id').set_index('inventor_id')
name_df['state'] = name_df['state'].fillna(has_state_df['state'])

has_name_df = merged_join_df.dropna(subset=['name_last']).drop_duplicates('inventor_id').set_index('inventor_id')
name_df['name_last'] = name_df['name_last'].fillna(has_name_df['name_last'])
name_df['name_first'] = name_df['name_first'].fillna(has_name_df['name_first'])

name_df.index.name = 'inventor_id'
df_10 = name_df[name_df.patent_num > 10]
df_5 = name_df[name_df.patent_num > 5]

df_10.to_pickle(os.path.join(tmp_path, 'inventor_p_10_fc_10.p'))
df_5.to_pickle(os.path.join(tmp_path, 'inventor_p_5_fc_10.p'))

df_10.to_csv(os.path.join(result_path, 'inventor_p_10_fc_10.csv'))
df_5.to_csv(os.path.join(result_path, 'inventor_p_5_fc_10.csv'))
