#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: constants
# Author: Mark Wang
# Date: 4/8/2016


class Constants(object):

    # url information
    START_URL = "http://www.lexisnexis.com/en-us/products/lexis-advance/lexis-advance-customer.page"
    FIND_PERSON_URL = 'https://r3.lexis.com/laprma/FindAPerson.aspx?national=true'

    # information used for
    SSN = 'ssn'
    LexID = 'LexID'
    FirstName = 'FirstName'
    MiddleName = 'MiddleName'
    LastName = 'LastName'

    ID_DICT = {'ssn': 'MainContent_SSN',
               'LexID': 'MainContent_Did',
               'FirstName': 'MainContent_Name_FirstName',
               'MiddleName': 'MainContent_Name_MiddleName',
               'LastName': 'MainContent_Name_LastName',
               }
