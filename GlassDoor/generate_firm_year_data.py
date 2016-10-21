#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: generate_firm_year_data
# Author: Mark Wang
# Date: 21/10/2016

import os

import numpy as np
import pandas as pd
import pathos

path = '/home/wangzg/Documents/WangYouan/research/Glassdoor'
input_path = 'input_data'
output_path = 'output'
result_path = 'result'

df = pd.read_csv(os.path.join(path, result_path, 'glassdoor_indicators_addPolMag.csv'),
                 dtype={'FK_employerId': str, 'FK_dateId': str, 'commentYear': str})
df_groups = df.groupby(by=['FK_employerId', 'commentYear'])

columns = ['FK_employerId', 'commentYear']
for prefix in ['pros', 'cons', 'advice', 'all', 'netProsCons', 'netProsConsAdvice']:
    if prefix in {'pros', 'cons', 'all', 'advice'}:
        columns.append('{}Num'.format(prefix))
        columns.append('{}CommunNum'.format(prefix))

    for middle in ['Pol', 'PolMag']:
        for suffix in ['simple', 'CommunNumChar', 'CommunNumCommun', 'CommunNumSent',
                       'CommunNumWord', 'NumChar', 'NumCommun', 'NumSent', 'NumWord']:
            if suffix == 'simple':
                columns.append('{}CommunGNLP{}_firmYear_simple'.format(prefix, middle))
            else:
                columns.append('{0}CommunGNLP{1}_firmYear_{0}Commun{2}_sum'.format(prefix, middle, suffix))
                columns.append('{0}CommunGNLP{1}_firmYear_{0}Commun{2}_averageAll'.format(prefix, middle, suffix))
                columns.append(
                    '{0}CommunGNLP{1}_firmYear_{0}Commun{2}_averageCommun'.format(prefix, middle, suffix))


def process_df(group_keys):
    grouped_df = pd.DataFrame(columns=columns)
    index = 0
    for name in group_keys:
        group = df_groups.get(name)
        row_info = {
            'FK_employerId': name[0],
            'commentYear': name[1],
        }
        for prefix in ['pros', 'cons', 'advice', 'all', 'netProsCons', 'netProsConsAdvice']:
            if prefix in {'pros', 'cons'}:
                row_info['{}Num'.format(prefix)] = group[prefix].count()
                row_info['{}CommunNum'.format(prefix)] = group['{}Commun'.format(prefix)].count()

            elif prefix == 'advice':
                row_info['{}Num'.format(prefix)] = group['adviceToManager'].count()
                row_info['{}CommunNum'.format(prefix)] = group['{}Commun'.format(prefix)].count()
            elif prefix == 'all':
                row_info['allNum'] = group.shape[0]
                row_info['allCommunNum'] = group['allCommun'].count()

            for middle in ['Pol', 'PolMag']:
                row_info['{}CommunGNLP{}_firmYear_simple'.format(prefix, middle)] = \
                    sum(group['{}CommunGNLP{}'.format(prefix, middle)])
                for suffix in ['CommunNumChar', 'CommunNumCommun', 'CommunNumSent', 'CommunNumWord', 'NumChar',
                               'NumCommun', 'NumSent', 'NumWord']:
                    prefix_name = '{0}CommunGNLP{1}_firmYear_{0}{2}'.format(prefix, middle, suffix)
                    if prefix.startswith('net'):
                        row_info['{}_sum'.format(prefix_name)] = \
                            sum(group['{}CommunGNLP{}'.format(prefix, middle)] * group['all{}'.format(suffix)])
                        row_info['{}_averageCommun'.format(prefix_name)] = \
                            row_info['{}_sum'.format(prefix_name)] / row_info['allCommunNum']
                        row_info['{}_averageAll'.format(prefix_name)] = \
                            row_info['{}_sum'.format(prefix_name)] / row_info['allNum']
                    else:
                        row_info['{}_sum'.format(prefix_name)] = \
                            sum(group['{}CommunGNLP{}'.format(prefix, middle)] * group['{}{}'.format(prefix, suffix)])
                        row_info['{}_averageCommun'.format(prefix_name)] = \
                            row_info['{}_sum'.format(prefix_name)] / row_info['{}CommunNum'.format(prefix)]
                        row_info['{}_averageAll'.format(prefix_name)] = \
                            row_info['{}_sum'.format(prefix_name)] / row_info['{}Num'.format(prefix)]

        # print row_info.keys()
        grouped_df.loc[index] = row_info
        index += 1

    return grouped_df


if __name__ == '__main__':
    # print columns

    process_num = 15
    pool = pathos.multiprocessing.ProcessingPool(process_num)

    split_names = np.array_split(df_groups.groups.keys(), process_num)
    result_dfs = pool.map(process_df, split_names)
    result_df = pd.concat(result_dfs, axis=0, ignore_index=True)
    result_df.to_csv('firm_year_statistics2.csv', encoding='utf8', index=False)
