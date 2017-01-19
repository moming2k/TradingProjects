#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step3_spa_src_stepwise_test
# @Date: 2017-01-17
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import re
import datetime

import pandas as pd
import numpy as np
from scipy import stats

from constant import Constant as const
from path_info import return_data_path
from util_function import date_as_float


def bootstrap(data_df, num):
    """
    generate bootstrap info
    :param data_df: input data frame, column is carry trade method, row is date
    :param num: bootstrap times
    :return: bootstrap sample
    """
    df_mean = data_df.mean()
    df_demean = data_df - df_mean
    result_df = pd.DataFrame(columns=data_df.keys())
    data_length = data_df.shape[0]
    for i in range(num):
        result_df.loc[i, :] = df_demean.sample(data_length, replace=True).mean()

    return result_df


def stepwise_spa_test(data_df, bootstrap_df, test_method=const.MEAN_RETURN):
    """ Do stepwise spa test """
    data_length = data_df.shape[0]
    data_mean = data_df.mean()
    data_std = data_df.std()
    data_sharpe = data_mean / data_std
    if test_method == const.MEAN_RETURN:
        sspa_statistics = data_mean
        test_df = bootstrap_df

    else:
        sspa_statistics = data_length ** 0.5 * data_sharpe
        recenter_parameter = (2 * np.log(np.log(data_length))) ** 0.5
        recenter_vector = data_mean * (sspa_statistics < recenter_parameter)
        test_df = (data_length ** 0.5) * bootstrap_df / data_std + data_length ** 0.5 * (recenter_vector / data_std)

    drop_column = []
    while len(drop_column) < data_df.shape[1]:
        boot_mean_df = test_df.drop(drop_column, axis=1)
        boot_sspa_statistic = pd.Series()
        temp_sspa_statistics = sspa_statistics.drop(drop_column)
        for i in test_df.index:
            boot_sspa_statistic.loc[i] = boot_mean_df.ix[i].max()

        cv = boot_sspa_statistic.nlargest(n=(int(test_df.shape[0] * 0.05) + 1)).min()
        new_drop_column = temp_sspa_statistics[temp_sspa_statistics > cv].keys()
        if len(new_drop_column) == 0:
            break
        else:
            drop_column.extend(new_drop_column)

    return len(drop_column)


def spa_or_src_test(data_df, bootstrap_df, test_type=const.SRC, test_method=const.MEAN_RETURN):
    data_length = data_df.shape[0]
    data_mean = data_df.mean()
    data_std = data_df.std()
    data_sharpe = data_mean / data_std

    if test_type == const.SRC:
        # generate src df
        test_df = (data_length ** 0.5) * bootstrap_df / data_std
        test_statistics = (data_length ** 0.5) * (data_sharpe)

    else:
        # generate spa df
        if test_method == const.MEAN_RETURN:
            test_statistics = data_mean
            test_df = bootstrap_df

        else:
            test_statistics = (data_length ** 0.5) * (data_sharpe)
            recenter_parameter = (2 * np.log(np.log(data_length))) ** 0.5
            recenter_vector = data_mean * (test_statistics < recenter_parameter)
            test_df = (data_length ** 0.5) * bootstrap_df / data_std + data_length ** 0.5 * (recenter_vector / data_std)

    k_sim_max = pd.Series()
    for i in test_df.index:
        k_sim_max.loc[i] = test_df.ix[i].max()

    cv = k_sim_max.nlargest(n=(int(test_df.shape[0] * 0.05) + 1)).min()
    reject_num = test_statistics[test_statistics > cv].shape[0]
    best_strategy_p_value = float(k_sim_max[k_sim_max > test_statistics.max()].shape[0]) / k_sim_max.shape[0]

    return reject_num, best_strategy_p_value


