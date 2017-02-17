#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step19_generate_insider_relationship_ewin3011
# @Date: 2017-02-17
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import re
import shutil
import logging
import datetime

import pathos
import pandas as pd

from path_info import Path
from os_related import get_process_num, make_dirs
from util_function_class import UtilFunction


class ReportGenerator(Path, UtilFunction):
    def __init__(self, transaction_cost, report_path, folder_suffix, logger=None):
        if logger is None:
            self.logger = logging.getLogger(self.__class__.__name__)

        else:
            self.logger = logger.getLogger(self.__class__.__name__)

        self.transaction_cost = transaction_cost
        self.report_path = report_path
        self.folder_name = folder_suffix
        self.pool = pathos.multiprocessing.ProcessingPool(get_process_num())

    def main_progress(self, calculate_class, stop_loss_rate):
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
        self._sort_result(w_path, s_path, stop_loss_rate, p_path, bp_path2, bp_path15)
        self._draw_histogram(s_path)

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
        alpha_strategy_result = self.merge_alpha_strategy_result(wealth_path)
        today_str = datetime.datetime.today().strftime('%Y%m%d')

        save_types = [self.SAVE_TYPE_PICKLE, self.SAVE_TYPE_CSV]
        self._save_info(save_path, wealth_result, '{}_{}sr'.format(today_str, stop_loss_rate), save_types)
        self._save_info(save_path, alpha_strategy_result, '{}_{}sr_alpha'.format(today_str, stop_loss_rate), save_types)

        statistic_df, best_strategy_df, sharpe_ratio, ann_return = self.generate_result_statistics(wealth_result)
        self._save_info(save_path, best_strategy_df, '{}_best_strategies_{}'.format(today_str, stop_loss_rate),
                        save_types)
        self._save_info(save_path, statistic_df, '{}_statistic_{}'.format(today_str, stop_loss_rate), save_types)

        labels = ['Raw Strategy', 'Beta Strategy', 'Beta Strategy']

        for method in wealth_result.keys():
            self.logger.debug('Draw method {} picture'.format(method))
            if sharpe_ratio[method] > 2:
                pic_path = bp_path2
            elif sharpe_ratio[method] > 1.5:
                pic_path = bp_path15
            else:
                pic_path = p_path
            plot_data_list = [wealth_result[method], alpha_strategy_result[method],
                              wealth_result[method] - alpha_strategy_result[method]]

            self._plot_multiline_picture_text(method, plot_data_list, labels,
                                              os.path.join(pic_path, '{}.png'.format(method)), stop_loss_rate)

    def _plot_multiline_picture_text(self, pic_title, data_list, legends, save_path, stop_loss_rate):

        self.logger.debug('Start to plot pic {}'.format(pic_title))
        report_list = [data_list[0], data_list[0][data_list[0].index < datetime.datetime(2015, 1, 1)],
                       data_list[0][data_list[0].index > datetime.datetime(2015, 1, 1)]]
        line1 = 'Transaction cost 0.2% SR {}%'.format(stop_loss_rate)
        info_list = [line1]
        time_period = ['all', 'before_2015', 'after_2015']

        for i, i_series in enumerate(report_list):
            sharpe_ratio = self.get_sharpe_ratio(i_series, df_type=self.WEALTH_DATAFRAME)
            ann_return = self.get_annualized_return(i_series, df_type=self.WEALTH_DATAFRAME)
            max_draw_down = self.get_max_draw_down(i_series)
            line = 'Data {}: Sharpe ratio {:.3f}, Annualized return {:.2f}%, Max drawdown rate {:.2f}%'.format(
                time_period[i], sharpe_ratio, ann_return, max_draw_down
            )
            info_list.append(line)

        text = '\n'.join(info_list)
        self.plot_multiline(data_list, legends, pic_title, save_path, text)

    def _computation(self, calculate_class, portfolio_info):
        calculator = calculate_class()

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

    def _draw_histogram(self, result_path):

        self.logger.info('Start to draw histogram')
        best_sharpe_ratio = 0.0
        best_sharpe_ratio_file_path = None
        best_ann_return = 0.0
        best_ann_return_file_path = None

        statistics_df_list = []

        dir_list = os.listdir(result_path)

        labels = ['Raw Strategy', 'Beta Strategy', 'Beta Strategy']

        for dir_name in dir_list:
            self.logger.info('handle dir {}'.format(dir_name))
            current_path = os.path.join(result_path, dir_name)
            if not os.path.isdir(current_path):
                continue

            statistics_file_name = self.get_target_file_name(current_path, 'statistic', 'p')
            wealth_file_name = self.get_target_file_name(current_path, 'sr.', 'p')
            alpha_file_name = self.get_target_file_name(current_path, 'alpha', 'p')

            if statistics_file_name is None or wealth_file_name is None or alpha_file_name is None:
                continue

            statistics_df = pd.read_pickle(os.path.join(current_path, statistics_file_name))
            statistics_df_t = statistics_df.transpose()
            statistics_df_list.append(statistics_df_t)

            wealth_df = pd.read_pickle(os.path.join(current_path, wealth_file_name))
            alpha_df = pd.read_pickle(os.path.join(current_path, alpha_file_name))

            self.draw_histogram(statistics_df_t['sharpe_ratio'], 'Sharpe Ratio', 'Strategies',
                                'Histogram of Sharpe Ratio',
                                os.path.join(current_path, 'sharpe_ratio_histogram.png'))

            self.draw_histogram(statistics_df_t['annualized_return'], 'Annualized Return', 'Strategies',
                                'Histogram of Annualized Return',
                                os.path.join(current_path, 'ann_return_histogram.png'))

            stop_loss_rate = re.findall(r'\d+', wealth_file_name)[-1]

            best_sharpe_name = statistics_df_t.sharpe_ratio.idxmax()
            best_annualized_return_name = statistics_df_t.annualized_return.idxmax()

            self._plot_multiline_picture_text(pic_title=best_sharpe_name, legends=labels,
                                              data_list=[wealth_df[best_sharpe_name], alpha_df[best_sharpe_name],
                                                         wealth_df[best_sharpe_name] - alpha_df[best_sharpe_name]],
                                              save_path=os.path.join(current_path, 'best_sharpe_ratio.png'),
                                              stop_loss_rate=stop_loss_rate)

            self._plot_multiline_picture_text(pic_title=best_annualized_return_name, legends=labels,
                                              data_list=[wealth_df[best_annualized_return_name],
                                                         alpha_df[best_annualized_return_name],
                                                         wealth_df[best_annualized_return_name] -
                                                         alpha_df[best_annualized_return_name]],
                                              save_path=os.path.join(current_path, 'best_ann_return.png'),
                                              stop_loss_rate=stop_loss_rate)
            if statistics_df.ix['annualized_return', best_annualized_return_name] > best_ann_return:
                best_ann_return = statistics_df.ix['annualized_return', best_annualized_return_name]
                best_ann_return_file_path = current_path

            if statistics_df.ix['sharpe_ratio', best_sharpe_name] > best_sharpe_ratio:
                best_sharpe_ratio = statistics_df.ix['sharpe_ratio', best_sharpe_name]
                best_sharpe_ratio_file_path = current_path

        if best_sharpe_ratio_file_path is not None:
            shutil.copy(os.path.join(best_sharpe_ratio_file_path, 'best_sharpe_ratio.png'),
                        os.path.join(result_path, 'best_sharpe_ratio.png'))

        if best_ann_return_file_path is not None:
            shutil.copy(os.path.join(best_ann_return_file_path, 'best_ann_return.png'),
                        os.path.join(result_path, 'best_ann_return.png'))

        merged_sta_df = pd.concat(statistics_df_list, axis=0, ignore_index=False)

        self.draw_histogram(merged_sta_df['sharpe_ratio'], 'Sharpe Ratio', 'Strategies', 'Histogram of Sharpe Ratio',
                            os.path.join(result_path, 'sharpe_ratio_histogram.png'))

        self.draw_histogram(merged_sta_df['annualized_return'], 'Annualized Return', 'Strategies',
                            'Histogram of Annualized Return',
                            os.path.join(result_path, 'ann_return_histogram.png'))


if __name__ == '__main__':

    import sys

    from xvfbwrapper import Xvfb

    from path_info import Path
    from calculate_return_utils_20170216 import CalculateReturnUtils20170216

    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    transaction_cost = 0.002
    suffix = 'insider_stock_20170214_alpha_no_neglect_all_types'
    report_path = os.path.join(Path.REPORT_DATA_PATH, 'report_info_buy_only')

    vdisplay = Xvfb(width=1366, height=768)
    vdisplay.start()

    test_info = ReportGenerator(transaction_cost=transaction_cost, report_path=report_path,
                                folder_suffix=suffix)

    for i in range(2):
        test_info.main_progress(calculate_class=CalculateReturnUtils20170216, stop_loss_rate=i)

    vdisplay.stop()
