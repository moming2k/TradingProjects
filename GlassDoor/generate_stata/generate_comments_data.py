#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: generate_comments_data
# @Date: 2016-11-29
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

today = datetime.datetime.today().strftime('%Y%m%d')

root_path = '/home/wangzg/Documents/WangYouan/research/Glassdoor'
data_path = os.path.join(root_path, 'result')
result_path = os.path.join(root_path, 'year_constrain_data')

if not os.path.isdir(result_path):
    os.makedirs(result_path)

da_file = os.path.join(data_path, 'da_commun_dropna.dta')
dd_file = os.path.join(data_path, 'dd_commun_dropna.dta')

ind_var_list = [['prosComNum1k', 'advComNum1k', 'allComNum1k', 'consComNum1k'],
                ['consPM_consNCom_avgAll1k', 'allPM_allNCom_avgAll1k', 'prosPM_prosNCom_avgAll1k',
                 'advPM_advNCom_avgAll1k'],
                ['consP_consNCom_avgAll1k', 'allP_allNCom_avgAll1k', 'prosP_prosNCom_avgAll1k',
                 'advP_advNCom_avgAll1k'],
                ['consPM_consNSt_sum1k', 'prosPM_prosNSt_sum1k', 'advPM_advNSt_sum1k', 'allPM_allNSt_sum1k'],
                ['consP_consNSt_sum1k', 'prosP_prosNSt_sum1k', 'advP_advNSt_sum1k', 'allP_allNSt_sum1k'],
                ['advP_advComNSt_avgAll1k', 'consP_consComNSt_avgAll1k', 'prosP_prosComNSt_avgAll1k',
                 'allP_allComNSt_avgAll1k'], ['consP_simple1k', 'prosP_simple1k', 'advP_simple1k', 'allP_simple1k'],
                ['consPM_simple1k', 'prosPM_simple1k', 'advPM_simple1k', 'allPM_simple1k'],
                ['allNum1k', 'advNum1k', 'consNum1k', 'prosNum1k'],
                ['prosP_prosNCh_avgCom1k', 'consP_consNCh_avgCom1k', 'allP_allNCh_avgCom1k', 'advP_advNCh_avgCom1k'],
                ['prosPM_prosNCh_avgCom1k', 'consPM_consNCh_avgCom1k', 'allPM_allNCh_avgCom1k',
                 'advPM_advNCh_avgCom1k'],
                ['advPM_advComNCom_avgAll1k', 'consPM_consComNCom_avgAll1k', 'prosPM_prosComNCom_avgAll1k',
                 'allPM_allComNCom_avgAll1k'],
                ['advPM_advComNSt_avgAll1k', 'consPM_consComNSt_avgAll1k', 'prosPM_prosComNSt_avgAll1k',
                 'allPM_allComNSt_avgAll1k'],
                ['advP_advNCom_avgAll1k', 'consP_consNCom_avgAll1k', 'prosP_prosNCom_avgAll1k',
                 'allP_allNCom_avgAll1k'],
                ['advPM_advNCom_avgAll1k', 'consPM_consNCom_avgAll1k', 'prosPM_prosNCom_avgAll1k',
                 'allPM_allNCom_avgAll1k'],
                ['advPM_advComNSt_avgAll1k', 'consPM_consComNSt_avgAll1k', 'prosPM_prosComNSt_avgAll1k',
                 'allPM_allComNSt_avgAll1k'],
                ['advP_advComNCom_avgAll1k', 'consP_consComNCom_avgAll1k', 'prosP_prosComNCom_avgAll1k',
                 'allP_allComNCom_avgAll1k'],
                ]

