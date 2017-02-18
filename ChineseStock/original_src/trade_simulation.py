#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: trade_simulation
# @Date: 2017-01-06
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


from constant import Constant


class TradeSimulation(Constant):
    def __init__(self, holding_days=22, senior_only=False):
        self.holding_days = holding_days

    def simulate_trading(self, stock_ticker, announce_date, action):
        pass
