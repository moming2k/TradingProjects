#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: __init__.py
# @Date: 2017-03-05
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


from path_info import PathInfo


class Constant(PathInfo):
    ROOT_URL = 'http://www.hkhorsedb.com/cseh/index.php'
    DATE_URL = 'http://www.hkhorsedb.com/cseh/poddsleftxml.php'

    LOGIN_XPATH = '/html/body/table/tbody/tr/td/table[3]/tbody/tr/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td/form/center/font/input[4]'

    # The following info is about info type
    HORSE = 'Horse'
    JOCKEY = 'Jockey'
    TRAINER = 'Trainer'

    # record info constant
    NAME = 'Name'
    COLOR = 'Color'
    SEX = 'Sex'
    ORIGIN = 'Origin'
    AGE = 'Age'
    IMPORT_TYPE = 'ImportType'
    SEASON_STAKE = 'SeasonStakes'
    TOTAL_STAKE = 'TotalStakes'
    NUMBER_ONE = 'No1'
    NUMBER_TWO = 'No2'
    NUMBER_THREE = 'No3'
    NUMBER_FOUR = 'No4'
    NUMBER_STARTS = 'NoStarts'
    CODE = 'Code'
    OWNER = 'Owner'
    CURRENT_RATING = 'CurrentRating'
    SEASON_START_RATING = 'SeasonStartRating'
    SIRE = 'Sire'
    DAM = 'Dam'
    DAM_SIRE = 'DamSire'
    STAKES = 'Stakes'

    CURRENT_SEASON = 'Current'
    LAST_SEASON = 'Last'

    BACKGROUND = 'Background'
    ACHIEVEMENTS = 'Achievements'
    NOTABLE_WINS = 'NotableWin'
    HK_CAREER_WINS = 'HKCareerWins'
    HK_CAREER_WINS_RATE = 'HKCareerWinsRate'
    IJC_RECORD = 'IJC'
    NATIONALITY = 'Nationality'

    YEAR = 'Year'
    MONTH = 'Month'
    DAY = 'Day'

    DATE = 'Date'
    RACE_INDEX = 'Index'

    RACE = 'Race'
    SEASON_INDEX = 'SeasionIndex'
    CLASS = 'Class'
    ID = 'ID'
    BIRTHDAY = 'Birthday'
    FORMER_NAME = 'FormerName'

    LAST_RACE = 'LastRace'
    LAST_NO_ONE = 'LastNo1'
    LAST_NO_TWO = 'LastNo2'
    LAST_NO_THREE = 'LastNo3'
    LAST_TOP_THREE = 'LastTop3'

    ENGLISH = 'English'
    CHINESE = 'Chinese'
