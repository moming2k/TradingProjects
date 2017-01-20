#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: constant
# @Date: 2017-01-16
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime

TIME_SEP = [datetime.datetime(1984, 1, 1), datetime.datetime(1988, 1, 1), datetime.datetime(1992, 1, 1),
            datetime.datetime(1996, 1, 1), datetime.datetime(2000, 1, 1), datetime.datetime(2004, 1, 1),
            datetime.datetime(2008, 1, 1), datetime.datetime(2012, 1, 1), datetime.datetime(2016, 1, 1),
            ]

developed_currency_list = ['AUSTRALIANDOLLAR',
                           'BELGIANFRANC',
                           'CADIANDOLLAR',
                           'DANISHKRONE',
                           'EURO',
                           'FRENCHFRANC',
                           'GERMANMARK',
                           'ITALIANLIRA',
                           'JAPANESEYEN',
                           'NETHGUILDER',
                           'NEWZEALANDDOLLAR',
                           'NORWEGIANKRONE',
                           'SWEDISHKRO',
                           'SWISSFRANC',
                           'UKPOUND']
all_currency_list = ['AUSTRALIANDOLLAR',
                     'AUSTRIANSCHIL',
                     'BELGIANFRANC',
                     'BRAZILIANREAL',
                     'BULGARIANLEV',
                     'CADIANDOLLAR',
                     'CROATIANKU',
                     'CYPRUSPOUND',
                     'CZECHKORU',
                     'DANISHKRONE',
                     'EGYPTIANPOUND',
                     'EURO',
                     'FINNISHMARKKA',
                     'FRENCHFRANC',
                     'GERMANMARK',
                     'GREEKDRACHMA',
                     'HONGKONGDOLLAR',
                     'HUNGARIANFORINT',
                     'ICELANDICKRO',
                     'INDIANRUPEE',
                     'INDONESIANRUPIAH',
                     'IRISHPUNT',
                     'ISRAELISHEKEL',
                     'ITALIANLIRA',
                     'JAPANESEYEN',
                     'KUWAITIDIR',
                     'MALAYSIANRINGGIT',
                     'MEXICANPESO',
                     'NETHGUILDER',
                     'NEWZEALANDDOLLAR',
                     'NORWEGIANKRONE',
                     'PHILIPPINEPESO',
                     'POLISHZLOTY',
                     'PORTUGUESEESCUDO',
                     'RUSSIANROUBLE',
                     'SAUDIRIYAL',
                     'SINGAPOREDOLLAR',
                     'SLOVAKKORU',
                     'SLOVENIANTOLAR',
                     'SOUTHAFRICARAND',
                     'SOUTHKOREANWON',
                     'SPANISHPESETA',
                     'SWEDISHKRO',
                     'SWISSFRANC',
                     'TAIWANNEWDOLLAR',
                     'THAIBAHT',
                     'UKPOUND',
                     'UKRAINEHRYVNIA']

emerging_currency_list = ['PORTUGUESEESCUDO', 'ISRAELISHEKEL', 'RUSSIANROUBLE', 'INDIANRUPEE', 'GREEKDRACHMA',
                          'PHILIPPINEPESO', 'SINGAPOREDOLLAR', 'POLISHZLOTY', 'FINNISHMARKKA', 'CYPRUSPOUND',
                          'HONGKONGDOLLAR', 'EGYPTIANPOUND', 'THAIBAHT', 'SLOVENIANTOLAR', 'SAUDIRIYAL',
                          'SOUTHAFRICARAND', 'HUNGARIANFORINT', 'IRISHPUNT', 'TAIWANNEWDOLLAR', 'BRAZILIANREAL',
                          'ICELANDICKRO', 'MALAYSIANRINGGIT', 'MEXICANPESO', 'CROATIANKU', 'SOUTHKOREANWON',
                          'CZECHKORU', 'KUWAITIDIR', 'UKRAINEHRYVNIA', 'SLOVAKKORU', 'INDONESIANRUPIAH',
                          'SPANISHPESETA', 'AUSTRIANSCHIL', 'BULGARIANLEV']

