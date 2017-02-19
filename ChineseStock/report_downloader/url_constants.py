#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: url_constants
# @Date: 2017-02-16
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

from constants import Constant


class URLConstant(Constant):
    SZ_MAIN_URL = 'http://www.szse.cn/main'
    SZ_POST_URL = 'http://www.szse.cn/szseWeb/FrontController.szse'

    SZ_REGULATORY_INFORMATION_URL = '{}/jgxxgk'.format(SZ_MAIN_URL)
    SZ_DJG_RELATED_SHARE_CHANGE_URL = '{}/djggfbd/'.format(SZ_REGULATORY_INFORMATION_URL)
    SZ_SHORT_TERM_TRADING_GET_URL = '{}/dxjy/'.format(SZ_REGULATORY_INFORMATION_URL)
    SZ_EVALUATION_GET_URL = '{}/xxplkp/'.format(SZ_REGULATORY_INFORMATION_URL)

    SH_MAIN_URL = 'http://www.sse.com.cn/disclosure/credibility/supervision/change/'
    SH_GET_URL = 'http://query.sse.com.cn/commonQuery.do'
