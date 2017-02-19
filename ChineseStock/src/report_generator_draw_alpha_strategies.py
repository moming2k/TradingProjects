#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: report_generator_draw_alpha_strategies
# @Date: 2017-02-18
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import re
import shutil
import datetime

import pandas as pd

from report_generator import ReportGenerator


class ReportGeneratorDrawAlphaStrategies(ReportGenerator):
    def _draw_histogram_from_statistics(self, statistics_df, save_path):
        raw_sharpe_ratio = statistics_df['{}_{}'.format(self.RAW_STRATEGY, self.SHARPE_RATIO)]
        raw_annualized_return = statistics_df['{}_{}'.format(self.RAW_STRATEGY, self.ANNUALIZED_RETURN)]
        # alpha_sharpe = statistics_df['{}_{}'.format(self.ALPHA_STRATEGY, self.SHARPE_RATIO)]
        alpha_return = statistics_df['{}_{}'.format(self.ALPHA_STRATEGY, self.RETURN)]
        self.draw_histogram(data_series=raw_sharpe_ratio.dropna(),
                            ylabel='Raw Strategy Sharpe Ratio',
                            xlabel='Strategies', title='Histogram of Raw Strategy Sharpe Ratio',
                            save_path=os.path.join(save_path, 'raw_sharpe_ratio_histogram.png'))

        self.draw_histogram(data_series=raw_annualized_return.dropna(),
                            ylabel='Raw Strategy Annualized Return',
                            xlabel='Strategies', title='Histogram of Raw Strategy Annualized Return',
                            save_path=os.path.join(save_path, 'raw_ann_return_histogram.png'))

        self.draw_histogram(data_series=alpha_return.dropna(),
                            ylabel='Alpha Strategy Return',
                            xlabel='Strategies', title='Histogram of Alpha Strategy Return',
                            save_path=os.path.join(save_path, 'alpha_return_histogram.png'))
        #
        # self.draw_histogram(data_series=alpha_sharpe.dropna(),
        #                     ylabel='Alpha Strategy Pseude Sharpe Ratio',
        #                     xlabel='Strategies', title='Histogram of Alpha Strategy Pseude Sharpe Ratio',
        #                     save_path=os.path.join(save_path, 'alpha_sharpe_ratio_histogram.png'))

    def generate_histogram_from_result_path(self, result_path):
        """ Draw histogram picture from result path, histograms include sharpe and ann return of raw strategy and
            simple return and sharpe ratio of alpha strategy. Also will select best such strategy picture
        """

        self.logger.info('Start to draw histogram from result_path {}'.format(result_path))

        max_value_dict = {}

        for key in [self.BEST_ALPHA_RETURN,
                    # self.BEST_ALPHA_SHARPE,
                    self.BEST_RAW_ANNUALIZED_RETURN, self.BEST_RAW_SHARPE_RATIO]:
            max_value_dict[key] = {self.VALUE: 0.0,
                                   self.PICTURE_PATH: None}

        statistics_df_list = []

        dir_list = os.listdir(result_path)

        self.logger.debug('Dir list is {}'.format(dir_list))

        for dir_name in dir_list:
            self.logger.info('handle dir {}'.format(dir_name))
            current_path = os.path.join(result_path, dir_name)
            if not os.path.isdir(current_path):
                continue

            wealth_file_name = self.get_target_file_name(current_path, 'sr.', 'p')
            beta_file_name = self.get_target_file_name(current_path, 'beta', 'p')

            if beta_file_name is None:
                beta_file_name = self.get_target_file_name(current_path, 'alpha', 'p')

            if wealth_file_name is None or beta_file_name is None:
                continue

            self.logger.debug('beta file is {}'.format(beta_file_name))
            self.logger.debug('wealth file is {}'.format(wealth_file_name))

            raw_strategy_df = self._re_index_orginal_data(pd.read_pickle(os.path.join(current_path, wealth_file_name)),
                                                          10000.)
            beta_strategy_df = self._re_index_orginal_data(pd.read_pickle(os.path.join(current_path, beta_file_name)),
                                                           10000.)

            alpha_strategy_df = raw_strategy_df - beta_strategy_df

            raw_sharpe_ratio = self.get_sharpe_ratio(raw_strategy_df, df_type=self.WEALTH_DATAFRAME).dropna()
            raw_annualized_return = self.get_annualized_return(raw_strategy_df, df_type=self.WEALTH_DATAFRAME).dropna()
            alpha_return = self.get_alpha_strategy_simple_return(alpha_strategy=alpha_strategy_df).dropna()
            # alpha_sharpe = self.get_alpha_strategies_pseude_sharpe_ratio(alpha_strategy=alpha_strategy_df).dropna()

            # Save required statistics
            statistics_df = pd.DataFrame(index=raw_sharpe_ratio.index)
            statistics_df['{}_{}'.format(self.RAW_STRATEGY, self.SHARPE_RATIO)] = raw_sharpe_ratio
            statistics_df['{}_{}'.format(self.RAW_STRATEGY, self.ANNUALIZED_RETURN)] = raw_annualized_return
            # statistics_df['{}_{}'.format(self.ALPHA_STRATEGY, self.SHARPE_RATIO)] = alpha_sharpe
            statistics_df['{}_{}'.format(self.ALPHA_STRATEGY, self.RETURN)] = alpha_return
            statistics_df_list.append(statistics_df)

            stop_loss_rate = re.findall(r'\d+', wealth_file_name)[-1]

            # Draw histogram
            self._draw_histogram_from_statistics(statistics_df, current_path)

            for key in max_value_dict:
                self.logger.debug('Current key is {}'.format(key))
                if key == self.BEST_RAW_ANNUALIZED_RETURN:
                    data_series = raw_annualized_return

                elif key == self.BEST_RAW_SHARPE_RATIO:
                    data_series = raw_sharpe_ratio

                # elif key == self.BEST_ALPHA_SHARPE:
                #     data_series = alpha_sharpe

                else:
                    data_series = alpha_return

                self.logger.debug('Current data series is {}'.format(data_series))
                best_strategy_name = data_series.idxmax()

                data_series_list = [raw_strategy_df[best_strategy_name], beta_strategy_df[best_strategy_name],
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

        merged_sta_df = pd.concat(statistics_df_list, axis=0, ignore_index=False)
        self._draw_histogram_from_statistics(merged_sta_df, result_path)

    def find_best_period_between_target_period(self, start_date, end_date, result_path):
        """ Find the best strategy between start_date and end_date """

        self.logger.info('Start to find best strategies between {} and {}'.format(start_date, end_date))
        max_value_dict = {}

        key_suffix = '{}_{}'.format(start_date.strftime('%y'), end_date.strftime('%y'))

        for key in [self.BEST_ALPHA_RETURN, self.BEST_RAW_ANNUALIZED_RETURN, self.BEST_RAW_SHARPE_RATIO,
                    '{}2'.format(self.BEST_ALPHA_RETURN)]:
            max_value_dict['{}_{}'.format(key, key_suffix)] = {self.VALUE: 0.0,
                                                               self.PICTURE_PATH: 0.0}

        dir_list = os.listdir(result_path)

        for dir_name in dir_list:
            current_path = os.path.join(result_path, dir_name)
            if not os.path.isdir(current_path):
                continue

            self.logger.debug('Start to handle path {}'.format(current_path))

            raw_df_name = self.get_target_file_name(current_path, 'sr.', 'p')
            beta_df_name = self.get_target_file_name(current_path, 'beta', 'p')

            if raw_df_name is None:
                self.logger.warn('Current folder does not have raw strategy file')
                continue
            elif beta_df_name is None:
                self.logger.warn('Current folder does not have beta strategy file')
                continue

            raw_strategy_df = self._re_index_orginal_data(pd.read_pickle(os.path.join(current_path, raw_df_name)),
                                                          10000.)
            beta_strategy_df = self._re_index_orginal_data(pd.read_pickle(os.path.join(current_path, beta_df_name)),
                                                           10000.)
            alpha_strategy_df = raw_strategy_df - beta_strategy_df

            raw_sub_df = self.get_sub_df(raw_strategy_df, start_date, end_date)
            alpha_sub_df = self.get_sub_df(raw_strategy_df, start_date, end_date)

            raw_sharpe_ratio = self.get_sharpe_ratio(raw_sub_df, df_type=self.WEALTH_DATAFRAME).dropna()
            raw_annualized_return = self.get_annualized_return(raw_sub_df, df_type=self.WEALTH_DATAFRAME).dropna()
            alpha_return = self.get_alpha_strategy_simple_return(alpha_strategy=alpha_sub_df).dropna()
            alpha_return2 = self.get_alpha_strategy_simple_return2(alpha_strategy=alpha_sub_df).dropna()

            stop_loss_rate = re.findall(r'\d+', raw_df_name)[-1]

            for key in max_value_dict:
                self.logger.debug('Current key is {}'.format(key))
                if key.startswith(self.BEST_RAW_ANNUALIZED_RETURN):
                    data_series = raw_annualized_return

                elif key.startswith(self.BEST_RAW_SHARPE_RATIO):
                    data_series = raw_sharpe_ratio

                # elif key == self.BEST_ALPHA_SHARPE:
                #     data_series = alpha_sharpe

                elif key.startswith('{}2'.format(self.BEST_ALPHA_RETURN)):
                    data_series = alpha_return2

                else:
                    data_series = alpha_return

                self.logger.debug('Current data series is {}'.format(data_series))
                best_strategy_name = data_series.idxmax()

                data_series_list = [raw_strategy_df[best_strategy_name], beta_strategy_df[best_strategy_name],
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

    def _plot_multiline_picture_text(self, pic_title, data_list, legends, save_path, stop_loss_rate):

        self.logger.debug('Start to plot pic {}'.format(pic_title))
        line1 = 'Transaction cost 0.2% SR {}%'.format(stop_loss_rate)

        info_list = [line1]

        raw_strategy = data_list[0]
        beta_strategy = data_list[1]
        alpha_strategy = data_list[2]

        time_period = ['all', '09_14', '13_16', 'after_16']
        period_list = [(None, None), (datetime.datetime(2009, 1, 1), datetime.datetime(2015, 1, 1)),
                       (datetime.datetime(2013, 7, 22), datetime.datetime(2016, 7, 20)),
                       (datetime.datetime(2016, 2, 1), None)]

        def generate_line_info(i, date_tuple):
            current_line = 'Date {}'.format(time_period[i])
            result_list = [current_line]

            def get_line_not_alpha(data_series, prefix_info):
                if date_tuple[0] is not None:
                    data_series = data_series[data_series.index > date_tuple[0]]

                if date_tuple[1] is not None:
                    data_series = data_series[data_series.index < date_tuple[1]]

                sharpe_ratio = self.get_sharpe_ratio(data_series, df_type=self.WEALTH_DATAFRAME)
                ann_return = self.get_annualized_return(data_series, df_type=self.WEALTH_DATAFRAME) * 100
                max_draw_down = self.get_max_draw_down(data_series) * 100

                current_line = '{}: Sharpe Ratio {:.3f}, Annualized Return {:.2f}%, Max Drawdown rate {:.2f}%'.format(
                    prefix_info, sharpe_ratio, ann_return, max_draw_down
                )
                return current_line

            def get_line_alpha(data_series):
                if date_tuple[0] is not None:
                    data_series = data_series[data_series.index > date_tuple[0]]

                if date_tuple[1] is not None:
                    data_series = data_series[data_series.index < date_tuple[1]]

                # pse_sharpe_ratio = self.get_alpha_strategies_pseude_sharpe_ratio(data_series)
                simple_return = self.get_alpha_strategy_simple_return(data_series) * 100
                simple_return2 = self.get_alpha_strategy_simple_return2(data_series) * 100
                # standard_dev = self.get_wealth_return_std(data_series)

                # current_line = 'Alpha: Pseude-Sharpe Ratio {:.3f}, Simple Return {:.2f}%, Std {:.4f}'.format(
                #     pse_sharpe_ratio, simple_return, standard_dev
                # )
                current_line = 'Alpha: Simple Return {:.2f}%, Simple Return 2 {:.2f}%'.format(
                    simple_return, simple_return2
                )
                return current_line

            for prefix in ['Raw', 'Beta', 'Alpha']:

                if prefix == 'Raw':
                    result_list.append(get_line_not_alpha(raw_strategy, prefix))

                elif prefix == 'Beta':
                    result_list.append(get_line_not_alpha(beta_strategy, prefix))

                else:
                    result_list.append(get_line_alpha(alpha_strategy))

            return result_list

        for i, date_tuple in enumerate(period_list[:2]):
            info_list.extend(generate_line_info(i, date_tuple))

        text1 = '\n'.join(info_list)

        info_list = []
        for i, date_tuple in enumerate(period_list[2:]):
            info_list.extend(generate_line_info(i + 2, date_tuple))

        text2 = '\n'.join(info_list)

        self.plot_multiline_alpha(data_list,
                                  legend_list=legends,
                                  picture_title=pic_title,
                                  picture_save_path=save_path,
                                  text1=text1, text2=text2)


if __name__ == '__main__':
    import logging
    import sys

    from xvfbwrapper import Xvfb

    from path_info import Path

    transaction_cost = 0.002

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')
    suffix = 'insider_stock_20170214_alpha_no_neglect_all_types'
    report_path = os.path.join(Path.REPORT_DATA_PATH, 'report_info_buy_only')
    test = ReportGeneratorDrawAlphaStrategies(transaction_cost, folder_suffix=suffix, report_path=report_path)
    result_path = os.path.join(Path.RESULT_PATH, 'insider_stock_20170214_alpha_no_neglect_all_types')

    vdisplay = Xvfb(width=1366, height=768)
    vdisplay.start()
    test.find_best_period_between_target_period(result_path=result_path, end_date=datetime.datetime(2016, 7, 20),
                                                start_date=datetime.datetime(2013, 7, 22))

    vdisplay.stop()
