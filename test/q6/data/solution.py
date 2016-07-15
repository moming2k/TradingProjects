#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: q6
# Author: Mark Wang
# Date: 13/7/2016

from multiprocessing import Pool

import pandas
import numpy as np
from fuzzywuzzy.fuzz import *
from fuzzywuzzy import process
import fuzzywuzzy.utils as utils

bank_names = pandas.read_csv('bank_names.csv', index_col=0)
bank_names_series = bank_names[bank_names.keys()[0]]


def naive_metric_score(s1, s2):
    """
    Return a measure of the sequences' similarity between 0 and 100,
    using different algorithms.

    Copy from fuzzywuzzy package, the only difference here is instead max(results) with sum(results) / 4
    """
    force_ascii = True
    p1 = utils.full_process(s1, force_ascii=force_ascii)
    p2 = utils.full_process(s2, force_ascii=force_ascii)

    if not utils.validate_string(p1):
        return 0
    if not utils.validate_string(p2):
        return 0

    # should we look at partials?
    try_partial = True
    unbase_scale = .95
    partial_scale = .90

    base = ratio(p1, p2)
    len_ratio = float(max(len(p1), len(p2))) / min(len(p1), len(p2))

    # if strings are similar length, don't use partials
    if len_ratio < 1.5:
        try_partial = False

    # if one string is much much shorter than the other
    if len_ratio > 8:
        partial_scale = .6

    if try_partial:
        partial = partial_ratio(p1, p2) * partial_scale
        ptsor = partial_token_sort_ratio(p1, p2, full_process=False) \
                * unbase_scale * partial_scale
        ptser = partial_token_set_ratio(p1, p2, full_process=False) \
                * unbase_scale * partial_scale

        return int(round(sum([base, partial, ptser, ptsor]) / 4.0))
    else:
        tsor = token_sort_ratio(p1, p2, full_process=False) * unbase_scale
        tser = token_set_ratio(p1, p2, full_process=False) * unbase_scale

        return int(round(sum([base, tser, tsor]) / 3.0))


def find_top10_matcher(row):
    result_tuple = process.extractBests(row, bank_names_series, scorer=naive_metric_score, limit=10)
    result_list = [(str(i), j[0]) for i, j in enumerate(result_tuple)]
    return pandas.Series({i[0]: i[1] for i in result_list})


def process_df(df):
    return df['Acquirer Name'].apply(find_top10_matcher)


if __name__ == "__main__":

    # As my computer has four cores
    process_number = 4
    pool = Pool(processes=process_number)

    # Load data
    activities = pandas.read_excel('acquirers.xlsx', index_col='Index')

    # Split big df to 4 splits
    split_dfs = np.array_split(activities, process_number)
    pool_results = pool.map(process_df, split_dfs)
    right_df = pandas.concat(pool_results, axis=0)
    left_df = pandas.DataFrame()
    left_df['acquirers'] = activities['Acquirer Name']
    df = pandas.merge(left_df, right_df, left_index=True, right_index=True)
    df.to_csv('output.csv')
