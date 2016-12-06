#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: get_inventor_patent_num
# @Date: 2016-12-05
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os

import pandas as pd

from functions import data_str2datetime

# import numpy as np
# import pathos

root_path = '/home/wangzg/Documents/WangYouan/research/InventorWho'
process_num = 4

result_path = os.path.join(root_path, 'result')

data_path = os.path.join(root_path, 'data')

raw_inventor = pd.read_sas(os.path.join(data_path, 'grant_rawinventor.sas7bdat'))
# us_patent_citation = pd.read_sas(os.path.join(data_path, 'grant_uspatentcitation_selected.sas7bdat'))
inv_pat_fleming = pd.read_sas(os.path.join(data_path, 'invpat_fleming_20120724.sas7bdat'))

groups = raw_inventor.groupby('inventor_id')
patent_count = groups.count()['patent_id'].to_frame('patent_num')
patent_count.loc[:, 'name_last'] = None
patent_count.loc[:, 'last_name'] = None

patent_count = patent_count[patent_count.patent_num > 20]

# keep one add name to patent_count
raw_inventor_first = raw_inventor.drop_duplicates(['inventor_id'], keep='first')
raw_inventor_first.drop(['uuid', 'sequence', 'patent_id'], axis=1, inplace=True)
raw_inventor_first.set_index('inventor_id', inplace=True)
raw_inventor_first = raw_inventor_first.merge(patent_count, left_index=True, right_index=True)

inv_pat_fleming_useful = inv_pat_fleming[[u'Patent', u'Invnum', u'AppDate', u'AppYear', u'GYear']]

inv_pat_fleming_useful.loc[:, 'inventor_id'] = inv_pat_fleming_useful['Invnum']
inv_pat_fleming_useful.loc[:, 'patent_id'] = inv_pat_fleming_useful['Patent']

inv_pat_fleming_useful.drop(['Invnum', 'Patent'], axis=1, inplace=True)

inv_pat_fleming_useful.dropna(how='any', inplace=True)
inv_pat_fleming_useful['AppYear'] = inv_pat_fleming_useful.AppYear.apply(int)
inv_pat_fleming_useful['GYear'] = inv_pat_fleming_useful.GYear.apply(int)
inv_pat_fleming_useful['patent_id'] = inv_pat_fleming_useful.patent_id.apply(int)
inv_pat_fleming_useful['AppDate'] = inv_pat_fleming_useful.AppDate.apply(data_str2datetime)
inv_pat_fleming_useful['inventor_id'] = inv_pat_fleming_useful.inventor_id.apply(lambda x: x[1:])

df = inv_pat_fleming_useful.sort_values('GYear').drop_duplicates(['inventor_id'], keep='first').set_index(
    'inventor_id').merge(patent_count, left_index=True, right_index=True, how='inner').sort

df.to_csv(os.path.join(result_path, 'inventor_patent_count.csv'), encoding='utf8')
df.to_pickle(os.path.join(result_path, 'inventor_patent_count.p'))

df_20 = df[df.patent_num > 20]
df_20.to_csv(os.path.join(result_path, 'inventor_patent_count_20.csv'))
df_20.to_pickle(os.path.join(result_path, 'inventor_patent_count_20.p'))

df_50 = df[df.patent_num > 50]
df_50.to_csv(os.path.join(result_path, 'inventor_patent_count_50.csv'), encoding='utf8')
df_50.to_pickle(os.path.join(result_path, 'inventor_patent_count_50.p'))

df_100 = df[df.patent_num > 100]
df_100.to_csv(os.path.join(result_path, 'inventor_patent_count_100.csv'), encoding='utf8')
df_100.to_pickle(os.path.join(result_path, 'inventor_patent_count_100.p'))
