#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: generate_required_parameters
# Author: Mark Wang
# Date: 20/10/2016

import os

import pandas as pd

if __name__ == '__main__':
    path = '/home/wangzg/Documents/WangYouan/research/Glassdoor'
    input_path = 'input_data'
    output_path = 'output'
    result_path = 'result'

    df = pd.read_csv(os.path.join(path, result_path, 'glassdoor_indicators_add_year.csv'),
                     dtype={'FK_employerId': str, 'FK_dateId': str, 'commentYear': str})
    # df = pd.read_csv(os.path.join(path, result_path, 'glassdoor_indicators_add_year_dropna.csv'),
    #                  index_col=0,
    #                  dtype={'FK_employerId': str, 'FK_dateId': str, 'commentYear': str})

    df['prosCommunGNLPPolMag'] = df['prosCommunGNLPPol'] * df['prosCommunGNLPMag']
    df['consCommunGNLPPolMag'] = df['consCommunGNLPPol'] * df['consCommunGNLPMag']
    df['adviceCommunGNLPPolMag'] = df['adviceCommunGNLPPol'] * df['adviceCommunGNLPMag']
    df['allCommunGNLPPolMag'] = df['allCommunGNLPPol'] * df['allCommunGNLPMag']

    df['netProsConsCommunGNLPPol'] = df['prosCommunGNLPPol'] + df['consCommunGNLPPol']
    df['netProsConsAdviceCommunGNLPPol'] = df['prosCommunGNLPPol'] + df['consCommunGNLPPol'] \
                                           + df['adviceCommunGNLPPol']
    df['netProsConsCommunGNLPPolMag'] = df['prosCommunGNLPPolMag'] + df['consCommunGNLPPolMag']
    df['netProsConsAdviceCommunGNLPPolMag'] = df['prosCommunGNLPPolMag'] + df['consCommunGNLPPolMag'] \
                                              + df['adviceCommunGNLPPolMag']

    df.to_csv(os.path.join(path, result_path, 'glassdoor_indicators_addPolMag.csv'), encoding='utf8',
              index=False)
    df_groups = df.groupby(by=['FK_employerId', 'commentYear'])

    columns = ['FK_employerId', 'commentYear']
    for prefix in ['pros', 'cons', 'advice', 'all', 'netProsCons', 'netProsConsAdvice']:
        if prefix in {'pros', 'cons', 'all', 'advice'}:
            columns.append('{}Num'.format(prefix))
            columns.append('{}CommunNum'.format(prefix))

        for middle in ['Pol', 'PolMag']:
            for suffix in ['simple', 'CommunNumChar_sum', 'CommunNumCommun_sum', 'CommunNumSent_sum',
                           'CommunNumWord_sum', 'NumChar_sum', 'NumCommun_sum', 'NumSent_sum', 'NumWord_sum']:
                if suffix == 'simple':
                    columns.append('{}CommunGNLP{}_firmYear_simple'.format(prefix, middle))
                else:
                    columns.append('{0}CommunGNLP{1}_firmYear_{0}Commun{2}'.format(prefix, middle, suffix))

    grouped_df = pd.DataFrame(columns=columns)
    index = 0
    for name, group in df_groups:
        row_info = {
            'FK_employerId': name[0],
            'commentYear': name[1],
        }
        for prefix in ['pros', 'cons', 'advice', 'all', 'netProsCons', 'netProsConsAdvice']:
            if prefix in {'pros', 'cons', 'all'}:
                row_info['{}Num'.format(prefix)] = group[prefix].count()
                row_info['{}CommunNum'.format(prefix)] = group['{}Commun'.format(prefix)].count()

            elif prefix == 'advice':
                row_info['{}Num'.format(prefix)] = group['adviceToManager'].count()
                row_info['{}CommunNum'.format(prefix)] = group['{}Commun'.format(prefix)].count()

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

        grouped_df.loc[index] = row_info
        index += 1

    grouped_df.to_csv('firm_year_statistics.csv', encoding='utf8', index=False)

