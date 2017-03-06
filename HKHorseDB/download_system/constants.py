#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: constants
# @Date: 2017-02-13
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

class Constant(object):
    ENGLISH = 'English'
    CHINESE = 'Chinese'

    # the follow constants are used in hkjc website
    HKJC_HOST_URL = 'www.hkjc.com'
    HKJC_RACING_URL = 'racing.hkjc.com'
    HORSE_LIST_PAGE = 'racing/selecthorsebychar.asp'
    HORSE_DETAIL_PAGE = 'racing/info/horse/smartform'
    HORSE_FORMER_NAME_PAGE = 'racing/horse_former_name.asp'
    JOCKEY_LIST_URL = '{}/racing/Info/jockey/Ranking'.format(HKJC_RACING_URL)
    JOCKEY_DETAIL_LIST_URL = 'racing/JockeyPastRec.asp'

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
    BIRTHDAY = 'Birthday'
    FORMER_NAME = 'FormerName'

    CURRENT_SEASON = 'Current'
    LAST_SEASON = 'Last'

    BACKGROUND = 'Background'
    ACHIEVEMENTS = 'Achievements'
    NOTABLE_WINS = 'NotableWin'
    HK_CAREER_WINS = 'HKCareerWins'
    HK_CAREER_WINS_RATE = 'HKCareerWinsRate'
    IJC_RECORD = 'IJC'
    NATIONALITY = 'Nationality'
