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
    StreetAddress = 'StreetAddress'
    City = 'City'
    State = 'State'
    ZipCode = 'ZipCode'
    Telephone = 'Telephone'
    DateOfBirth = 'DateOfBirth'
    AgeLow = 'AgeLow'
    AgeHigh = 'AgeHigh'

    # check box
    StrictSearch = 'IsStrictSearch'
    UsePhonetics = 'IsUsePhonetics'
    UseNicknames = 'IsUseNicknames'

    # Select box
    AddressRadius = 'AddressRadius'

    TEXT_ID_DICT = {'ssn': 'MainContent_SSN',
                    'LexID': 'MainContent_Did',
                    'FirstName': 'MainContent_Name_FirstName',
                    'MiddleName': 'MainContent_Name_MiddleName',
                    'LastName': 'MainContent_Name_LastName',
                    'StreetAddress': 'MainContent_Address_Address1',
                    'City': 'MainContent_Address_City',
                    'ZipCode': 'MainContent_Address_Zip5',
                    'Telephone': 'MainContent_Phone',
                    'DateOfBirth': 'MainContent_DOB',
                    }

    CHECK_ID_DICT = {'IsStrictSearch': 'MainContent_StrictMatch',
                     'IsUsePhonetics': 'MainContent_UsePhonetics',
                     'IsUseNicknames': 'MainContent_UseNicknames',
                     }

    SELECT_ID_DICT = {'AddressRadius': 'MainContent_Radius_Radius',
                      'State': 'MainContent_Address_State_stateList',
                      }

    AgeRangeID = {'AgeLow': 'AgeLow',
                  'AgeHigh': 'AgeHigh'}

    SearchButtonID = 'MainContent_formSubmit_searchButton'
    ClearFormButtonID = 'MainContent_formSubmit_clearFormLink'
