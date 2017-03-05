#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: calculate_return_utils_20170303
# @Date: 2017-03-03
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd
import numpy as np

import calculate_return_utils_20170219


class CalculateReturnUtils(calculate_return_utils_20170219.CalculateReturnUtils20170219):
    """ This class add run up info to data """

    def calculate_return_and_wealth(self, info):
        portfolio_num = info[self.PORTFOLIO_NUM]
        holding_days = info[self.HOLDING_DAYS]
        info_type = info[self.INFO_TYPE]
        return_path = info[self.REPORT_RETURN_PATH]
        wealth_path = info[self.WEALTH_DATA_PATH]
        report_path = info[self.REPORT_PATH]
        run_up_rate = info[self.RUN_UP_RATE]
        run_up_x = info[self.RUN_UP_X]
        run_up_y = info[self.RUN_UP_Y]

        file_name = '{}_{}p_{}d_{}r_{}x_{}y'.format(info_type, portfolio_num, holding_days, run_up_rate, run_up_x,
                                                    run_up_y)

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

            report_df = self.generate_buy_only_return_df_run_up(return_path, holding_days, info_type=info_type,
                                                                stoploss_rate=stoploss_rate, report_path=report_path,
                                                                runup_rate=run_up_rate, runup_x=run_up_x,
                                                                runup_y=run_up_y)
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

    def generate_buy_only_return_df_run_up(self, return_path, holding_days, info_type, stoploss_rate,
                                           report_path, runup_rate, runup_x=20, runup_y=1):
        """
        based on run up rate to get return df
        :param return_path: the path where should save those return data
        :param holding_days: the holding days of buy wealth
        :param info_type: only keep target info type into consideration, like company, self, or others
        :param stoploss_rate: the drawback rate of target info
        :param report_path: the input report path
        :param runup_rate: run up rate
        :param runup_x: x information
        :param runup_y: y information
        :return: return df
        """
        if info_type is None:
            info_type = self.ALL

        if report_path is None:
            report_path = self.INSIDER_EXE_GT2_RUN_UP_PATH

        file_path = os.path.join(return_path, 'hdays_{}_report.p'.format(holding_days))
        if os.path.isfile(file_path):
            report_df = self.filter_df(pd.read_pickle(file_path), info_type)
            return report_df

        report_list = os.listdir(report_path)

        run_up_col = '{}_{}x_{}y'.format(self.RUN_UP_RATE, runup_x, runup_y)

        def process_report_df(row):
            ann_date = row[self.REPORT_ANNOUNCE_DATE]
            ticker = row[self.REPORT_TICKER]
            run_up = row[run_up_col]

            if run_up > runup_rate / 100. or np.isnan(run_up):
                return pd.Series(self._temp_result.copy())
            else:
                return self.calculate_trade_info(announce_date=ann_date, ticker_info=ticker[:6],
                                                 holding_days=holding_days, stoploss_rate=stoploss_rate,
                                                 buy_price_type=self.STOCK_OPEN_PRICE,
                                                 sell_price_type=self.STOCK_CLOSE_PRICE,
                                                 after_price_type=self.STOCK_OPEN_PRICE)

        result_df_list = []

        for file_name in report_list:
            report_df = self.filter_df(pd.read_pickle(os.path.join(report_path, file_name)), info_type)
            if self.REPORT_MARKET_TICKER in report_df.keys():
                report_df[self.REPORT_TICKER] = report_df[self.REPORT_MARKET_TICKER]
                del report_df[self.REPORT_MARKET_TICKER]
            tmp_df = report_df.merge(report_df.apply(process_report_df, axis=1), left_index=True,
                                     right_index=True)
            if self.REPORT_TICKER in tmp_df.keys():
                del tmp_df[self.REPORT_TICKER]
            if not tmp_df.empty:
                result_df_list.append(tmp_df)

        result_df = pd.concat(result_df_list).reset_index(drop=True)
        if info_type == self.ALL or len(self.INFO_TYPE_LIST) == 1:
            result_df.to_pickle(file_path)
        return result_df
