#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: merge_inv_fleming_citation
# @Date: 2016-12-06
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd
import numpy as np

from functions import str2int

root_path = '/home/wangzg/Documents/WangYouan/research/InventorWho'
data_path = os.path.join(root_path, 'data')
tmp_path = os.path.join(root_path, 'temp')
citation_result_path = os.path.join(root_path, 'citation_result')
patent_count_result_path = os.path.join(root_path, 'result')

citation_df = pd.read_csv(os.path.join(data_path, 'inventorYearCitationImmigrate.csv'),
                          dtype={'year': int, 'patent_id': int})
citation_df = citation_df[['patent_id', 'year', 'permno', 'state', 'forwardCitationCountToSampleEnd', 'inventor_id']]
citation_df = citation_df[citation_df.year < 2017]
citation_df['permno'] = citation_df['permno'].apply(str2int)
citation_df.loc[citation_df.state.notnull(), 'country'] = 'US'
citation_df.loc[citation_df.state.notnull(), 'state'] = citation_df[citation_df.state.notnull()].state.apply(
    lambda x: x.toupper())
citation_df.to_pickle(os.path.join(tmp_path, 'citation.p'))

invent_fleming_df = pd.read_sas(os.path.join(data_path, 'invpat_fleming_20120724.sas7bdat'))
invent_fleming_df = invent_fleming_df[['Firstname', 'Lastname', 'Street', u'AppYear', u'Invnum', u'Patent', 'City',
                                       'State', 'Country', 'Zipcode']]
invent_fleming_df = invent_fleming_df[invent_fleming_df.Patent.notnull()]
invent_fleming_df = invent_fleming_df[invent_fleming_df.Invnum.notnull()]

invent_fleming_df.loc[:, 'name_first'] = invent_fleming_df['Firstname']
invent_fleming_df.loc[:, 'name_last'] = invent_fleming_df['Lastname']
invent_fleming_df.loc[:, 'street'] = invent_fleming_df['Street']
invent_fleming_df.loc[:, 'state'] = invent_fleming_df['State']
invent_fleming_df.loc[:, 'country'] = invent_fleming_df['Country'].app
invent_fleming_df.loc[:, 'zipcode'] = invent_fleming_df['Zipcode']
invent_fleming_df.loc[:, 'year'] = invent_fleming_df['AppYear']
invent_fleming_df.loc[:, 'city'] = invent_fleming_df['City']
invent_fleming_df.loc[:, 'patent_id'] = invent_fleming_df['Patent'].apply(int)
invent_fleming_df.loc[:, 'inventor_id'] = invent_fleming_df['Invnum'].apply(lambda x: x[1:])

invent_fleming_df.drop(['Firstname', 'Lastname', 'Street', u'AppYear', u'Invnum', u'Patent', 'City', 'State',
                        'Country', 'Zipcode'], axis=1, inplace=True)
invent_fleming_df.to_pickle(os.path.join(tmp_path, 'invent_fleming.p'))

merged_df = invent_fleming_df.merge(citation_df, how='outer', on=['patent_id', 'inventor_id'], suffixes=['_f', '_c'])

for key in ['year', 'country', 'state']:
    merged_df[key] = merged_df['{}_f'.format(key)].fillna(merged_df['{}_c'.format(key)])
    merged_df.drop(['{}_f'.format(key), '{}_c'.format(key)], axis=1, inplace=True)

merged_df['permno'] = merged_df.permno.apply(str2int)
merged_df['forwardCitationCountToSampleEnd'] = merged_df.forwardCitationCountToSampleEnd.apply(str2int)
merged_df['year'] = merged_df.year.apply(str2int)
merged_df.to_pickle(os.path.join(tmp_path, 'merged.p'))

merged_df = pd.read_pickle(os.path.join(tmp_path, 'merged.p'))
groups = merged_df.groupby('inventor_id')

