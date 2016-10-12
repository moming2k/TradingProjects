#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: count_string_info
# Author: Mark Wang
# Date: 12/10/2016

import os

import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer

from utils import multi_process_df, count_target_num, reformat_para

output_path = 'output'
stemmer = PorterStemmer()

CHAR_NUMBER = 'NumChar'
WORD_NUMBER = 'NumWord'
SENTENCE_NUMBER = 'NumSent'
COMMUN_NUMBER = 'NumCommun'


def get_string_characteristics(row):
    col_info = {}
    for col_name in ["pros", "cons", "adviceToManager"]:
        sentences = reformat_para(row[col_name])
        if col_name == 'adviceToManager':
            col_name = 'advice'
        new_key_1 = '{}{}'.format(col_name, CHAR_NUMBER)
        new_key_2 = '{}{}'.format(col_name, WORD_NUMBER)
        new_key_3 = '{}{}'.format(col_name, SENTENCE_NUMBER)
        new_key_4 = '{}{}'.format(col_name, COMMUN_NUMBER)
        col_info[new_key_1] = len(sentences)
        word_tokens = word_tokenize(sentences)
        col_info[new_key_2] = len(word_tokens)
        col_info[new_key_3] = len(sent_tokenize(sentences))
        col_info[new_key_4] = count_target_num(map(stemmer.stem, word_tokens), 'commun')

    for col_name in ["prosCommun", "consCommun", "adviceCommun"]:
        new_key_1 = '{}{}'.format(col_name, CHAR_NUMBER)
        new_key_2 = '{}{}'.format(col_name, WORD_NUMBER)
        new_key_3 = '{}{}'.format(col_name, SENTENCE_NUMBER)
        new_key_4 = '{}{}'.format(col_name, COMMUN_NUMBER)
        sentences = row[col_name]
        if not hasattr(sentences, 'replace'):
            sentences = ''
        col_info[new_key_1] = len(sentences)
        word_tokens = word_tokenize(sentences)
        col_info[new_key_2] = len(word_tokens)
        col_info[new_key_3] = len(sent_tokenize(sentences))
        col_info[new_key_4] = count_target_num(map(stemmer.stem, word_tokens), 'commun')

    for suffix in [CHAR_NUMBER, WORD_NUMBER, SENTENCE_NUMBER, COMMUN_NUMBER]:
        col_info['all{}'.format(suffix)] = 0
        for prefix in ["pros", "cons", "advice"]:
            col_info['all{}'.format(suffix)] += col_info['{}{}'.format(prefix, suffix)]

    return pd.Series(col_info)


def compute_file_info(df):
    new_df = df.apply(get_string_characteristics, axis=1)
    return pd.concat([df, new_df], axis=1)


if __name__ == '__main__':
    process_num = 18

    source_file = pd.read_csv(os.path.join(output_path, 'review_commun.csv'),
                              # usecols=['pros', 'cons', 'adviceToManager'],
                              nrows=100
                              )
    output_df = multi_process_df(process_num, source_file, compute_file_info)
    output_df.to_csv(os.path.join(output_path, 'review_commun_basic_str_character.csv'), index=False, encoding='utf8')
