#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: generate_fiscal_year_info
# Author: Mark Wang
# Date: 6/11/2016

import os
import datetime
from dateutil.relativedelta import relativedelta

import numpy as np
import pandas as pd
import pathos

path = '/home/wangzg/Documents/WangYouan/research/Glassdoor'
input_path = 'input_data'
output_path = 'output'
result_path = 'result'

df = pd.read_csv(os.path.join(path, result_path, 'glassdoor_indicators_addPolMag.csv'),
                 dtype={'FK_employerId': str, 'FK_dateId': str})

df['FK_dateId'] = df['FK_dateId'].apply(lambda x: datetime.datetime.strptime(x, '%Y%m%d'))
fiscal_year_data = pd.read_csv(os.path.join(path, output_path, 'cf_dd_merged.csv'),
                               usecols=['datadate', 'gdid', 'fyear'],
                               dtype={'datadate': str, 'gdid': str, 'fyear': str})
fiscal_year_data['datadate'] = fiscal_year_data['datadate'].apply(lambda x: datetime.datetime.strptime(x, '%Y%m%d'))

del df['commentYear']


def get_fiscal_year(row):
    comment_date = row['FK_dateId']
    gdid = row['FK_employerId']
    tmp = fiscal_year_data[fiscal_year_data['gdid'] == gdid]
    if tmp.empty:
        return np.nan

    tmp = tmp[tmp['datadate'] >= comment_date]
    if tmp.empty:
        return np.nan

    fiscal_year = tmp.ix[tmp.index[0], 'datadate']
    one_year_before = fiscal_year - relativedelta(years=1)
    if one_year_before < comment_date <= fiscal_year:
        return tmp['fyear'].tolist()[0]
    else:
        return np.nan


df['fiscalYear'] = df.apply(get_fiscal_year, axis=1)
df = df.dropna(subset=['fiscalYear'], how='any')
df.to_csv(os.path.join(path, result_path, 'glassdoor_indicators_addFYear.csv'), index=False,
          encoding='utf8')
df_groups = df.groupby(['FK_employerId', 'fiscalYear'])
columns = ['FK_employerId', 'fiscalYear']
for prefix in ['pros', 'cons', 'advice', 'all', 'netProsCons', 'netProsConsAdvice']:
    if prefix in {'pros', 'cons', 'all', 'advice'}:
        columns.append('{}Num'.format(prefix))
        columns.append('{}CommunNum'.format(prefix))

    for middle in ['Pol', 'PolMag']:
        columns.append('{}CommunGNLP{}_firmYear_simple'.format(prefix, middle))
        for suffix in ['CommunNumChar', 'CommunNumCommun', 'CommunNumSent',
                       'CommunNumWord', 'NumChar', 'NumCommun', 'NumSent', 'NumWord']:
            columns.append('{0}CommunGNLP{1}_firmYear_{0}{2}_sum'.format(prefix, middle, suffix))
            columns.append('{0}CommunGNLP{1}_firmYear_{0}{2}_averageAll'.format(prefix, middle, suffix))
            columns.append(
                '{0}CommunGNLP{1}_firmYear_{0}{2}_averageCommun'.format(prefix, middle, suffix))


def process_df(group_keys):
    grouped_df = pd.DataFrame(columns=columns)
    index = 0
    # print group_keys
    for name in group_keys:
        group = df_groups.get_group(tuple(name))
        row_info = {
            'FK_employerId': name[0],
            'fiscalYear': name[1],
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
                    group['{}CommunGNLP{}'.format(prefix, middle)].sum()
                for suffix in ['CommunNumChar', 'CommunNumCommun', 'CommunNumSent', 'CommunNumWord', 'NumChar',
                               'NumCommun', 'NumSent', 'NumWord']:
                    prefix_name = '{0}CommunGNLP{1}_firmYear_{0}{2}'.format(prefix, middle, suffix)
                    if prefix.startswith('net'):
                        row_info['{}_sum'.format(prefix_name)] = \
                            (group['{}CommunGNLP{}'.format(prefix, middle)] * group['all{}'.format(suffix)]).sum()
                        if row_info['allCommunNum'] > 0:
                            row_info['{}_averageCommun'.format(prefix_name)] = \
                                row_info['{}_sum'.format(prefix_name)] / row_info['allCommunNum']
                        else:
                            row_info['{}_averageCommun'.format(prefix_name)] = 0
                        row_info['{}_averageAll'.format(prefix_name)] = \
                            row_info['{}_sum'.format(prefix_name)] / row_info['allNum']
                    else:
                        row_info['{}_sum'.format(prefix_name)] = \
                            (group['{}CommunGNLP{}'.format(prefix, middle)]
                             * group['{}{}'.format(prefix, suffix)]).sum()
                        if row_info['{}CommunNum'.format(prefix)] > 0:
                            row_info['{}_averageCommun'.format(prefix_name)] = \
                                row_info['{}_sum'.format(prefix_name)] / row_info['{}CommunNum'.format(prefix)]
                        else:
                            row_info['{}_averageCommun'.format(prefix_name)] = np.nan

                        if row_info['{}Num'.format(prefix)] > 0:
                            row_info['{}_averageAll'.format(prefix_name)] = \
                                row_info['{}_sum'.format(prefix_name)] / row_info['{}Num'.format(prefix)]
                        else:
                            row_info['{}_averageAll'.format(prefix_name)] = np.nan

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
    result_df.to_csv(os.path.join(path, result_path, 'firm_fiscal_year_statistics_sample.csv'),
                     encoding='utf8', index=False)
