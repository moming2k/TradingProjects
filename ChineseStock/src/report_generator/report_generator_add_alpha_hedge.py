#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: report_generator_add_alpha_hedge
# @Date: 2017-02-19
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import re
import shutil
import datetime

import pandas as pd

from report_generator_draw_alpha_strategies import ReportGeneratorDrawAlphaStrategies


class ReportGeneratorAlphaHedge(ReportGeneratorDrawAlphaStrategies):
    def __init__(self, transaction_cost, report_path, folder_suffix, logger=None, stock_price_path=None,
                 trading_days_list_path=None):
        ReportGeneratorDrawAlphaStrategies.__init__(self, transaction_cost, report_path, folder_suffix, logger,
                                                    stock_price_path, trading_days_list_path)
        self.ALPHA_STRATEGY_LEGENDS = ['Raw Strategy', 'Alpha Strategy']

    def _draw_histogram_from_statistics(self, statistics_df, save_path):
        raw_sharpe_ratio = statistics_df['{}_{}'.format(self.RAW_STRATEGY, self.SHARPE_RATIO)]
        raw_annualized_return = statistics_df['{}_{}'.format(self.RAW_STRATEGY, self.ANNUALIZED_RETURN)]
        alpha_sharpe = statistics_df['{}_{}'.format(self.ALPHA_STRATEGY, self.SHARPE_RATIO)]
        alpha_return = statistics_df['{}_{}'.format(self.ALPHA_STRATEGY, self.RETURN)]
        self.draw_histogram(data_series=raw_sharpe_ratio.dropna(),
                            xlabel='Raw Strategy Sharpe Ratio',
                            ylabel='Strategies Number', title='Histogram of Raw Strategy Sharpe Ratio',
                            save_path=os.path.join(save_path, 'raw_sharpe_ratio_histogram.png'))

        self.draw_histogram(data_series=raw_annualized_return.dropna(),
                            xlabel='Raw Strategy Annualized Return',
                            ylabel='Strategies Number', title='Histogram of Raw Strategy Annualized Return',
                            save_path=os.path.join(save_path, 'raw_ann_return_histogram.png'))

        self.draw_histogram(data_series=alpha_return.dropna(),
                            xlabel='Alpha Strategy Annualized Return',
                            ylabel='Strategies Number', title='Histogram of Alpha Strategy Annualized Return',
                            save_path=os.path.join(save_path, 'alpha_ann_return_histogram.png'))
        #
        self.draw_histogram(data_series=alpha_sharpe.dropna(),
                            xlabel='Alpha Strategy Sharpe Ratio',
                            ylabel='Strategies Number', title='Histogram of Alpha Strategy Sharpe Ratio',
                            save_path=os.path.join(save_path, 'alpha_sharpe_ratio_histogram.png'))

    def generate_histogram_from_result_path(self, result_path):
        """ Draw histogram picture from result path, histograms include sharpe and ann return of raw strategy and
            simple return and sharpe ratio of alpha strategy. Also will select best such strategy picture
        """

        self.logger.info('Start to draw histogram from result_path {}'.format(result_path))
        self._find_max_value_during_target_period(result_path=result_path, period=self.ALL)

    def _find_max_value_during_target_period(self, result_path, period):

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

        for key in [self.BEST_ALPHA_RETURN, self.BEST_ALPHA_SHARPE, self.MINIMAL_ALPHA_DRAWDOWN,
                    self.MINIMAL_RAW_DRAWDOWN, self.BEST_RAW_ANNUALIZED_RETURN, self.BEST_RAW_SHARPE_RATIO]:
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

            raw_sharpe_ratio = self.get_sharpe_ratio(raw_sub_df, df_type=self.WEALTH_DATAFRAME).dropna()
            raw_annualized_return = self.get_annualized_return(raw_sub_df, df_type=self.WEALTH_DATAFRAME).dropna()
            raw_max_drawdown = raw_sub_df.apply(self.get_max_draw_down, axis=0)
            alpha_sharpe_ratio = self.get_sharpe_ratio(alpha_sub_df, df_type=self.WEALTH_DATAFRAME).dropna()
            alpha_annualized_return = self.get_annualized_return(alpha_sub_df, df_type=self.WEALTH_DATAFRAME).dropna()
            alpha_max_drawdown = alpha_sub_df.apply(self.get_max_draw_down, axis=0)

            statistics_df = pd.DataFrame(index=raw_sharpe_ratio.index)
            statistics_df['{}_{}'.format(self.RAW_STRATEGY, self.SHARPE_RATIO)] = raw_sharpe_ratio
            statistics_df['{}_{}'.format(self.RAW_STRATEGY, self.ANNUALIZED_RETURN)] = raw_annualized_return
            statistics_df['{}_{}'.format(self.ALPHA_STRATEGY, self.SHARPE_RATIO)] = alpha_sharpe_ratio
            statistics_df['{}_{}'.format(self.ALPHA_STRATEGY, self.RETURN)] = alpha_annualized_return
            statistics_df_list.append(statistics_df)

            if start_date is None:
                self._draw_histogram_from_statistics(statistics_df, current_path)

            stop_loss_rate = re.findall(r'\d+', raw_df_name)[-1]

            for key in max_value_dict:
                self.logger.debug('Current key is {}'.format(key))
                if key.startswith(self.BEST_RAW_ANNUALIZED_RETURN):
                    data_series = raw_annualized_return

                elif key.startswith(self.BEST_RAW_SHARPE_RATIO):
                    data_series = raw_sharpe_ratio

                elif key.startswith(self.BEST_ALPHA_SHARPE):
                    data_series = alpha_sharpe_ratio

                elif key.startswith(self.MINIMAL_RAW_DRAWDOWN):
                    data_series = raw_max_drawdown

                elif key.startswith(self.MINIMAL_ALPHA_DRAWDOWN):
                    data_series = alpha_max_drawdown

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

        if start_date is None:
            merged_sta_df = pd.concat(statistics_df_list, axis=0, ignore_index=False)
            self._draw_histogram_from_statistics(merged_sta_df, result_path)

    def find_best_period_between_target_period(self, start_date, end_date, result_path):
        """ Find the best strategy between start_date and end_date """

        self.logger.info('Start to find best strategies between {} and {}'.format(start_date, end_date))
        self._find_max_value_during_target_period(result_path=result_path, period=[start_date, end_date])

    def _plot_multiline_picture_text(self, pic_title, data_list, legends, save_path, stop_loss_rate):

        self.logger.debug('Start to plot pic {}'.format(pic_title))
        # self.logger.debug('Data series is {}'.format(data_list))
        line1 = 'Transaction cost 0.2% SR {}%'.format(stop_loss_rate)

        info_list = [line1]

        raw_strategy = data_list[0]
        # beta_strategy = data_list[1]
        alpha_strategy = data_list[1]

        time_period = ['all', '09_14', '13_16', 'after_16']
        period_list = [(None, None), (datetime.datetime(2009, 1, 1), datetime.datetime(2015, 1, 1)),
                       (datetime.datetime(2013, 7, 22), datetime.datetime(2016, 7, 20)),
                       (datetime.datetime(2016, 2, 1), None)]

        def generate_line_info(i, date_tuple):
            current_line = 'Date {}'.format(time_period[i])
            result_list = [current_line]

            def get_line_not_alpha(data_series, prefix_info):
                if date_tuple[0] is not None:
                    sub_data_series = data_series[data_series.index > date_tuple[0]]
                else:
                    sub_data_series = data_series

                if date_tuple[1] is not None:
                    sub_data_series = sub_data_series[sub_data_series.index < date_tuple[1]]

                sharpe_ratio = self.get_sharpe_ratio(sub_data_series, df_type=self.WEALTH_DATAFRAME)
                ann_return = self.get_annualized_return(sub_data_series, df_type=self.WEALTH_DATAFRAME) * 100
                max_draw_down = self.get_max_draw_down(sub_data_series) * 100

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

            for prefix in ['Raw', 'Alpha']:

                if prefix == 'Raw':
                    result_list.append(get_line_not_alpha(raw_strategy, prefix))

                # elif prefix == 'Beta':
                #     result_list.append(get_line_not_alpha(beta_strategy, prefix))

                else:
                    result_list.append(get_line_not_alpha(alpha_strategy, prefix))

            return result_list

        for i, date_tuple in enumerate(period_list[:2]):
            info_list.extend(generate_line_info(i, date_tuple))

        text1 = '\n'.join(info_list)

        info_list = []
        for i, date_tuple in enumerate(period_list[2:]):
            info_list.extend(generate_line_info(i + 2, date_tuple))

        text2 = '\n'.join(info_list)

        self.logger.debug('Text1 is {}'.format(text1))
        self.logger.debug('Text2 is {}'.format(text2))
        self.logger.debug('Save path is {}'.format(save_path))

        self.plot_multiline_alpha(data_list,
                                  legend_list=legends,
                                  picture_title=pic_title,
                                  picture_save_path=save_path,
                                  text1=text1, text2=text2)

    def _sort_result(self, wealth_path, save_path, stop_loss_rate, p_path, bp_path2, bp_path15):
        self.logger.info('all info type processed finished, start generate result')
        wealth_result = self.merge_result(wealth_path)
        alpha_result = self.merge_alpha_strategy_result(wealth_path)
        today_str = datetime.datetime.today().strftime('%Y%m%d')

        # self.logger.debug('wealth result date list {}'.format(wealth_result.index))
        # self.logger.debug('alpha result date list {}'.format(alpha_result.index))

        save_types = [self.SAVE_TYPE_PICKLE, self.SAVE_TYPE_CSV]
        self._save_info(save_path, wealth_result, '{}_{}sr_raw'.format(today_str, stop_loss_rate), save_types)
        self._save_info(save_path, alpha_result, '{}_{}sr_alpha'.format(today_str, stop_loss_rate), save_types)

        statistic_df, best_strategy_df, sharpe_ratio, ann_return = self.generate_result_statistics(wealth_result)
        self._save_info(save_path, best_strategy_df, '{}_best_strategies_{}'.format(today_str, stop_loss_rate),
                        save_types)
        self._save_info(save_path, statistic_df, '{}_statistic_{}'.format(today_str, stop_loss_rate), save_types)

        labels = self.ALPHA_STRATEGY_LEGENDS

        for method in wealth_result.keys():
            self.logger.debug('Draw method {} picture'.format(method))
            if sharpe_ratio[method] > 2:
                pic_path = bp_path2
            elif sharpe_ratio[method] > 1.5:
                pic_path = bp_path15
            else:
                pic_path = p_path
            plot_data_list = [wealth_result[method], alpha_result[method]]

            self._plot_multiline_picture_text(method, plot_data_list, labels,
                                              os.path.join(pic_path, '{}.png'.format(method)), stop_loss_rate)

    @staticmethod
    def merge_result(result_path):
        file_list = os.listdir(result_path)

        df = pd.DataFrame()

        for file_name in file_list:
            if not file_name.endswith('.p') or 'raw' not in file_name:
                continue

            column_name = '_'.join(file_name.split('_')[:-1])
            col = pd.read_pickle(os.path.join(result_path, file_name))
            # if col.empty:
            #     continue
            # print column_name, col.first_valid_index(), col.last_valid_index()
            df[column_name] = col

        return df

    @staticmethod
    def merge_alpha_strategy_result(result_path):
        file_list = os.listdir(result_path)

        df = pd.DataFrame()

        for file_name in file_list:
            if not file_name.endswith('.p') or 'alpha' not in file_name:
                continue

            column_name = '_'.join(file_name.split('_')[:-1])
            col = pd.read_pickle(os.path.join(result_path, file_name))
            # print column_name, col.first_valid_index(), col.last_valid_index()
            df[column_name] = col

        # print 'alpha', df

        return df


if __name__ == '__main__':
    import sys
    import logging

    from xvfbwrapper import Xvfb

    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    suffix = 'forecast_report_stock_20170214'
    report_path = os.path.join(ReportGeneratorAlphaHedge.REPORT_DATA_PATH, 'report_info_buy_only')
    result_path = os.path.join(ReportGeneratorAlphaHedge.RESULT_PATH, suffix)

    stop_loss_rate = 0

    vdisplay = Xvfb(width=1366, height=768)
    vdisplay.start()
    test = ReportGeneratorAlphaHedge(0.002, report_path, suffix)
    w_path, s_path, r_path, p_path, bp_path15, bp_path2 = test._generate_useful_paths(stop_loss_rate)
    test._sort_result(w_path, s_path, stop_loss_rate, p_path, bp_path2, bp_path15)
    # test._sort_result(wealth_path=)
    vdisplay.stop()
