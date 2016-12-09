#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_city_to_inventor
# Author: warn
# Date: warn

import os
import re

import pandas as pd

root_path = '/home/wangzg/Documents/WangYouan/research/InventorWho'

data_path = os.path.join(root_path, 'data')
tmp_path = os.path.join(root_path, 'temp')
google_data_path = os.path.join(root_path, 'GooglePatentData')
samput_data_path = os.path.join(root_path, 'SampatData')
result_path = os.path.join(root_path, 'result')

NAME_FIRST = 'name_first'
NAME_LAST = 'name_last'
INVENTOR_TEXT = 'inventor_text'


def get_city_from_inventor_text(row):
    first_name = row[NAME_FIRST]
    last_name = row[NAME_LAST]
    text = row[INVENTOR_TEXT]

    names = text.split('), ')
    next_name = []
    if hasattr(last_name, 'upper'):
        for name in names:
            if last_name.upper() in name.upper():
                next_name.append(name)

    if hasattr(first_name, 'upper'):
        if len(next_name) > 1:
            names = []
            for name in next_name:
                if first_name.upper() in name.upper():
                    names.append(name)
            next_name = names
        elif len(next_name) == 0:
            for name in names:
                if first_name.upper() in name.upper():
                    next_name.append(name)

    if len(next_name) == 1:
        return next_name[0].split('(')[-1]
    else:
        return '|'.join(next_name)


def get_state_and_city(new_names):
    if len(new_names) == 0 or '|' in new_names:
        return pd.Series({'state_n': None, 'city_n': None})

    else:
        city, state = new_names.split(', ')
        state = re.findall(r'\w+', state)[0]
        city = re.findall(r'\w+', state)[0]
        return pd.Series({'state_n': state, 'city_n': city})


def process_new_names(new_name):
    if not hasattr(new_name, 'split') or '|' in new_name:
        return None

    while ',,' in new_name:
        new_name = new_name.replace(',,', ',')

    split = new_name.split(',')
    if len(split) == 1:
        return split[0]
    elif len(split) > 1:
        return split[-2]
    else:
        return None

if __name__ == '__main__':
    df = pd.read_pickle(os.path.join(tmp_path, 'df_5_add_inventor_text.p'))
    df['new_names'] = df.apply(get_city_from_inventor_text, axis=1)
    df.merge(df.new_names.apply(get_state_and_city), left_index=True, right_index=True)
    df.to_pickle(tmp_path, 'add_state_city_name.p')