ind_var_name = ['ComNum1k', 'PM_NCom_avgAll1k', 'P_NCom_avgAll1k', 'PM_NSt_sum1k', 'P_NSt_sum1k',
                'P_ComNSt_avgAll1k', 'P_simple1k', 'PM_simple1k', 'Num1k', 'P_NCh_avgCom1k', 'PM_NCh_avgCom1k',
                'PM_ComNCom_avgAll1k', 'PM_ComNSt_avgAll1k', 'P_NCom_avgAll1k', 'PM_NCom_avgAll1k',
                'PM_ComNSt_avgAll1k', 'P_ComNCom_avgAll1k']

dep_vars = ['da', 'da_cfo', 'da_btm', 'absda', 'absda_cfo', 'absda_btm', 'da_win', 'da_win_cfo', 'da_win_btm',
            'absda_win', 'absda_win_cfo', 'absda_win_btm', 'da_ff48', 'da_ff48_cfo', 'da_ff48_btm', 'absda_ff48',
            'absda_ff48_cfo', 'absda_ff48_btm', 'da_ff48_win', 'da_ff48_win_cfo', 'da_ff48_win_btm', 'absda_ff48_win',
            'absda_ff48_win_cfo', 'absda_ff48_win_btm', 'resid', 'resid_loss', 'resid_loss_spi', 'resid_cfo',
            'absresid', 'absresid_loss', 'absresid_loss_spi', 'absresid_cfo', 'resid_std', 'resid_loss_std',
            'resid_lossspi_std', 'resid_cfo_std', 'resid_stddec', 'resid_loss_stddec', 'resid_lossspi_stddec',
            'resid_cfo_stddec', 'resid_win', 'resid_win_loss', 'resid_win_loss_spi', 'resid_win_cfo', 'absresid_win',
            'absresid_win_loss', 'absresid_win_loss_spi', 'absresid_win_cfo', 'resid_win_std', 'resid_win_loss_std',
            'resid_win_lossspi_std', 'resid_win_cfo_std', 'resid_win_stddec', 'resid_win_loss_stddec',
            'resid_win_lossspi_stddec', 'resid_win_cfo_stddec']

dd_dep_vars = ['resid', 'resid_loss', 'resid_loss_spi', 'resid_cfo', 'absresid', 'absresid_loss', 'absresid_loss_spi',
               'absresid_cfo', 'resid_std', 'resid_loss_std', 'resid_lossspi_std', 'resid_cfo_std', 'resid_stddec',
               'resid_loss_stddec', 'resid_lossspi_stddec', 'resid_cfo_stddec', 'resid_win', 'resid_win_loss',
               'resid_win_loss_spi', 'resid_win_cfo', 'absresid_win', 'absresid_win_loss', 'absresid_win_loss_spi',
               'absresid_win_cfo', 'resid_win_std', 'resid_win_loss_std', 'resid_win_lossspi_std', 'resid_win_cfo_std',
               'resid_win_stddec', 'resid_win_loss_stddec', 'resid_win_lossspi_stddec', 'resid_win_cfo_stddec']

da_dep_vars = ['da', 'da_cfo', 'da_btm', 'absda', 'absda_cfo', 'absda_btm', 'DA_win', 'absda_win', 'DA_win_cfo',
               'absda_win_cfo', 'DA_win_btm', 'absda_win_btm', 'DA_ff48', 'DA_ff48_cfo', 'DA_ff48_btm', 'absda_ff48',
               'absda_ff48_cfo', 'absda_ff48_btm', 'DA_ff48_win', 'absda_ff48_win', 'DA_ff48_win_cfo',
               'absda_ff48_win_cfo', 'DA_ff48_win_btm', 'absda_ff48_win_btm']

control_variables = ['oancf2at_std', 'sale2at_std', 'lnassets', 'loss_avg', 'sgrowth_chg', 'abvwret',
                     'litigation', 'foreign']
up_to_you = ['roa', 'cfo', 'accrual ', 'wc_chg', 'bleverage', 'sgrowth', 'no_intangible', 'cap_intensity',
             'restructure', 'age', 'btm', 'sale_chg', 'ibc_increase']

