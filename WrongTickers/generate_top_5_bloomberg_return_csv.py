#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: generate_top_5_bloomberg_return_csv
# Author: Mark Wang
# Date: 30/7/2016

import pandas as pd

df = pd.read_csv('result_csv/Bloomberg_CRSP(renamed).csv', index_col=0)
df = df[df['EarningsSurprise'] > 0.5]
df['EarningsSurpriseReturn'] = (df['OpenPriceTomorrow'] - df['ClosePriceYesterday']) / df['ClosePriceYesterday']
df = df.sort_values('EarningsSurprise', ascending=False)\
    .sort_values('EarningsSurpriseReturn', ascending=False)\
    .head(int(0.05 * df.shape[0]) + 1)

df.reset_index(drop=True).to_csv('result_csv/Bloomberg_CRSP_rename_top5pc.csv', encoding='utf8')
