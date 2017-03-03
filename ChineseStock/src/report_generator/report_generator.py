#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: report_generator
# @Date: 2017-02-18
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime
import logging
import os
import re
import shutil

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import pathos

from ..util_functions.os_related import get_process_num, make_dirs
from ..util_functions.util_function_class import UtilFunction


class ReportGenerator(UtilFunction):
    @staticmethod
    def merge_result(result_path):
        file_list = os.listdir(result_path)

        df = pd.DataFrame()

        for file_name in file_list:
            if not file_name.endswith('.p') or 'beta' in file_name:
                continue

            column_name = file_name[:-2]
            df[column_name] = pd.read_pickle(os.path.join(result_path, file_name))

        return df

    @staticmethod
    def merge_beta_strategy_result(result_path):
        file_list = os.listdir(result_path)

        df = pd.DataFrame()

        for file_name in file_list:
            if not file_name.endswith('.p') or 'beta' not in file_name:
                continue

            column_name = '_'.join(file_name.split('_')[:-1])
            df[column_name] = pd.read_pickle(os.path.join(result_path, file_name))

        return df

    def generate_result_statistics(self, wealth_df):
        """ Based on input data generate statistics """
        result_df = pd.DataFrame(columns=wealth_df.keys())
        best_strategy_df = pd.DataFrame(columns=['name', 'sharpe_ratio', 'ann_return'])
        start_date = wealth_df.index[0]
        end_date = wealth_df.index[-1]
        return_df = (wealth_df - wealth_df.shift(1)) / wealth_df.shift(1)
        return_df.ix[start_date, :] = 0.

        sharpe_ratio = self.get_sharpe_ratio(return_df)
        ann_return = self.get_annualized_return(wealth_df)

        result_df.loc['total_return', :] = wealth_df.ix[end_date] / wealth_df.ix[start_date]
        result_df.loc['sharpe_ratio', :] = sharpe_ratio
        result_df.loc['annualized_return', :] = ann_return

        best_ann_name = ann_return.idxmax()
        best_sharpe_name = sharpe_ratio.idxmax()

        best_strategy_df.loc['ann_return'] = {
            'name': best_ann_name,
            'sharpe_ratio': sharpe_ratio[best_ann_name],
            'ann_return': ann_return.max()}
        best_strategy_df.loc['sharpe_ratio'] = {
            'name': best_sharpe_name,
            'sharpe_ratio': sharpe_ratio.max(),
            'ann_return': ann_return[best_sharpe_name]}

        return result_df, best_strategy_df, sharpe_ratio, ann_return

    def __init__(self, transaction_cost, report_path, folder_suffix, logger=None, stock_price_path=None,
                 trading_days_list_path=None):
        if logger is None:
            self.logger = logging.getLogger(self.__class__.__name__)

        else:
            self.logger = logger.getLogger(self.__class__.__name__)

        self.transaction_cost = transaction_cost
        self.report_path = report_path
        self.folder_name = folder_suffix
        self.pool = pathos.multiprocessing.ProcessingPool(get_process_num())
        if stock_price_path is None:
            self.stock_price_path = self.STOCK_PRICE_20170214_PATH

        else:
            self.stock_price_path = stock_price_path

        if trading_days_list_path is None:
            self.trading_days_list_path = self.TRADING_DAYS_20170228_PATH
        else:
            self.trading_days_list_path = trading_days_list_path

    def main_progress(self, calculate_class, stop_loss_rate, sort_result=True):
        self.logger.info('Start to calculate with transaction cost {}, stop loss: {}%'.format(self.transaction_cost,
                                                                                              stop_loss_rate))
        w_path, s_path, r_path, p_path, bp_path15, bp_path2 = self._generate_useful_paths(stop_loss_rate)

        portfolio_info = []
        for portfolio_num in self.PORTFOLIO_NUM_RANGE:
            for holding_days in self.HOLDING_DAYS_LIST:
                portfolio_info.append({self.PORTFOLIO_NUM: portfolio_num,
                                       self.HOLDING_DAYS: holding_days,
                                       self.TRANSACTION_COST: self.transaction_cost,
                                       self.REPORT_RETURN_PATH: r_path,
                                       self.WEALTH_DATA_PATH: w_path,
                                       self.STOPLOSS_RATE: -float(abs(stop_loss_rate)) / 100,
                                       self.REPORT_PATH: self.report_path})

        self._computation(calculate_class=calculate_class, portfolio_info=portfolio_info)
        if sort_result:
            self._sort_result(w_path, s_path, stop_loss_rate, p_path, bp_path2, bp_path15)

        self.logger.info('Process finished')

    def _save_info(self, save_path, save_df, save_name, save_types=None):
        self.logger.debug('Save {} to path {}'.format(save_name, save_path))

        if save_types is None:
            save_types = self.SAVE_TYPE_PICKLE

        if isinstance(save_types, str):
            save_types = [save_types]

        for save_type in save_types:
            if save_type == self.SAVE_TYPE_PICKLE:
                save_df.to_pickle(os.path.join(save_path, '{}.p'.format(save_name)))

            elif save_type == self.SAVE_TYPE_EXCEL:
                save_df.to_excel(os.path.join(save_path, '{}.xlsx'.format(save_name)))

            elif save_type == self.SAVE_TYPE_CSV:
                save_df.to_csv(os.path.join(save_path, '{}.csv'.format(save_name)))

    def _sort_result(self, wealth_path, save_path, stop_loss_rate, p_path, bp_path2, bp_path15):
        self.logger.info('all info type processed finished, start generate result')
        wealth_result = self.merge_result(wealth_path)
        beta_strategy_df = self.merge_beta_strategy_result(wealth_path)
        today_str = datetime.datetime.today().strftime('%Y%m%d')

        save_types = [self.SAVE_TYPE_PICKLE, self.SAVE_TYPE_CSV]
        self._save_info(save_path, wealth_result, '{}_{}sr'.format(today_str, stop_loss_rate), save_types)
        self._save_info(save_path, beta_strategy_df, '{}_{}sr_beta'.format(today_str, stop_loss_rate), save_types)

        statistic_df, best_strategy_df, sharpe_ratio, ann_return = self.generate_result_statistics(wealth_result)
        self._save_info(save_path, best_strategy_df, '{}_best_strategies_{}'.format(today_str, stop_loss_rate),
                        save_types)
        self._save_info(save_path, statistic_df, '{}_statistic_{}'.format(today_str, stop_loss_rate), save_types)

        labels = ['Raw Strategy', 'Beta Strategy', 'Alpha Strategy']

        for method in wealth_result.keys():
            self.logger.debug('Draw method {} picture'.format(method))
            if sharpe_ratio[method] > 2:
                pic_path = bp_path2
            elif sharpe_ratio[method] > 1.5:
                pic_path = bp_path15
            else:
                pic_path = p_path
            plot_data_list = [wealth_result[method], beta_strategy_df[method],
                              wealth_result[method] - beta_strategy_df[method]]

            self._plot_multiline_picture_text(method, plot_data_list, labels,
                                              os.path.join(pic_path, '{}.png'.format(method)), stop_loss_rate)

    def plot_multiline_alpha(self, data_list, legend_list, picture_title, picture_save_path, text1, text2):
        """ Draw data series info """

        # plot file and save picture
        fig = plt.figure(figsize=(15, 8))

        left = 0.1
        bottom = 0.3
        width = 0.75
        height = 0.60
        ax = fig.add_axes([left, bottom, width, height])
        ax.set_title(picture_title)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        plt.gca().xaxis.set_major_locator(mdates.YearLocator())
        plt.figtext(0.01, 0.01, text1, horizontalalignment='left')
        plt.figtext(0.51, 0.01, text2, horizontalalignment='left')

        date_series = data_list[0].index

        color_list = ['r-', 'b-', 'y-', 'g-']

        for i, data_series in enumerate(data_list):
            # get data series info
            plt.plot(date_series, data_series, color_list[i], label=legend_list[i])

        min_date = date_series[0]
        max_date = date_series[-1]
        plt.gca().set_xlim(min_date, max_date)
        plt.legend(loc=0)
        fig.autofmt_xdate()
        # fig.suptitle(picture_title)

        # print dir(fig)
        fig.savefig(picture_save_path)
        plt.close()

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
                # standard_dev = self.get_wealth_return_std(data_series)

                # current_line = 'Alpha: Pseude-Sharpe Ratio {:.3f}, Simple Return {:.2f}%, Std {:.4f}'.format(
                #     pse_sharpe_ratio, simple_return, standard_dev
                # )
                current_line = 'Alpha: Simple Return {:.2f}%'.format(
                    simple_return
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

    def _computation(self, calculate_class, portfolio_info):
        calculator = calculate_class(trading_list_path=self.trading_days_list_path,
                                     stock_price_path=self.stock_price_path)
        # calculator.initial_wealth = 1.0

        self.logger.info('Start to do the computation, the processor number is {}'.format(get_process_num()))
        # for info_type in [self.ALL]:
        for info_type in self.INFO_TYPE_LIST:
            self.logger.info('Start to handle info type {}'.format(info_type))

            def change_info_type(x):
                x[self.INFO_TYPE] = info_type
                return x

            new_portfolio_info = map(change_info_type, portfolio_info)

            self.pool.map(calculator.calculate_return_and_wealth, new_portfolio_info)
            self.logger.info('info type {} processed finished'.format(info_type))

    def _generate_useful_paths(self, stop_loss_rate):
        transaction_cost_str = str(int(round(1000 * self.transaction_cost)))

        wealth_path = os.path.join(self.TEMP_PATH, self.folder_name,
                                   'cost_{}_sr_{}_wealth'.format(transaction_cost_str,
                                                                 stop_loss_rate))

        save_path = os.path.join(self.RESULT_PATH, self.folder_name,
                                 'cost_{}_sr_{}'.format(transaction_cost_str,
                                                        stop_loss_rate))
        report_return_path = os.path.join(self.TEMP_PATH, self.folder_name,
                                          'cost_{}_sr_{}_report'.format(transaction_cost_str,
                                                                        stop_loss_rate))
        picture_save_path = os.path.join(save_path, 'picture')
        better_picture_save_path = os.path.join(save_path, 'picture_1_5')
        best_picture_save_path = os.path.join(save_path, 'picture_2')

        make_dirs(
            [wealth_path, save_path, report_return_path, picture_save_path, better_picture_save_path,
             best_picture_save_path])
        return wealth_path, save_path, report_return_path, picture_save_path, better_picture_save_path, \
               best_picture_save_path

    def _re_index_orginal_data(self, original_df, target_value):
        """ Reset target series to format data """
        original_df /= original_df.ix[original_df.first_valid_index()]
        original_df *= target_value
        return original_df

    def generate_histogram_from_result_path(self, result_path):
        """ Draw histogram picture from result path, histograms include sharpe and ann return of alpha strategy """

        self.logger.info('Start to draw histogram from result_path {}'.format(result_path))
        best_sharpe_ratio = 0.0
        best_sharpe_ratio_file_path = None
        best_ann_return = 0.0
        best_ann_return_file_path = None

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

            sharpe_ratio = self.get_sharpe_ratio(alpha_strategy_df, df_type=self.WEALTH_DATAFRAME)
            annualized_return = self.get_annualized_return(alpha_strategy_df, df_type=self.WEALTH_DATAFRAME)

            statistics_df = pd.DataFrame(index=sharpe_ratio.index)
            statistics_df['sharpe_ratio'] = sharpe_ratio
            statistics_df['annualized_return'] = annualized_return
            statistics_df_list.append(statistics_df)

            self.draw_histogram(sharpe_ratio.dropna(), 'Sharpe Ratio', 'Strategies', 'Histogram of Sharpe Ratio',
                                os.path.join(current_path, 'sharpe_ratio_histogram.png'))

            self.draw_histogram(annualized_return.dropna(), 'Annualized Return', 'Strategies',
                                'Histogram of Annualized Return',
                                os.path.join(current_path, 'ann_return_histogram.png'))

            stop_loss_rate = re.findall(r'\d+', wealth_file_name)[-1]

            best_sharpe_name = sharpe_ratio.idxmax()
            best_annualized_return_name = annualized_return.idxmax()

            best_sharpe_data_list = [raw_strategy_df[best_sharpe_name], beta_strategy_df[best_sharpe_name],
                                     alpha_strategy_df[best_sharpe_name]]
            self._plot_multiline_picture_text(data_list=best_sharpe_data_list,
                                              pic_title=best_sharpe_name, legends=self.ALPHA_STRATEGY_LEGENDS,
                                              save_path=os.path.join(current_path, 'best_sharpe_ratio.png'),
                                              stop_loss_rate=stop_loss_rate)
            best_ann_return_list = [raw_strategy_df[best_annualized_return_name],
                                    beta_strategy_df[best_annualized_return_name],
                                    alpha_strategy_df[best_annualized_return_name]]
            self._plot_multiline_picture_text(data_list=best_ann_return_list,
                                              pic_title=best_annualized_return_name,
                                              legends=self.ALPHA_STRATEGY_LEGENDS,
                                              save_path=os.path.join(current_path, 'best_ann_return.png'),
                                              stop_loss_rate=stop_loss_rate)
            if annualized_return[best_annualized_return_name] > best_ann_return:
                best_ann_return = annualized_return[best_annualized_return_name]
                best_ann_return_file_path = current_path

            if sharpe_ratio[best_sharpe_name] > best_sharpe_ratio:
                best_sharpe_ratio = sharpe_ratio[best_sharpe_name]
                best_sharpe_ratio_file_path = current_path

        if best_sharpe_ratio_file_path is not None:
            shutil.copy(os.path.join(best_sharpe_ratio_file_path, 'best_sharpe_ratio.png'),
                        os.path.join(result_path, 'best_sharpe_ratio.png'))

        if best_ann_return_file_path is not None:
            shutil.copy(os.path.join(best_ann_return_file_path, 'best_ann_return.png'),
                        os.path.join(result_path, 'best_ann_return.png'))

        merged_sta_df = pd.concat(statistics_df_list, axis=0, ignore_index=False)

        self.draw_histogram(merged_sta_df['sharpe_ratio'].dropna(), 'Sharpe Ratio', 'Strategies',
                            'Histogram of Sharpe Ratio',
                            os.path.join(result_path, 'sharpe_ratio_histogram.png'))

        self.draw_histogram(merged_sta_df['annualized_return'].dropna(), 'Annualized Return', 'Strategies',
                            'Histogram of Annualized Return',
                            os.path.join(result_path, 'ann_return_histogram.png'))
