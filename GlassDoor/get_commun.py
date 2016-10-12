#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: get_commun
# Author: Mark Wang
# Date: 12/10/2016

import re

import pandas as pd
import numpy as np
import pathos.multiprocessing as process
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()


def get_commun_sentence(sentences):
    if not hasattr(sentences, 'lower'):
        return None
    sentences = sentences.decode("utf8")
    sentences = sentences.replace('\r\n', '.')
    sentences = re.sub(r'[.]+', '. ', sentences)
    sentences = re.sub(r'[ ]+', ' ', sentences)
    sentence_list = sent_tokenize(sentences.lower())
    result_list = []
    for sentence in sentence_list:
        stem_set = set(map(stemmer.stem, word_tokenize(sentence)))
        if 'commun' in stem_set:
            result_list.append(sentence)

    return ' '.join(result_list) if result_list else None


def get_all_commun(row):
    result = [row['prosCommun'], row['consCommun'], row['adviceCommun']]
    while None in result:
        result.remove(None)

    return ' '.join(result) if result else None


def get_commun(df):
    df['prosCommun'] = df['pros'].apply(get_commun_sentence)
    df['consCommun'] = df['cons'].apply(get_commun_sentence)
    df['adviceCommun'] = df['adviceToManager'].apply(get_commun_sentence)
    df['allCommun'] = df.apply(get_all_commun, axis=1)

    return df


if __name__ == '__main__':
    process_num = 18

    pool = process.ProcessingPool(process_num)
    source_file = pd.read_csv('Ruoyan_review_4.csv', usecols=['pros', 'cons', 'adviceToManager'],
                              nrows=100)

    split_dfs = np.array_split(source_file, process_num)
    result_dfs = pool.map(get_commun, split_dfs)
    pd.concat(result_dfs, axis=0).to_csv("review_commun.csv", index=False, encoding='utf8')
