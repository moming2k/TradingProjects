#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: count_those_inventor_more_than_100
# @Date: 2016-12-06
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd
import numpy as np

from functions import data_str2datetime

root_path = '/home/wangzg/Documents/WangYouan/research/InventorWho'

result_path = os.path.join(root_path, 'result')
data_path = os.path.join(root_path, 'data')

patent_count = pd.read_pickle(os.path.join(result_path, 'inventor_patent_count_100.p'))

inv_pat_fleming = pd.read_sas(os.path.join(data_path, 'invpat_fleming_20120724.sas7bdat'))

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

inv_pat_fleming_useful.to_pickle(os.path.join(result_path, 'inv_pat_fleming_useful.p'))

groups = inv_pat_fleming_useful.groupby('inventor_id')

keys = groups.groups.keys()

patent_count.loc[:, 'missing_year'] = 0
for inventor_id in patent_count:
    if inventor_id not in keys:
        patent_count.loc[:, 'missing_year'] = np.nan
        continue

    df = groups.get_group(inventor_id)