raw_inventor_df = pd.read_sas(os.path.join(data_path, 'grant_rawinventor.sas7bdat'))
raw_inventor_df.drop(['uuid', 'sequence'], axis=1, inplace=True)
line_len = raw_inventor_df['rawlocation_id'].apply(lambda x: len(x.split('|')))
raw_inventor_df['state'] = raw_inventor_df[line_len == 3]['rawlocation_id'].apply(lambda x: x.split('|')[1].upper())
raw_inventor_df['country'] = raw_inventor_df[line_len == 3]['rawlocation_id'].apply(lambda x: x.split('|')[2].upper())
raw_inventor_df['city'] = raw_inventor_df[line_len == 3]['rawlocation_id'].apply(lambda x: x.split('|')[0])
raw_inventor_df.drop(['rawlocation_id'], axis=1, inplace=True)
merged_join_df = merged_df.merge(raw_inventor_df, how='left', on=['inventor_id', 'patent_id'], suffixes=['', '_raw'])

for key in ['state', 'country', 'name_last', 'name_first', 'city']:
    merged_join_df[key] = merged_join_df[key].fillna(merged_join_df['{}_raw'.format(key)])
    del merged_join_df['{}_raw'.format(key)]
merged_join_df = merged_join_df.sort_values('year')
merged_join_df.to_pickle(os.path.join(tmp_path, 'merged_join.p'))

merged_join_df = pd.read_pickle(os.path.join(tmp_path, 'merged_join.p'))


def process_df(keys):
    patent_count = pd.DataFrame(columns=['name_last', 'name_first', 'patent_num', 'fc_gt_1',
                                         'fc_gt_5', 'fc_gt_10', 'fc_gt_20', 'fc_gt_50', 'fc_gc_100', 'patent_coverage',
                                         'first_patent_year', 'first_city', 'last_city', 'last_patent_year'])

    merged_join_groups = merged_join_df.groupby('inventor_id')

    for inventor_id in keys:

        df = merged_join_groups.get_group(inventor_id)
        result_dict = {'fc_gt_5': df[df[u'forwardCitationCountToSampleEnd'] > 5].shape[0],
                       'fc_gt_1': df[df[u'forwardCitationCountToSampleEnd'] > 1].shape[0],
                       'fc_gt_10': df[df[u'forwardCitationCountToSampleEnd'] > 10].shape[0],
                       'fc_gt_20': df[df[u'forwardCitationCountToSampleEnd'] > 20].shape[0],
                       'fc_gt_50': df[df[u'forwardCitationCountToSampleEnd'] > 50].shape[0],
                       'fc_gt_100': df[df[u'forwardCitationCountToSampleEnd'] > 100].shape[0],
                       'patent_num': df.shape[0],
                       }
        year_series = map(int, df.year.dropna().tolist())
        if len(year_series) > 0:
            year_set = set(year_series)
            result_dict['first_patent_year'] = year_series[0]
            result_dict['last_patent_year'] = year_series[-1]
            result_dict['patent_coverage'] = float(len(year_series)) / float(len(year_set))
        else:
            result_dict['first_patent_year'] = np.nan
            result_dict['last_patent_year'] = np.nan
            result_dict['patent_coverage'] = np.nan

        city_series = df.city.dropna().tolist()
        if len(city_series) > 0:
            result_dict['first_city'] = city_series[0]
            result_dict['last_city'] = city_series[-1]
        else:
            result_dict['first_city'] = np.nan
            result_dict['last_city'] = np.nan

        first_name = df.name_first.dropna().tolist()
        last_name = df.name_last.dropna().tolist()
        if first_name:
            result_dict['name_first'] = first_name[0]
        else:
            result_dict['name_first'] = np.nan
        if last_name:
            result_dict['name_last'] = last_name[0]
        else:
            result_dict['name_last'] = np.nan
        patent_count.loc[inventor_id] = result_dict

    return patent_count
