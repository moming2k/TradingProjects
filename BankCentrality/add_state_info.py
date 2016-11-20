#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_state_info
# Author: Mark Wang
# Date: 20/11/2016

import os

import pandas as pd

path = '/home/wangzg/Documents/WangYouan/research/BankCentrality'
data_path = 'data'
result_path = 'result'

df = pd.read_excel(os.path.join(path, data_path, '20151225USPubBankMnAName.xlsx'),
                   )
