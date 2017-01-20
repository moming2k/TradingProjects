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
from path_info import return_data_path, temp_path
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


def stepwise_spa_test(data_df, bootstrap_df, test_method=const.MEAN_RETURN, in_sample_column=None):
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

    if in_sample_column is not None:
        return list(set(drop_column).intersection(in_sample_column))
    else:
        return drop_column


def spa_src_p_value(data_df, bootstrap_df, strategy_name, test_method=const.MEAN_RETURN):
    data_length = data_df.shape[0]
    data_mean = data_df.mean()
    data_std = data_df.std()
    data_sharpe = data_mean / data_std

    # the following code are used to generate src p value
    test_df = (data_length ** 0.5) * bootstrap_df / data_std
    test_statistics = (data_length ** 0.5) * (data_sharpe)
    k_sim_max = pd.Series()
    for i in test_df.index:
        k_sim_max.loc[i] = test_df.ix[i].max()

    src_p_value = float(k_sim_max[k_sim_max > test_statistics[strategy_name]].shape[0]) / k_sim_max.shape[0]

    # the following code are used to generate spa p value
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

    spa_p_value = float(k_sim_max[k_sim_max > test_statistics[strategy_name]].shape[0]) / k_sim_max.shape[0]

    return src_p_value, spa_p_value


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


