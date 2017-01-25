#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: constants
# @Date: 2017-01-25
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import numpy as np

portfolio_num_range = range(5, 20)
portfolio_num_range.extend(range(25, 101, 5))

holding_days_list = range(2, 15)

drawdown_rate_range = np.arange(-0.05, 0, 0.01)

transaction_cost_list = [0.05, 0.1]

info_type_list = ['all', 'company', 'exe', 'exe_brothers', 'exe_parents', 'exe_self', 'exe_spouse']


class Constant(object):
    # trading market type
    SHANGHAI_A = 1
    SHANGHAI_B = 2
    SHENZHEN_A = 4
    SHENZHEN_B = 8
    GEM = 16  # Growth Enterprises Market Board

    # Other information
    OVERWEIGHT = u'增持'
    REDUCTION = u'减持'
    SENIOR = u'高管'
    COMPANY = u'公司'
    PERSON = u'个人'

    SPOUSE = u'配偶'
    SELF = u'本人'
    PARENTS = u'父母'
    FATHER = u'父亲'
    MOTHER = u'母亲'
    OTHERS = u'其他'
    BROTHERS = u'兄弟姐妹'
    OTHER_RELATIONS = u'其他关联'

    CONTROLLED_CORPORATION = u'受控法人'
    LISTED_COMPANY = u'上市公司'

    REPORT_TICKER = 'VAR1'
    REPORT_COMPANY_NAME = 'VAR2'
    REPORT_ANNOUNCE_DATE = 'anndate'
    REPORT_ACTION = 'VAR10'
    REPORT_RELATIONSHIP = 'relation'
    REPORT_TYPE = 'type'

    REPORT_SELL_DATE = 'sell_date'
    REPORT_RETURN_RATE = 'return'
    REPORT_BUY_DATE = 'buy_date'
    REPORT_MARKET_TICKER = 'market_ticker'
    REPORT_MARKET_TYPE = 'market_type'
    REPORT_BUY_PRICE = 'buy_price'

    STOCK_TICKER = 'Stkcd'
    STOCK_DATE = 'Trddt'
    STOCK_OPEN_PRICE = 'Opnprc'
    STOCK_CLOSE_PRICE = 'Clsprc'
    STOCK_MARKET_TYPE = 'Markettype'
    STOCK_ADJPRCWD = 'Adjprcwd'
    STOCK_ADJPRCND = 'Adjprcnd'

    HOLDING_DAYS = 'holding_days'
    PORTFOLIO_NUM = 'portfolio_num'
    DRAWDOWN_RATE = 'drawdown_rate'
    INFO_TYPE = 'info_type'
