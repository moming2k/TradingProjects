#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: generate_test_per5
# Author: Mark Wang
# Date: 20/11/2016

import os
import datetime

dep_var = ['AcquirerCAR_TestPer5_F1', 'TargetCAR_TestPer5_F1', 'CombinedCAR_TestPer5_F1', 'AcquirerCAR_TestPer5_F3',
           'TargetCAR_TestPer5_F3', 'CombinedCAR_TestPer5_F3', 'AcquirerCAR_TestPer5_F4', 'TargetCAR_TestPer5_F4',
           'CombinedCAR_TestPer5_F4']

ind_var = ['all_dc', 'all_nc', 'all_nb', 'all_ec', 'all_dc_last_year', 'all_nc_last_year', 'all_nb_last_year',
           'all_ec_last_year', 'board_dc', 'board_nc', 'board_nb', 'board_ec', 'board_dc_last_year',
           'board_nc_last_year', 'board_nb_last_year', 'board_ec_last_year', 'ceochairman_dc', 'ceochairman_nc',
           'ceochairman_nb', 'ceochairman_ec', 'ceochairman_dc_last_year', 'ceochairman_nc_last_year',
           'ceochairman_nb_last_year', 'ceochairman_ec_last_year', 'ceo_dc', 'ceo_nc', 'ceo_nb', 'ceo_ec',
           'ceo_dc_last_year', 'ceo_nc_last_year', 'ceo_nb_last_year', 'ceo_ec_last_year', 'chairman_dc', 'chairman_nc',
           'chairman_nb', 'chairman_ec', 'chairman_dc_last_year', 'chairman_nc_last_year', 'chairman_nb_last_year',
           'chairman_ec_last_year']

dep_var_per2 = ['AcquirerCAR_TestPer2_F1', 'TargetCAR_TestPer2_F1', 'CombinedCAR_TestPer2_F1',
                'AcquirerCAR_TestPer2_F3', 'TargetCAR_TestPer2_F3', 'CombinedCAR_TestPer2_F3',
                'AcquirerCAR_TestPer2_F4', 'TargetCAR_TestPer2_F4', 'CombinedCAR_TestPer2_F4',
                'AcquirerCAR_TestPer2_F1_100', 'CombinedCAR_TestPer2_F1_100', 'TargetCAR_TestPer2_F1_100',
                'AcquirerCAR_TestPer2_F1_w1', 'AcquirerCAR_TestPer2_F1_w25', 'AcquirerCAR_TestPer2_F1_w5']

control_variables = ['AcquirerRunnp_200_11', 'AcquirerROA', 'AcquirerTobinQ', 'DealValueByAcqAssetCombined',
                     'Cash_deal_dummy', 'Stock_deal_dummy', 'Attitude_dummy', 'Target_public_dummy',
                     'PercentageAcquired', 'Acquirer_Total_Assets_mil_Combin']

lag = '''{} i.Year i.acquirerstate_num, vce(clu AcquirerCUSIP_num)\n'''.format(' '.join(control_variables))

today = datetime.date.today().strftime('%Y%m%d')
output_path = '/home/wangzg/Documents/WangYouan/research/BankCentrality/{}Per5Result'.format(today)
if not os.path.isdir(output_path):
    os.makedirs(output_path)

f = open('reg_per5.do', 'w')
f.write('use "/home/wangzg/Documents/WangYouan/research/BankCentrality/result/Car_Centrality_dropna.dta"\n\n')

for dep in dep_var:
    for ind in ind_var:
        outreg_text = 'outreg2 using {}/{}{}Per5.xls, drop(i.Year i.acquirerstate_num)'.format(output_path, today, ind)
        outreg_text = '{} addtext(Year Dummy, Yes, Acquirer State Dummy, Yes, Cluster, AcquirerCUSIP_num)'.format(
            outreg_text)
        outreg_text = '{} tstat bdec(2) tdec(2) rdec(3) nolabel append\n\n'.format(outreg_text)

        f.write('capture noisily qui regress {} {} {}'.format(dep, ind, lag))
        f.write(outreg_text)

f.close()