currency_dict = {'AUSTRALIANDOLLAR': 'Australia',
                 'AUSTRIANSCHIL': 'Austria',
                 'BELGIANFRANC': 'Belgium',
                 'BRAZILIANREAL': 'Brazil',
                 'BULGARIANLEV': 'Bulgaria',
                 'CADIANDOLLAR': 'Canada',
                 'CROATIANKU': 'Croatia',
                 'CYPRUSPOUND': 'Cyprus',
                 'CZECHKORU': 'Czech',
                 'DANISHKRONE': 'Denmark',
                 'EGYPTIANPOUND': 'Egypt',
                 'EURO': 'Europe',
                 'FINNISHMARKKA': 'Finland',
                 'FRENCHFRANC': 'France',
                 'GERMANMARK': 'Germany',
                 'GREEKDRACHMA': 'Greece',
                 'HONGKONGDOLLAR': 'HongKong',
                 'HUNGARIANFORINT': 'Hungary',
                 'ICELANDICKRO': 'Iceland',
                 'INDIANRUPEE': 'India',
                 'INDONESIANRUPIAH': 'Indonesia',
                 'IRISHPUNT': 'Ireland',
                 'ISRAELISHEKEL': 'Israel',
                 'ITALIANLIRA': 'Italy',
                 'JAPANESEYEN': 'Japan',
                 'KUWAITIDIR': 'Kuwait',
                 'MALAYSIANRINGGIT': 'Malaysia',
                 'MEXICANPESO': 'Mexico',
                 'NETHGUILDER': 'Netherlands',
                 'NEWZEALANDDOLLAR': 'New ealand',
                 'NORWEGIANKRONE': 'Norway',
                 'PHILIPPINEPESO': 'Philippines',
                 'POLISHZLOTY': 'Poland',
                 'PORTUGUESEESCUDO': 'Portugal',
                 'RUSSIANROUBLE': 'Russia',
                 'SAUDIRIYAL': 'Saudi Arabia',
                 'SINGAPOREDOLLAR': 'Singapore',
                 'SLOVAKKORU': 'Slovakia',
                 'SLOVENIANTOLAR': 'Slovenia',
                 'SOUTHAFRICARAND': 'South Africa',
                 'SOUTHKOREANWON': 'South Korea',
                 'SPANISHPESETA': 'Spain',
                 'SWEDISHKRO': 'Sweden',
                 'SWISSFRANC': 'Switzerland',
                 'TAIWANNEWDOLLAR': 'Taiwan',
                 'THAIBAHT': 'Thailand',
                 'UKPOUND': 'United Kingdom',
                 'UKRAINEHRYVNIA': 'Ukraine'}

columns = ['Mean(%)', 'Max', 'Min', 'Std. dev.', 'Sample Period']


class Constant(object):
    SRC = 'SRC'
    SPA = 'SPA'
    MEAN_RETURN = 'Mean Return'
    SHARPE_RATIO = 'Sharpe Ratio'

    ONE_MONTH = '1m'
    THREE_MONTH = '3m'
    SIX_MONTH = '6m'
    TWELVE_MONTH = '12m'

    STRATEGY_NUM = 'strategy_num'

    BEST_STRATEGY_DESCRIPTION = 'Description'
    BEST_STRATEGY_MEAN_RETURN = 'MeanReturn'
    BEST_STRATEGY_SHARPE_RATIO = 'SharpeRatio'
    BEST_STRATEGY_NOMINAL_P_VALUE = 'Nominal p-value'
    BEST_STRATEGY_RC_P_VALUE = 'Reality check p-value'
    BEST_STRATEGY_PA_P_VALUE = 'SPA test p-value'
    BEST_STRATEGY_ST_P_VALUE = 'Stepwise test p-value'

    AVERAGE_REJECT_NUM = 'Average number'
    MINIMUM_REJECT_NUM = 'Minimum number'
    MAXIMUM_REJECT_NUM = 'Maximum number'
    AVERAGE_REJECT_PORTION = 'Average number / all'
