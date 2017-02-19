#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: calculate_return_utils_20170219
# @Date: 2017-02-19
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import pandas as pd

import numpy as np

from ..account_portfolio.average_portfolio import AveragePortfolio
from ..account_portfolio.account_hedge_399300 import AccountHedge399300
from calculate_return_utils_20170216 import CalculateReturnUtils20170216


class CalculateReturnUtils20170219(CalculateReturnUtils20170216):
    """ This file I add alpha test to structure and no neglect period """

    def calculate_portfolio_return(self, report_df, portfolio_num, transaction_cost=0):
        portfolio = AveragePortfolio(portfolio_num, total_value=self.initial_wealth,
                                     transaction_cost=transaction_cost, price_type=self.STOCK_CLOSE_PRICE)
        alpha_hedge_portfolio = AveragePortfolio(portfolio_num, total_value=self.initial_wealth,
                                                 transaction_cost=transaction_cost, price_type=self.STOCK_CLOSE_PRICE,
                                                 account_class=AccountHedge399300)
        buy_date_list = report_df[self.REPORT_BUY_DATE].sort_values()
        wealth_series = pd.Series()
        alpha_hedge_series = pd.Series()

        for current_date in self.trading_days_list:

            info_index = buy_date_list[buy_date_list == current_date].index

            for i in info_index:
                short_end_date = report_df.ix[i, self.REPORT_SELL_DATE]

                buy_date = report_df.ix[i, self.REPORT_BUY_DATE]
                ticker = report_df.ix[i, self.REPORT_MARKET_TICKER]
                # market_type = return_df.ix[i, const.REPORT_MARKET_TYPE]
                buy_price_type = report_df.ix[i, self.REPORT_BUY_TYPE]
                sell_price_type = report_df.ix[i, self.REPORT_SELL_TYPE]

                if np.isnan(short_end_date) or ticker is None:
                    continue
                portfolio.short_stocks(buy_date=buy_date, end_date=short_end_date, buy_stock_type=buy_price_type,
                                       sell_stock_type=sell_price_type, stock_ticker=ticker)
                alpha_hedge_portfolio.short_stocks(buy_date=buy_date, end_date=short_end_date,
                                                   buy_stock_type=buy_price_type,
                                                   sell_stock_type=sell_price_type, stock_ticker=ticker)

            wealth_series.loc[current_date] = portfolio.get_current_values(current_date)
            alpha_hedge_series.loc[current_date] = alpha_hedge_portfolio.get_current_values(current_date)

        return wealth_series, alpha_hedge_series

    def calculate_return_and_wealth(self, info):
        portfolio_num = info[self.PORTFOLIO_NUM]
        holding_days = info[self.HOLDING_DAYS]
        info_type = info[self.INFO_TYPE]
        return_path = info[self.REPORT_RETURN_PATH]
        wealth_path = info[self.WEALTH_DATA_PATH]
        report_path = info[self.REPORT_PATH]

        file_name = '{}_{}p_{}d'.format(info_type, portfolio_num, holding_days)

        if self.TRANSACTION_COST in info:
            transaction_cost = info[self.TRANSACTION_COST]
            file_name = '{}_{}cost'.format(file_name, int(transaction_cost * 1000))
        else:
            transaction_cost = 0

        if self.STOPLOSS_RATE in info:
            stoploss_rate = info[self.STOPLOSS_RATE]
            file_name = '{}_{}sr'.format(file_name, int(abs(stoploss_rate) * 100))
        else:
            stoploss_rate = None

        try:

            report_df = self.generate_buy_only_return_df(return_path, holding_days, info_type=info_type,
                                                         stoploss_rate=stoploss_rate, report_path=report_path)
        except Exception, err:
            import traceback
            traceback.print_exc()

            print info
            print 'Exception happened when report df'

            raise Exception(err)

        try:

            wealth_series, alpha_series = self.calculate_portfolio_return(report_df, portfolio_num,
                                                                          transaction_cost=transaction_cost)
            wealth_series.to_pickle(os.path.join(wealth_path, '{}_raw.p'.format(file_name)))
            alpha_series.to_pickle(os.path.join(wealth_path, '{}_alpha.p'.format(file_name)))

        except Exception, err:
            import traceback
            traceback.print_exc()

            print info
            print 'Exception happened when handle wealth series'

            raise Exception(err)

        return wealth_series
