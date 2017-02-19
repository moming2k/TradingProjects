#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: step20_generate_insider_si_own_cd_report
# Author: warn
# Date: warn

from ChineseStock.src.report_generator.report_generator_draw_alpha_strategies import ReportGeneratorDrawAlphaStrategies
from ChineseStock.src.util_functions.os_related import get_process_num


class ReportGenerator(ReportGeneratorDrawAlphaStrategies):
    def _computation(self, calculate_class, portfolio_info):
        calculator = calculate_class()
        # calculator.initial_wealth = 1.0

        self.logger.info('Start to do the computation, the processor number is {}'.format(get_process_num()))
        # for info_type in [self.ALL]:
        for info_type in [self.ALL]:
            self.logger.info('Start to handle info type {}'.format(info_type))

            def change_info_type(x):
                x[self.INFO_TYPE] = info_type
                return x

            new_portfolio_info = map(change_info_type, portfolio_info)

            self.pool.map(calculator.calculate_return_and_wealth, new_portfolio_info)
            self.logger.info('info type {} processed finished'.format(info_type))


if __name__ == '__main__':
    import os
    import sys
    import logging

    from xvfbwrapper import Xvfb

    from ChineseStock.src.constants.path_info import Path
    from ChineseStock.src.calculate_return_utils.calculate_return_utils_20170216 import CalculateReturnUtils20170216

    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    transaction_cost = 0.002
    suffix = 'all_report_stoct_20170224'
    report_path = os.path.join(Path.REPORT_DATA_PATH, 'report_data_20170205', 'ticker_sep')

    vdisplay = Xvfb(width=1366, height=768)
    vdisplay.start()

    test_info = ReportGenerator(transaction_cost=transaction_cost, report_path=report_path,
                                folder_suffix=suffix)

    for i in range(6):
        test_info.main_progress(calculate_class=CalculateReturnUtils20170216, stop_loss_rate=i)

    vdisplay.stop()
