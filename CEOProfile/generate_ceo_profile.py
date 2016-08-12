#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: generate_ceo_profile
# Author: Mark Wang
# Date: 10/8/2016

import os
import sys
import re
import logging
import datetime

import pandas as pd

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')
logger = logging.getLogger(os.uname()[0])
current_year = datetime.datetime.today().year


def format_ceo_name(name):
    logger.debug("Input name is {}".format(name))
    if ',' in name:
        name = name.split(',')[0]

    name_list = map(lambda x: ''.join(re.findall(r'[a-zA-Z]+', x)), name.split(' '))
    if len(name_list) >= 3:
        return ','.join((name_list[0], name_list[1], name_list[-1]))
    elif len(name_list) == 2:
        return ','.join((name_list[0], "", name_list[-1]))
    elif name_list:
        logger.warn("Name {} only has one name".format(name))
        return ','.join(("", "", name_list[0]))
    else:
        logger.error("Name {} cannot find any result".format(name))
        return ','.join(("", "", ""))


def format_cusip_in_corp_prof(cusip):
    if isinstance(cusip, str) or isinstance(cusip, unicode):
        if len(cusip) < 9:
            return "{:09d}".format(int(cusip))[:-1]
        else:
            return cusip[:-1]
    else:
        return "{:09d}".format(int(cusip))[:-1]


def format_cusip_in_ceo_prof(cusip):
    if isinstance(cusip, str) or isinstance(cusip, unicode):
        if len(cusip) < 8:
            return "{:08d}".format(int(cusip))
        else:
            return cusip
    else:
        return "{:08d}".format(int(cusip))


if __name__ == "__main__":
    # handle ceo profile, generate their age and format CUSIP
    ceo_info_df = pd.read_csv("CEO_firm.csv", index_col=False, usecols=['EXEC_FULLNAME', "birth_year", "CUSIP"])
    ceo_info_df['CUSIP'] = ceo_info_df['CUSIP'].apply(format_cusip_in_ceo_prof)
    ceo_info_df['Age'] = ceo_info_df['birth_year'].apply(lambda x: current_year - int(x))
    ceo_info_df['Name'] = ceo_info_df['EXEC_FULLNAME'].apply(format_ceo_name)

    # handle firm location file
    corp_info_df = pd.read_excel("20160328firm_location_coordinates.xlsx")
    corp_info_df['cusip'] = corp_info_df['cusip'].apply(format_cusip_in_corp_prof)


    def get_ceo_live_state(cusip):
        index = corp_info_df[corp_info_df['cusip'] == cusip].index[0]
        return corp_info_df.ix[index, 'state']


    ceo_info_df['state'] = ceo_info_df['CUSIP'].apply(get_ceo_live_state)
