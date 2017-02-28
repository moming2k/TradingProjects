#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step23_sort_result
# @Date: 2017-02-28
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime

from report_generator.report_generator_add_alpha_hedge import ReportGeneratorAlphaHedge


class ReportGeneratorTemp(ReportGeneratorAlphaHedge):
    def _sort_result(self, wealth_path, save_path, stop_loss_rate, p_path, bp_path2, bp_path15):
        self.logger.info('all info type processed finished, start generate result')
        wealth_result = self.merge_result(wealth_path)

        wealth_result = wealth_result[wealth_result.index > datetime.datetime(2005, 1, 1)]
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


if __name__ == '__main__':
    import os
    import sys
    import logging

    from xvfbwrapper import Xvfb

    from constants.path_info import Path

    # from calculate_return_utils.calculate_return_utils_20170219 import CalculateReturnUtils20170219

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    transaction_cost = 0.002
    suffix = 'forecast_report_stock_20170214'
    report_path = os.path.join(Path.REPORT_DATA_PATH, 'report_data_20170224', 'forecast_report')

    vdisplay = Xvfb(width=1366, height=768)
    vdisplay.start()

    test_info = ReportGeneratorTemp(transaction_cost=transaction_cost, report_path=report_path,
                                    folder_suffix=suffix, trading_days_list_path=Path.TRADING_DAYS_20170216_PATH,
                                    stock_price_path=Path.STOCK_PRICE_20170214_PATH)

    test_info.INFO_TYPE_LIST = [test_info.ALL]
    #
    for i in range(6):
        #     test_info.main_progress(calculate_class=CalculateReturnUtils20170219, stop_loss_rate=i, sort_result=True)
        w_path, s_path, r_path, p_path, bp_path15, bp_path2 = test_info._generate_useful_paths(i)

        test_info._sort_result(w_path, s_path, i, p_path, bp_path2, bp_path15)

    result_path = os.path.join(Path.RESULT_PATH, suffix)
    test_info.generate_histogram_from_result_path(result_path)
    test_info.find_best_period_between_target_period(result_path=result_path,
                                                     end_date=datetime.datetime(2016, 7, 20),
                                                     start_date=datetime.datetime(2013, 7, 22))
    test_info.find_best_period_between_target_period(result_path=result_path,
                                                     end_date=datetime.datetime(2016, 7, 20),
                                                     start_date=datetime.datetime(2013, 7, 22)
                                                     )
    test_info.find_best_period_between_target_period(result_path=result_path,
                                                     end_date=datetime.datetime(2014, 12, 31),
                                                     start_date=datetime.datetime(2009, 1, 1),
                                                     )
    test_info.find_best_period_between_target_period(result_path=result_path,
                                                     end_date=None,
                                                     start_date=datetime.datetime(2016, 2, 1)
                                                     )
    vdisplay.stop()
