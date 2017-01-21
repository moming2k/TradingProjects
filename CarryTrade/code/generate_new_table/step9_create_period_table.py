#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step9_create_period_table
# @Date: 2017-01-20
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

# import os
import re

import pandas as pd
from scipy import stats

from util_function import date_as_float
# from path_info import return_data_path
from constant import Constant as const
from constant import TIME_SEP
from step3_spa_src_stepwise_test import spa_src_p_value, stepwise_spa_test, bootstrap


def create_period_table(data_df, month_period=const.ONE_MONTH,
                        period_index=1, sep_num=4, test_time=500, bootstrap_sample=1000):
    if sep_num == 4:
        time_sep_list = TIME_SEP[::2]

    else:
        time_sep_list = TIME_SEP[:]

    in_start_date = time_sep_list[period_index - 1]
    in_end_date = out_start_date = time_sep_list[period_index]
    out_end_date = time_sep_list[period_index + 1]

    sample_df = data_df[data_df.index < in_end_date]
    sample_df = sample_df[sample_df.index >= in_start_date]

    out_sample_df = data_df[data_df.index < out_end_date]
    out_sample_df = out_sample_df[out_sample_df.index >= out_start_date]

    # the following rows are used to generate best strategy rows
    row_list = [const.BEST_STRATEGY_DESCRIPTION]
    for suffix in [const.IN_SAMPLE, const.OUT_OF_SAMPLE]:
        for prefix in [const.BEST_STRATEGY_MEAN_RETURN, const.BEST_STRATEGY_NOMINAL_P_VALUE,
                       const.BEST_STRATEGY_RC_P_VALUE, const.BEST_STRATEGY_ST_P_VALUE]:
            row_list.append('{} {}'.format(prefix, suffix))

    # the following rows are about all profitable strategies
    for suffix in [const.IN_SAMPLE, const.OUT_OF_SAMPLE]:
        for prefix in [const.AVERAGE_REJECT_NUM, const.AVERAGE_REJECT_PORTION]:
            row_list.append('{} {}'.format(prefix, suffix))

    result_df = pd.DataFrame(index=row_list, columns=['{} {}'.format(const.MEAN_RETURN, month_period),
                                                      '{} {}'.format(const.SHARPE_RATIO, month_period)])

    # Some parameters that would be used in following test
    sharpe_parameter = (12.0 / float(month_period[:-1])) ** 0.5
    sample_mean = sample_df.mean()
    sample_wealth = (sample_df + 1).cumprod().ix[sample_df.last_valid_index()]
    sample_ann = sample_wealth ** (1 / (date_as_float(in_end_date) - date_as_float(in_start_date))) - 1
    sample_sharpe = sample_mean / sample_df.std() * sharpe_parameter

    out_sample_mean = out_sample_df.mean()
    out_sample_wealth = (out_sample_df + 1).cumprod().ix[out_sample_df.last_valid_index()]
    out_sample_ann = out_sample_wealth ** (1 / (date_as_float(out_end_date) - date_as_float(out_start_date))) - 1
    out_sample_sharpe = out_sample_mean / out_sample_df.std() * sharpe_parameter

    for test_method in [const.MEAN_RETURN, const.SHARPE_RATIO]:
        column_name = '{} {}'.format(test_method, month_period)

        if test_method == const.MEAN_RETURN:
            best_strategy_name = sample_mean.idxmax()
            result_df.loc['{} {}'.format(const.BEST_STRATEGY_MEAN_RETURN,
                                         const.IN_SAMPLE), column_name] = sample_ann[best_strategy_name]
            result_df.loc['{} {}'.format(const.BEST_STRATEGY_MEAN_RETURN,
                                         const.OUT_OF_SAMPLE), column_name] = out_sample_ann[best_strategy_name]

        else:
            best_strategy_name = sample_sharpe.idxmax()
            result_df.loc['{} {}'.format(const.BEST_STRATEGY_MEAN_RETURN,
                                         const.IN_SAMPLE), column_name] = sample_sharpe[best_strategy_name]
            result_df.loc['{} {}'.format(const.BEST_STRATEGY_MEAN_RETURN,
                                         const.OUT_OF_SAMPLE), column_name] = out_sample_sharpe[best_strategy_name]

        description_info = re.findall('\d+', best_strategy_name)
        if 'memory' in best_strategy_name:
            description = '({d[1]}r, {d[2]}m, {d[3]}m)'.format(d=description_info)
        else:
            description = '({d[1]}l, {d[2]}p, {d[3]}m)'.format(d=description_info)
        result_df.loc[const.BEST_STRATEGY_DESCRIPTION, column_name] = description

        result_df.loc['{} {}'.format(const.BEST_STRATEGY_NOMINAL_P_VALUE, const.IN_SAMPLE), column_name] = \
            stats.ttest_1samp(sample_df[best_strategy_name], 0.).pvalue
        result_df.loc['{} {}'.format(const.BEST_STRATEGY_NOMINAL_P_VALUE, const.OUT_OF_SAMPLE), column_name] = \
            stats.ttest_1samp(out_sample_df[best_strategy_name], 0.).pvalue

        in_rc_p_value = 0.
        out_rc_p_value = 0.
        in_st_p_value = 0.
        out_st_p_value = 0.

        in_reject_num = 0.
        out_reject_num = 0.

        for i in range(test_time):
            sample_boot_df = bootstrap(sample_df, bootstrap_sample)
            sample_rc_p_value, sample_st_p_value = spa_src_p_value(sample_df, sample_boot_df,
                                                                   best_strategy_name, test_method)
            sample_reject_columns = stepwise_spa_test(sample_df, sample_boot_df, test_method)
            in_reject_num += len(sample_reject_columns)

            in_rc_p_value += sample_rc_p_value
            in_st_p_value += sample_st_p_value

            out_sample_boot_df = bootstrap(out_sample_df, bootstrap_sample)
            out_sample_rc_p_value, out_sample_st_p_value = spa_src_p_value(out_sample_df, out_sample_boot_df,
                                                                           best_strategy_name, test_method)

            out_sample_reject_columns = stepwise_spa_test(out_sample_df, out_sample_boot_df, test_method,
                                                          sample_reject_columns)

            out_rc_p_value += out_sample_rc_p_value
            out_st_p_value += out_sample_st_p_value
            out_reject_num += len(out_sample_reject_columns)

        fl_test_time = float(test_time)
        result_df.loc['{} {}'.format(const.BEST_STRATEGY_RC_P_VALUE, const.IN_SAMPLE),
                      column_name] = in_rc_p_value / fl_test_time
        result_df.loc['{} {}'.format(const.BEST_STRATEGY_RC_P_VALUE, const.OUT_OF_SAMPLE),
                      column_name] = out_rc_p_value / fl_test_time

        result_df.loc['{} {}'.format(const.BEST_STRATEGY_ST_P_VALUE, const.IN_SAMPLE),
                      column_name] = in_st_p_value / fl_test_time
        result_df.loc['{} {}'.format(const.BEST_STRATEGY_ST_P_VALUE, const.OUT_OF_SAMPLE),
                      column_name] = out_st_p_value / fl_test_time

        result_df.loc['{} {}'.format(const.AVERAGE_REJECT_NUM, const.IN_SAMPLE),
                      column_name] = in_reject_num / fl_test_time
        result_df.loc['{} {}'.format(const.AVERAGE_REJECT_NUM, const.OUT_OF_SAMPLE),
                      column_name] = out_reject_num / fl_test_time

        result_df.loc['{} {}'.format(const.AVERAGE_REJECT_PORTION, const.IN_SAMPLE),
                      column_name] = in_reject_num / fl_test_time / data_df.shape[1]
        result_df.loc['{} {}'.format(const.AVERAGE_REJECT_PORTION, const.OUT_OF_SAMPLE),
                      column_name] = out_reject_num / fl_test_time / data_df.shape[1]

    return result_df