dd_f = open('dd_reg_different_comments_num.do', 'w')
dd_f.write('use "/home/wangzg/Documents/WangYouan/research/Glassdoor/result/dd_commun_dropna.dta"\n\n')
da_f = open('da_reg_different_comments_num.do', 'w')
da_f.write('use "/home/wangzg/Documents/WangYouan/research/Glassdoor/result/da_commun_dropna.dta"\n\n')

for comments_num in [1, 3, 5, 10]:
    option = 'if allNum > {}'.format(comments_num)

    save_path = os.path.join(result_path, 'comments_{}'.format(comments_num))
    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    for i in range(len(ind_var_list)):
        ind_vars = ind_var_list[i]
        output = ind_var_name[i]

        output_path = os.path.join(save_path, 'dd_{}'.format(output))
        if not os.path.isdir(output_path):
            os.makedirs(output_path)
        f = dd_f
        for dep in dd_dep_vars:
            f.write('// To generate dep: {}\n'.format(dep))
            for ind in ind_vars:
                f.write('// current ind is {}\n\n'.format(ind))

                file_name = '{}_{}Result.xls'.format(today, dep)

                # ind
                f.write('// ind only\n')
                f.write('capture noisily qui regress {} {} {}\n'.format(dep, ind, option))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(' addtext(Year Dummy, No, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control
                f.write('// ind + control\n')
                f.write('capture noisily qui regress {} {} {} {}\n'.format(dep, ind, ' '.join(control_variables),
                                                                           option))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(' addtext(Year Dummy, No, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you
                f.write('// ind + control + up to you\n')
                f.write('capture noisily qui regress {} {} {} {} {}\n'.format(dep, ind, ' '.join(control_variables),
                                                                              ' '.join(up_to_you),
                                                                              option))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(' addtext(Year Dummy, No, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + i.fyear
                f.write('// ind + control + i.fyear\n')
                f.write('capture noisily qui regress {} {} {} i.fyear {}\n'.format(dep, ind,
                                                                                   ' '.join(control_variables),
                                                                                   option))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + i.sic2
                f.write('// ind + control + i.sic2\n')
                f.write('capture noisily qui regress {} {} {} i.sic2\n'.format(dep, ind, ' '.join(control_variables)))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(
                    ' addtext(Year Dummy, No, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + i.sic2 + i.fyear
                f.write('// ind + control + i.fyear + i.sic2\n')
                f.write('capture noisily qui regress {} {} {} i.sic2 i.fyear\n'.format(dep, ind,
                                                                                       ' '.join(control_variables)))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you + i.fyear
                f.write('// ind + control + up to you + i.fyear\n')
                f.write(
                    'capture noisily qui regress {} {} {} {} i.fyear\n'.format(dep, ind, ' '.join(control_variables),
                                                                               ' '.join(up_to_you)))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you + i.sic2
                f.write('// ind + control + up to you + i.sic2\n')
                f.write('capture noisily qui regress {} {} {} {} i.sic2\n'.format(dep, ind, ' '.join(control_variables),
                                                                                  ' '.join(up_to_you)))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(
                    ' addtext(Year Dummy, No, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you + i.sic2 + i.fyear
                f.write('// ind + control + up to you + i.sic2 + i.fyear\n')
                f.write('capture noisily qui regress {} {} {} {} i.sic2 i.fyear\n'.format(dep, ind,
                                                                                          ' '.join(control_variables),
                                                                                          ' '.join(up_to_you)))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + i.sic2 + i.fyear + vce
                f.write('// ind + control + i.sic2 + i.fyear, vce clu sic2\n')
                f.write(
                    'capture noisily qui regress {} {} {} i.sic2 i.fyear'.format(dep, ind, ' '.join(control_variables)))
                f.write(', vce(cluster sic2)\n')
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, Industry)'.format(
                        dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you + i.sic2 + i.fyear + vce
                f.write('// ind + control + up to you + i.sic2 + i.fyear, vce clu sic2\n')
                f.write('capture noisily qui regress {} {} {} {} i.sic2 i.fyear'.format(dep, ind,
                                                                                        ' '.join(control_variables),
                                                                                        ' '.join(up_to_you)))
                f.write(', vce(cluster sic2)\n')
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, Industry)'.format(
                        dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

            f.write('\n')

        output_path = os.path.join(save_path, 'da_{}'.format(output))
        if not os.path.isdir(output_path):
            os.makedirs(output_path)

        f = da_f
        for dep in da_dep_vars:
            f.write('// To generate dep: {}\n'.format(dep))
            for ind in ind_vars:
                f.write('// current ind is {}\n\n'.format(ind))

                file_name = '{}_{}Result.xls'.format(today, dep)

                # ind
                f.write('// ind only\n')
                f.write('capture noisily qui regress {} {}\n'.format(dep, ind))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(' addtext(Year Dummy, No, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control
                f.write('// ind + control\n')
                f.write('capture noisily qui regress {} {} {}\n'.format(dep, ind, ' '.join(control_variables)))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(' addtext(Year Dummy, No, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you
                f.write('// ind + control + up to you\n')
                f.write('capture noisily qui regress {} {} {} {}\n'.format(dep, ind, ' '.join(control_variables),
                                                                           ' '.join(up_to_you)))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(' addtext(Year Dummy, No, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + i.fyear
                f.write('// ind + control + i.fyear\n')
                f.write('capture noisily qui regress {} {} {} i.fyear\n'.format(dep, ind, ' '.join(control_variables)))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + i.sic2
                f.write('// ind + control + i.sic2\n')
                f.write('capture noisily qui regress {} {} {} i.sic2\n'.format(dep, ind, ' '.join(control_variables)))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(
                    ' addtext(Year Dummy, No, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + i.sic2 + i.fyear
                f.write('// ind + control + i.fyear + i.sic2\n')
                f.write('capture noisily qui regress {} {} {} i.sic2 i.fyear\n'.format(dep, ind,
                                                                                       ' '.join(control_variables)))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you + i.fyear
                f.write('// ind + control + up to you + i.fyear\n')
                f.write(
                    'capture noisily qui regress {} {} {} {} i.fyear\n'.format(dep, ind, ' '.join(control_variables),
                                                                               ' '.join(up_to_you)))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you + i.sic2
                f.write('// ind + control + up to you + i.sic2\n')
                f.write('capture noisily qui regress {} {} {} {} i.sic2\n'.format(dep, ind, ' '.join(control_variables),
                                                                                  ' '.join(up_to_you)))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(
                    ' addtext(Year Dummy, No, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you + i.sic2 + i.fyear
                f.write('// ind + control + up to you + i.sic2 + i.fyear\n')
                f.write('capture noisily qui regress {} {} {} {} i.sic2 i.fyear\n'.format(dep, ind,
                                                                                          ' '.join(control_variables),
                                                                                          ' '.join(up_to_you)))
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + i.sic2 + i.fyear + vce
                f.write('// ind + control + i.sic2 + i.fyear, vce clu sic2\n')
                f.write(
                    'capture noisily qui regress {} {} {} i.sic2 i.fyear'.format(dep, ind, ' '.join(control_variables)))
                f.write(', vce(cluster sic2)\n')
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, Industry)'.format(
                        dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you + i.sic2 + i.fyear + vce
                f.write('// ind + control + up to you + i.sic2 + i.fyear, vce clu sic2\n')
                f.write('capture noisily qui regress {} {} {} {} i.sic2 i.fyear'.format(dep, ind,
                                                                                        ' '.join(control_variables),
                                                                                        ' '.join(up_to_you)))
                f.write(', vce(cluster sic2)\n')
                f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, Industry)'.format(
                        dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

            f.write('\n')

dd_f.close()
da_f.close()
