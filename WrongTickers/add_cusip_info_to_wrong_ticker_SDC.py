#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: add_info_to_wrong_ticker_SDC
# Author: Mark Wang
# Date: 16/8/2016

from multiprocessing import Pool

from add_info_to_wrong_ticker import *

vol_df = pd.read_csv('Stock_data/Volume.csv', dtype={'CUSIP': str, 'date': str, 'TICKER': str},
                     usecols=['date', 'TICKER', 'CUSIP', 'VOL'])


# comp_df = pd.read_csv('Stock_data/Compustat.csv', dtype={'cusip': str, 'iid': str, 'datadate': str},
#                       usecols=['gvkey', 'iid', 'datadate', 'cusip', 'divd', 'cshoc', 'eps', 'trfd', 'exchg'])
# comp_df['cusip'] = comp_df['cusip'].apply(lambda x: x[:-1])


def get_cusip_from_ticker_date(ticker, today, yesterday, tomorrow):
    df = vol_df[vol_df['TICKER'] == ticker]
    if df.empty:
        return np.nan
    today = ''.join(today.split('-'))
    yesterday = ''.join(yesterday.split('-'))
    tomorrow = ''.join(tomorrow.split('-'))
    real_df = df[df['date'] == today]
    if real_df.empty:
        real_df = df[df['date'] == yesterday]

    if real_df.empty:
        real_df = df[df['date'] == tomorrow]

    if real_df.empty:
        real_df = df

    return real_df.ix[real_df.index[0], 'CUSIP']


def get_volume_from_volume_date(ticker, date):
    df = vol_df[vol_df['TICKER'] == ticker]
    date = ''.join(date.split('-'))
    df = df[df['date'] == date]
    if df.empty:
        return np.nan

    vol = df.ix[df.index[0], 'VOL']
    if not vol or np.isnan(vol):
        return np.nan
    else:
        return int(vol)


def get_prior_one_year_volume(date, cusip):
    df = vol_df[vol_df['CUSIP'] == cusip]
    df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y%m%d'))
    current_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    index = df[df['date'] == ''.join(date.split('-'))]
    if index.empty:
        return np.nan, np.nan
    index = index.index[0]
    df = df[df.index < index]
    df_vol = df.tail(252).VOL
    vol_list = []
    for vol in df_vol:
        if vol and not np.nan(vol):
            vol_list.append(int(vol))
    return sum(vol_list), np.std(vol_list)


def add_cusip(row):
    today = row['DateToday']
    tomorrow = row['DateTomorrow']
    yesterday = row['DateYesterday']
    wrong_ticker = row['WrongTicker']
    real_ticker = row['Ticker']

    result = {'cusip': get_cusip_from_ticker_date(real_ticker, today, tomorrow, yesterday),
              'cusip_wrong': get_cusip_from_ticker_date(wrong_ticker, today, tomorrow, yesterday),
              'Volume_real': get_volume_from_volume_date(real_ticker, today),
              'VolumeTomorrow_real': get_volume_from_volume_date(real_ticker, tomorrow),
              'VolumeYesterday_real': get_volume_from_volume_date(real_ticker, yesterday),
              }

    # info_to_add = ['Price', 'LogReturn', 'SimpleReturn', 'PriceHigh', 'PriceLow']
    # for info in info_to_add:
    #     for required_time in ['Today', 'Tomorrow', 'Yesterday']:
    #         if required_time == 'Today':
    #             column_name = info
    #         else:
    #             column_name = "{}{}".format(info, required_time)
    #
    #         column_name = '{}_real'.format(column_name)
    #
    #         result[column_name] = get_wrong_ticker_information_from_saved_file(row, info, required_time)
    # try:
    #     result['PriceRange_real'] = result['PriceHigh_real'] - result['PriceLow_real']
    # finally:
    #     result['PriceRange_real'] = np.nan
    # try:
    #     result['PriceRangeTomorrow_real'] = result['PriceHighTomorrow_real'] - result['PriceLowTomorrow_real']
    # finally:
    #     result['PriceRangeTomorrow_real'] = np.nan
    # try:
    #     result['PriceRangeYesterday_real'] = result['PriceHighYesterday_real'] - result['PriceLowYesterday_real']
    # finally:
    #     result['PriceRangeYesterday_real'] = np.nan
    #
    # result.update(get_comp_df_info(result['cusip'], today, date_type='Today', data_type='real'))
    # result.update(get_comp_df_info(result['cusip'], yesterday, date_type='Yesterday', data_type='real'))
    # result.update(get_comp_df_info(result['cusip'], tomorrow, date_type='Tomorrow', data_type='real'))
    #
    # result.update(get_comp_df_info(result['cusip_wrong'], today, date_type='Today', data_type='wrong'))
    # result.update(get_comp_df_info(result['cusip_wrong'], yesterday, date_type='Yesterday', data_type='wrong'))
    # result.update(get_comp_df_info(result['cusip_wrong'], tomorrow, date_type='Tomorrow', data_type='wrong'))
    #
    # vol = get_prior_one_year_volume(today, result['cusip'])
    # vol_wrong = get_prior_one_year_volume(today, result['cusip_wrong'])
    # result['PriorVolSum_real'] = vol[0]
    # result['PriorVolStd_real'] = vol[1]
    # result['PriorVolSum_wrong'] = vol_wrong[1]
    # result['PriorVolStd_wrong'] = vol_wrong[1]
    return pd.Series(result)


def process_df(data_df):
    return pd.concat([data_df, data_df.apply(add_cusip, axis=1)], axis=1)


if __name__ == '__main__':
    process_num = 10
    pool = Pool(processes=process_num)

    print "Read SDC file from path"
    sdc_df = pd.read_csv('result_csv/wrong_tickers_from_SDC_target_name.csv', index_col=0)

    print "Split file"
    split_df = np.array_split(sdc_df, process_num)
    result_dfs = pool.map(process_df, split_df)
    sdc_df = pd.concat(result_dfs, axis=0)
    # bloomberg_df = process_bloomberg_df(bloomberg_df)
    sdc_df.to_csv('result_csv/wrong_tickers_from_SDC_target_name.csv', encoding='utf8')
