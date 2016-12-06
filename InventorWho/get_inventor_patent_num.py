#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: get_inventor_patent_num
# @Date: 2016-12-05
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os

import pandas as pd
# import numpy as np
# import pathos

root_path = '/home/wangzg/Documents/WangYouan/research/InventorWho'
process_num = 4

result_path = os.path.join(root_path, 'result')

data_path = os.path.join(root_path, 'data')

raw_inventor = pd.read_sas(os.path.join(data_path, 'grant_rawinventor.sas7bdat'))
# us_patent_citation = pd.read_sas(os.path.join(data_path, 'grant_uspatentcitation_selected.sas7bdat'))
# inv_pat_fleming = pd.read_sas(os.path.join(data_path, 'invpat_fleming_20120724.sas7bdat'))

groups = raw_inventor.groupby('inventor_id')
patent_count = groups.count()['patent_id'].to_frame('patent_num')
patent_count.loc[:, 'name_last'] = None
patent_count.loc[:, 'last_name'] = None

patent_count = patent_count[patent_count.patent_num>20]


# def process_index(index):
for inventor_id in patent_count.index:
    df = groups.get_group(inventor_id)
    patent_count[inventor_id, 'name_last'] = df.head(1).to_dict()[u'name_last'].values()[0]
    patent_count[inventor_id, 'name_first'] = df.head(1).to_dict()[u'name_first'].values()[0]

# return None


# split_index = np.array_split(patent_count.index, process_num)

# pool = pathos.multiprocessing.ProcessingPool(process_num)
# pool.map(process_index, split_index)

patent_count.to_csv(os.path.join(result_path, 'patent_count.csv'))
patent_count.to_pickle(os.path.join(result_path, 'patent_count.p'))