def generate_table_3or4(test_time=500, bootstrap_num=1000, currency_num='48'):
    column_list = []
    for i in [const.MEAN_RETURN, const.SHAPRE_RATIO]:
        for j in [const.ONE_MONTH, const.THREE_MONTH, const.SIX_MONTH, const.TWELVE_MONTH]:
            column_list.append('{} {}'.format(i, j))
    result_df = pd.DataFrame(columns=column_list, index=[const.STRATEGY_NUM, const.BEST_STRATEGY_DESCRIPTION,
                                                         const.BEST_STRATEGY_MEAN_RETURN,
                                                         const.BEST_STRATEGY_SHAPRE_RATIO,
                                                         const.BEST_STRATEGY_NOMINAL_P_VALUE,
                                                         const.BEST_STRATEGY_RC_P_VALUE,
                                                         const.BEST_STRATEGY_ST_P_VALUE,
                                                         const.AVERAGE_REJECT_NUM,
                                                         const.MINIMUM_REJECT_NUM,
                                                         const.MAXIMUM_REJECT_NUM,
                                                         const.AVERAGE_REJECT_PORTION])
    for file_info in os.listdir(return_data_path):
        if not file_info.endswith('.p') or currency_num not in file_info:
            continue

        month_info = re.findall(r'\d+m', file_info)
        if len(month_info) == 0:
            continue

        month = month_info[0]
        df = pd.read_pickle(os.path.join(return_data_path, file_info))
        sharpe_parameter = (12.0 / float(month[:-1])) ** 0.5
        start_date = datetime.datetime(df.index[0].year, 1, 1)
        end_date = df.index[-1]
        wealth_df = (df + 1).cumprod()
        mean_return = df.mean()
        annualized_return = (wealth_df.tail(1) ** (date_as_float(end_date) - date_as_float(start_date))
                             - 1).ix[df.index[-1]]
        sharpe_ratio = mean_return / df.std() * sharpe_parameter

        for key in [const.MEAN_RETURN, const.SHAPRE_RATIO]:
            column_name = '{} {}'.format(key, month)
            result_df.loc[const.STRATEGY_NUM, column_name] = df.shape[1]
            if key == const.MEAN_RETURN:
                best_strategy_name = mean_return.idxmax()
            else:
                best_strategy_name = sharpe_ratio.idxmax()

            description_info = re.findall('\d+', best_strategy_name)
            result_df.loc[const.BEST_STRATEGY_DESCRIPTION, column_name] = '({d[1]}l, {d[2]}p, {d[3]}m)'.format(
                d=description_info)
            result_df.loc[const.BEST_STRATEGY_MEAN_RETURN, column_name] = annualized_return[best_strategy_name]
            result_df.loc[const.BEST_STRATEGY_SHAPRE_RATIO, column_name] = sharpe_ratio[best_strategy_name]
            result_df.loc[const.BEST_STRATEGY_NOMINAL_P_VALUE, column_name] = stats.ttest_1samp(
                df[best_strategy_name], 0.
            ).pvalue

            best_rc_p_value = 0.0
            best_st_p_value = 0.0
            total_reject_num = 0.0
            max_reject_num = float('-inf')
            min_reject_num = float('inf')

            for i in range(test_time):
                boot_df = bootstrap(data_df=df, num=bootstrap_num)
                rc_reject_num, rc_p_value = spa_or_src_test(df, bootstrap_df=boot_df, test_type=const.SRC,
                                                            test_method=key)
                pa_reject_num, pa_p_value = spa_or_src_test(df, bootstrap_df=boot_df, test_type=const.SPA,
                                                            test_method=key)
                st_reject_num = stepwise_spa_test(df, bootstrap_df=boot_df, test_method=key)

                # TODO: understand what reject num should be recorded

                best_rc_p_value += rc_p_value
                best_st_p_value += pa_p_value

            result_df.loc[const.BEST_STRATEGY_ST_P_VALUE, column_name] = best_st_p_value / test_time
            result_df.loc[const.BEST_STRATEGY_RC_P_VALUE, column_name] = best_rc_p_value / test_time
            result_df.loc[const.BEST_STRATEGY_RC_P_VALUE, column_name] = best_rc_p_value / test_time
            result_df.loc[const.AVERAGE_REJECT_NUM, column_name] = total_reject_num / test_time
            result_df.loc[const.MINIMUM_REJECT_NUM, column_name] = min_reject_num
            result_df.loc[const.MAXIMUM_REJECT_NUM, column_name] = max_reject_num
            result_df.loc[const.AVERAGE_REJECT_PORTION, column_name] = total_reject_num / float(test_time) / df.shape[1]

    return result_df