def generate_table_3or4(file_path, test_time=500, bootstrap_num=1000):
    index_list = [const.STRATEGY_NUM, const.BEST_STRATEGY_DESCRIPTION,
                  const.BEST_STRATEGY_MEAN_RETURN,
                  const.BEST_STRATEGY_SHARPE_RATIO,
                  const.BEST_STRATEGY_NOMINAL_P_VALUE,
                  const.BEST_STRATEGY_RC_P_VALUE,
                  const.BEST_STRATEGY_ST_P_VALUE,
                  const.AVERAGE_REJECT_NUM,
                  const.MINIMUM_REJECT_NUM,
                  const.MAXIMUM_REJECT_NUM,
                  const.AVERAGE_REJECT_PORTION
                  ]

    # for i in ['rc', 'pa', 'st']:
    #     for j in [const.AVERAGE_REJECT_NUM,
    #               const.MINIMUM_REJECT_NUM,
    #               const.MAXIMUM_REJECT_NUM,
    #               const.AVERAGE_REJECT_PORTION]:
    #         index_list.append('{}_{}'.format(j, i))

    # generate column list info

    month_info = re.findall(r'\d+m', file_path)
    if len(month_info) == 0:
        return pd.DataFrame()

    month = month_info[0]
    column_list = []
    for i in [const.MEAN_RETURN, const.SHARPE_RATIO]:
        column_list.append('{} {}'.format(i, month))
        # for j in [const.ONE_MONTH, const.THREE_MONTH, const.SIX_MONTH, const.TWELVE_MONTH]:
        #     column_list.append('{} {}'.format(i, j))
    result_df = pd.DataFrame(columns=column_list, index=index_list)
    df = pd.read_pickle(file_path)
    sharpe_parameter = (12.0 / float(month[:-1])) ** 0.5
    start_date = datetime.datetime(df.index[0].year, 1, 1)
    end_date = df.index[-1]
    wealth_df = (df + 1).cumprod().ix[df.last_valid_index()]
    mean_return = df.mean()
    annualized_return = wealth_df ** (1 / (date_as_float(end_date) - date_as_float(start_date))) - 1
    sharpe_ratio = mean_return / df.std() * sharpe_parameter

    for key in [const.MEAN_RETURN, const.SHARPE_RATIO]:
        column_name = '{} {}'.format(key, month)
        result_df.loc[const.STRATEGY_NUM, column_name] = df.shape[1]
        if key == const.MEAN_RETURN:
            best_strategy_name = mean_return.idxmax()
        else:
            best_strategy_name = sharpe_ratio.idxmax()

        description_info = re.findall('\d+', best_strategy_name)
        if 'memory' in best_strategy_name:
            description = '({d[1]}r, {d[2]}m, {d[3]}m)'.format(
                d=description_info)
        else:
            description = '({d[1]}l, {d[2]}p, {d[3]}m)'.format(
                d=description_info)
        result_df.loc[const.BEST_STRATEGY_DESCRIPTION, column_name] = description
        result_df.loc[const.BEST_STRATEGY_MEAN_RETURN, column_name] = annualized_return[best_strategy_name]
        result_df.loc[const.BEST_STRATEGY_SHARPE_RATIO, column_name] = sharpe_ratio[best_strategy_name]
        result_df.loc[const.BEST_STRATEGY_NOMINAL_P_VALUE, column_name] = stats.ttest_1samp(
            df[best_strategy_name], 0.
        ).pvalue

        best_rc_p_value = 0.0
        best_st_p_value = 0.0

        total_reject_num = {}
        max_reject_num = {}
        min_reject_num = {}

        for i in ['rc', 'pa', 'st']:
            total_reject_num[i] = 0.0
            max_reject_num[i] = float('-inf')
            min_reject_num[i] = float('inf')

        for i in range(test_time):
            boot_df = bootstrap(data_df=df, num=bootstrap_num)
            rc_reject_num, rc_p_value = spa_or_src_test(df, bootstrap_df=boot_df, test_type=const.SRC,
                                                        test_method=key)
            pa_reject_num, pa_p_value = spa_or_src_test(df, bootstrap_df=boot_df, test_type=const.SPA,
                                                        test_method=key)
            st_reject_num = len(stepwise_spa_test(df, bootstrap_df=boot_df, test_method=key))

            total_reject_num['rc'] += rc_reject_num
            min_reject_num['rc'] = min(min_reject_num['rc'], rc_reject_num)
            max_reject_num['rc'] = max(max_reject_num['rc'], rc_reject_num)

            total_reject_num['pa'] += pa_reject_num
            min_reject_num['pa'] = min(min_reject_num['pa'], pa_reject_num)
            max_reject_num['pa'] = max(max_reject_num['pa'], pa_reject_num)

            total_reject_num['st'] += st_reject_num
            min_reject_num['st'] = min(min_reject_num['st'], st_reject_num)
            max_reject_num['st'] = max(max_reject_num['st'], st_reject_num)

            best_rc_p_value += rc_p_value
            best_st_p_value += pa_p_value

        i = 'st'
        result_df.loc[const.BEST_STRATEGY_ST_P_VALUE, column_name] = best_st_p_value / test_time
        result_df.loc[const.BEST_STRATEGY_RC_P_VALUE, column_name] = best_rc_p_value / test_time
        result_df.loc[const.AVERAGE_REJECT_NUM, column_name] = float(total_reject_num[i]) / test_time
        result_df.loc[const.MAXIMUM_REJECT_NUM, column_name] = max_reject_num[i]
        result_df.loc[const.MINIMUM_REJECT_NUM, column_name] = min_reject_num[i]
        result_df.loc[const.AVERAGE_REJECT_PORTION, column_name] = float(total_reject_num[i]) / test_time / df.shape[1]

        # for i in ['rc', 'pa', 'st']:
        #     result_df.loc['{}_{}'.format(const.AVERAGE_REJECT_NUM, i), column_name] = float(
        #         total_reject_num[i]) / test_time
        #     result_df.loc['{}_{}'.format(const.MAXIMUM_REJECT_NUM, i), column_name] = max_reject_num[i]
        #     result_df.loc['{}_{}'.format(const.MINIMUM_REJECT_NUM, i), column_name] = min_reject_num[i]
        #     result_df.loc['{}_{}'.format(const.AVERAGE_REJECT_PORTION, i), column_name] = float(
        #         total_reject_num[i]) / test_time / df.shape[1]

    return result_df


if __name__ == '__main__':
    import pathos

    pool = pathos.multiprocessing.ProcessingPool(4)
    file_list = os.listdir(return_data_path)

    test_currency = '48'

    test_path = []
    for file_name in file_list:
        if test_currency in file_name:
            test_path.append(return_data_path, file_name)


    def process_df(file_path):
        return generate_table_3or4(file_path)


    result_dfs = pool.map(process_df, test_path)
    result_df = pd.concat(result_dfs, axis=1)
    result_df.to_pickle(os.path.join(temp_path, 'table3.p'))
