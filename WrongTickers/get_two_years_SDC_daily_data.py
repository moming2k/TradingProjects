#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: get_two_years_SDC_daily_data
# Author: Mark Wang
# Date: 27/8/2016

import datetime

import pandas as pd

from constants import *


def get_two_years_data(row):
    pass


if __name__ == "__main__":
    file_path = 'result_csv/wrong_tickers_from_Bloomberg_large_ES.csv'
    df = pd.read_csv(file_path, index_col=0, usecols=[CUSIP_REAL, CUSIP_WRONG, DATE_TODAY, DATE_YESTERDAY,
                                                      DATE_TOMORROW, COMPANY_NAME, TICKER_WRONG, TICKER_REAL,
                                                      WRONG_TICKER_SOURCE])
    df[DATE_TODAY] = df[DATE_TODAY].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
    df[DATE_YESTERDAY] = df[DATE_YESTERDAY].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
    df[DATE_TOMORROW] = df[DATE_TOMORROW].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))