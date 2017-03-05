#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: report_generator_add_max_drawdown_limit
# @Date: 2017-03-02
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import re
import shutil

import pandas as pd

import report_generator_add_alpha_hedge


class ReportGenerator(report_generator_add_alpha_hedge.ReportGeneratorAlphaHedge):
    """ This class add max drawdown limit and run up information """

    def __init__(self, transaction_cost, report_path, folder_suffix, logger=None, stock_price_path=None,
                 trading_days_list_path=None):
        report_generator_add_alpha_hedge.ReportGeneratorAlphaHedge.__init__(
            self, transaction_cost, report_path, folder_suffix, logger, stock_price_path, trading_days_list_path)
        # self.PORTFOLIO_NUM_RANGE = range(5, 11)

    def main_progress(self, calculate_class, stop_loss_rate, sort_result=True):
        """ add run up information, calculate return utils after 20170303 can handle this issue """
        self.logger.info('Start to calculate with transaction cost {}, stop loss: {}%'.format(self.transaction_cost,
                                                                                              stop_loss_rate))
        w_path, s_path, r_path, p_path, bp_path15, bp_path2 = self._generate_useful_paths(stop_loss_rate)

        portfolio_info = []
        for portfolio_num in self.PORTFOLIO_NUM_RANGE:
            for holding_days in self.HOLDING_DAYS_LIST:
                for run_up_rate in self.RUN_UP_STOP_TRADE_RATE:
                    for run_up_x in self.RUN_UP_DAY_X_LIST:
                        portfolio_info.append({self.PORTFOLIO_NUM: portfolio_num,
                                               self.HOLDING_DAYS: holding_days,
                                               self.TRANSACTION_COST: self.transaction_cost,
                                               self.REPORT_RETURN_PATH: r_path,
                                               self.WEALTH_DATA_PATH: w_path,
                                               self.STOPLOSS_RATE: -float(abs(stop_loss_rate)) / 100,
                                               self.REPORT_PATH: self.report_path,
                                               self.RUN_UP_RATE: run_up_rate,
                                               self.RUN_UP_X: run_up_x,
                                               self.RUN_UP_Y: 1
                                               })

        self._computation(calculate_class=calculate_class, portfolio_info=portfolio_info)
        if sort_result:
            self._sort_result(w_path, s_path, stop_loss_rate, p_path, bp_path2, bp_path15)

        self.logger.info('Process finished')

    def _get_useful_key_by_drawdown_limit(self, df, drawdown_limit):
        drawdown = df.apply(self.get_max_draw_down, axis=0)
        sub = drawdown[drawdown < (drawdown_limit / 100.)]
        return sub.keys()

    def _get_best_strategy_with_drawdown_limit(self, result_path, period, drawdown_limit=5, drawdown_type='raw'):
        max_value_dict = {}

        statistics_df_list = []

        dir_list = os.listdir(result_path)

        self.logger.debug('Dir list is {}'.format(dir_list))
        if isinstance(period, str):
            self.logger.info('Start to draw histogram from result_path {}'.format(result_path))
            key_suffix = ''
            start_date = end_date = None

        else:
            start_date = period[0]
            end_date = period[1]
            self.logger.info('Start to find best strategies between {} and {}'.format(start_date, end_date))
            if start_date is not None and end_date is not None:
                key_suffix = '_{}_{}'.format(start_date.strftime('%y'), end_date.strftime('%y'))

            elif start_date is None:
                key_suffix = '_before_{}'.format(end_date.strftime('%y'))
            else:
                key_suffix = '_after_{}'.format(start_date.strftime('%y'))

        key_suffix = '{}_{}dr{}'.format(key_suffix, drawdown_type, drawdown_limit)
        for key in [self.BEST_ALPHA_RETURN, self.BEST_ALPHA_SHARPE,
                    self.BEST_RAW_ANNUALIZED_RETURN, self.BEST_RAW_SHARPE_RATIO]:
            max_value_dict['{}{}'.format(key, key_suffix)] = {self.VALUE: float('-inf'),
                                                              self.PICTURE_PATH: None}

        for dir_name in dir_list:
            current_path = os.path.join(result_path, dir_name)
            if not os.path.isdir(current_path):
                continue

            self.logger.debug('Start to handle path {}'.format(current_path))

            raw_df_name = self.get_target_file_name(current_path, 'raw', 'p')
            alpha_df_name = self.get_target_file_name(current_path, 'alpha', 'p')

            if alpha_df_name is None:
                alpha_df_name = self.get_target_file_name(current_path, 'beta', 'p')

            if raw_df_name is None:
                self.logger.warn('Current folder does not have raw strategy file')
                continue
            elif alpha_df_name is None:
                self.logger.warn('Current folder does not have alpha strategy file')
                continue

            raw_strategy_df = self._re_index_orginal_data(pd.read_pickle(os.path.join(current_path, raw_df_name)),
                                                          10000.)
            alpha_strategy_df = self._re_index_orginal_data(pd.read_pickle(os.path.join(current_path, alpha_df_name)),
                                                            10000.)

            raw_sub_df = self.get_sub_df(raw_strategy_df, start_date, end_date)
            alpha_sub_df = self.get_sub_df(alpha_strategy_df, start_date, end_date)

            if drawdown_type == 'raw':
                keys = self._get_useful_key_by_drawdown_limit(raw_sub_df, drawdown_limit)
            else:
                keys = self._get_useful_key_by_drawdown_limit(alpha_sub_df, drawdown_limit)

            if len(keys) == 0:
                continue

            raw_sub_df = raw_sub_df[keys]
            alpha_sub_df = alpha_sub_df[keys]

            raw_sharpe_ratio = self.get_sharpe_ratio(raw_sub_df, df_type=self.WEALTH_DATAFRAME).dropna()
            raw_annualized_return = self.get_annualized_return(raw_sub_df, df_type=self.WEALTH_DATAFRAME).dropna()
            alpha_sharpe_ratio = self.get_sharpe_ratio(alpha_sub_df, df_type=self.WEALTH_DATAFRAME).dropna()
            alpha_annualized_return = self.get_annualized_return(alpha_sub_df, df_type=self.WEALTH_DATAFRAME).dropna()

            stop_loss_rate = re.findall(r'\d+', raw_df_name)[-1]

            for key in max_value_dict:
                self.logger.debug('Current key is {}'.format(key))
                if key.startswith(self.BEST_RAW_ANNUALIZED_RETURN):
                    data_series = raw_annualized_return

                elif key.startswith(self.BEST_RAW_SHARPE_RATIO):
                    data_series = raw_sharpe_ratio

                elif key.startswith(self.BEST_ALPHA_SHARPE):
                    data_series = alpha_sharpe_ratio

                else:
                    data_series = alpha_annualized_return

                # self.logger.debug('Current data series is {}'.format(data_series))
                if key.startswith('best'):
                    best_strategy_name = data_series.idxmax()
                else:
                    best_strategy_name = data_series.idxmin()

                data_series_list = [raw_strategy_df[best_strategy_name],
                                    alpha_strategy_df[best_strategy_name]]
                self._plot_multiline_picture_text(data_list=data_series_list,
                                                  pic_title=best_strategy_name, legends=self.ALPHA_STRATEGY_LEGENDS,
                                                  save_path=os.path.join(current_path, '{}.png'.format(key)),
                                                  stop_loss_rate=stop_loss_rate)

                if data_series.max() > max_value_dict[key][self.VALUE]:
                    max_value_dict[key][self.VALUE] = data_series.max()
                    max_value_dict[key][self.PICTURE_PATH] = current_path

            for key in max_value_dict:
                if max_value_dict[key][self.PICTURE_PATH] is None:
                    continue

                else:
                    src = os.path.join(max_value_dict[key][self.PICTURE_PATH], '{}.png'.format(key))
                    dst = os.path.join(result_path, '{}.png'.format(key))

                    shutil.copy(src, dst)

    def find_best_period_between_target_period_drawdown_limit(self, start_date, end_date, result_path, limit):
        """ Find the best strategy between start_date and end_date """

        self.logger.info('Start to find best strategies between {} and {}'.format(start_date, end_date))
        self._find_max_value_during_target_period(result_path=result_path, period=[start_date, end_date])
        for dd_type in ['alpha', 'raw']:
            self._get_best_strategy_with_drawdown_limit(result_path=result_path, period=[start_date, end_date],
                                                        drawdown_limit=limit, drawdown_type=dd_type)

    def generate_histogram_from_result_path_drawdown_limit(self, result_path, limit):
        """ Draw histogram picture from result path, histograms include sharpe and ann return of raw strategy and
            simple return and sharpe ratio of alpha strategy. Also will select best such strategy picture
        """
        self.logger.info('Start to draw histogram from result_path {}'.format(result_path))
        self._find_max_value_during_target_period(result_path=result_path, period=self.ALL)
        for dd_type in ['alpha', 'raw']:
            self._get_best_strategy_with_drawdown_limit(result_path=result_path, period=self.ALL,
                                                        drawdown_limit=limit, drawdown_type=dd_type)
