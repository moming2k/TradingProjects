#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: generate_da_commun_file
# Author: Mark Wang
# Date: 19/11/2016

import datetime

ind_vars = ['prosComNum1k', 'advComNum1k', 'allComNum1k', 'consComNum1k']

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

today = datetime.date.today().strftime('%Y%m%d')
dd_output_path = '/home/wangzg/Documents/WangYouan/research/Glassdoor/dd_sep_ind_dep_result'
da_output_path = '/home/wangzg/Documents/WangYouan/research/Glassdoor/da_sep_ind_dep_result'

f = open('dd_reg.do', 'w')
f.write('use "/home/wangzg/Documents/WangYouan/research/Glassdoor/result/dd_commun_dropna.dta"\n\n')

output_path = dd_output_path
for dep in dd_dep_vars:
    f.write('// To generate dep: {}\n'.format(dep))
    for ind in ind_vars:
        f.write('// current ind is {}\n\n'.format(ind))

        file_name = '{}_{}_{}_Result.xls'.format(today, dep, ind)

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
        f.write(' addtext(Year Dummy, Yes, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
        f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

        # ind + control + i.sic2
        f.write('// ind + control + i.sic2\n')
        f.write('capture noisily qui regress {} {} {} i.sic2\n'.format(dep, ind, ' '.join(control_variables)))
        f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
        f.write(' addtext(Year Dummy, No, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
        f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

        # ind + control + i.sic2 + i.fyear
        f.write('// ind + control + i.fyear + i.sic2\n')
        f.write('capture noisily qui regress {} {} {} i.sic2 i.fyear\n'.format(dep, ind, ' '.join(control_variables)))
        f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
        f.write(' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
        f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

        # ind + control + up to you + i.fyear
        f.write('// ind + control + up to you + i.fyear\n')
        f.write('capture noisily qui regress {} {} {} {} i.fyear\n'.format(dep, ind, ' '.join(control_variables),
                                                                           ' '.join(up_to_you)))
        f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
        f.write(' addtext(Year Dummy, Yes, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
        f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

        # ind + control + up to you + i.sic2
        f.write('// ind + control + up to you + i.sic2\n')
        f.write('capture noisily qui regress {} {} {} {} i.sic2\n'.format(dep, ind, ' '.join(control_variables),
                                                                          ' '.join(up_to_you)))
        f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
        f.write(' addtext(Year Dummy, No, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
        f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

        # ind + control + up to you + i.sic2 + i.fyear
        f.write('// ind + control + up to you + i.sic2 + i.fyear\n')
        f.write('capture noisily qui regress {} {} {} {} i.sic2 i.fyear\n'.format(dep, ind, ' '.join(control_variables),
                                                                                  ' '.join(up_to_you)))
        f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
        f.write(' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
        f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

        # ind + control + i.sic2 + i.fyear + vce
        f.write('// ind + control + i.sic2 + i.fyear, vce clu sic2\n')
        f.write('capture noisily qui regress {} {} {} i.sic2 i.fyear'.format(dep, ind, ' '.join(control_variables)))
        f.write(', vce(cluster sic2)\n')
        f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
        f.write(' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, Industry)'.format(dep))
        f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

        # ind + control + up to you + i.sic2 + i.fyear + vce
        f.write('// ind + control + up to you + i.sic2 + i.fyear, vce clu sic2\n')
        f.write('capture noisily qui regress {} {} {} {} i.sic2 i.fyear'.format(dep, ind, ' '.join(control_variables),
                                                                                ' '.join(up_to_you)))
        f.write(', vce(cluster sic2)\n')
        f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
        f.write(' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, Industry)'.format(dep))
        f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

    f.write('\n')

f.close()

f = open('da_reg.do', 'w')

f.write('use "/home/wangzg/Documents/WangYouan/research/Glassdoor/result/da_commun_dropna.dta"\n\n')
output_path = da_output_path
for dep in da_dep_vars:
    f.write('// To generate dep: {}\n'.format(dep))
    for ind in ind_vars:
        f.write('// current ind is {}\n\n'.format(ind))

        file_name = '{}_{}_{}_Result.xls'.format(today, dep, ind)

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
        f.write(' addtext(Year Dummy, Yes, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
        f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

        # ind + control + i.sic2
        f.write('// ind + control + i.sic2\n')
        f.write('capture noisily qui regress {} {} {} i.sic2\n'.format(dep, ind, ' '.join(control_variables)))
        f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
        f.write(' addtext(Year Dummy, No, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
        f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

        # ind + control + i.sic2 + i.fyear
        f.write('// ind + control + i.fyear + i.sic2\n')
        f.write('capture noisily qui regress {} {} {} i.sic2 i.fyear\n'.format(dep, ind, ' '.join(control_variables)))
        f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
        f.write(' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
        f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

        # ind + control + up to you + i.fyear
        f.write('// ind + control + up to you + i.fyear\n')
        f.write('capture noisily qui regress {} {} {} {} i.fyear\n'.format(dep, ind, ' '.join(control_variables),
                                                                           ' '.join(up_to_you)))
        f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
        f.write(' addtext(Year Dummy, Yes, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
        f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

        # ind + control + up to you + i.sic2
        f.write('// ind + control + up to you + i.sic2\n')
        f.write('capture noisily qui regress {} {} {} {} i.sic2\n'.format(dep, ind, ' '.join(control_variables),
                                                                          ' '.join(up_to_you)))
        f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
        f.write(' addtext(Year Dummy, No, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
        f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

        # ind + control + up to you + i.sic2 + i.fyear
        f.write('// ind + control + up to you + i.sic2 + i.fyear\n')
        f.write('capture noisily qui regress {} {} {} {} i.sic2 i.fyear\n'.format(dep, ind, ' '.join(control_variables),
                                                                                  ' '.join(up_to_you)))
        f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
        f.write(' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
        f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

        # ind + control + i.sic2 + i.fyear + vce
        f.write('// ind + control + i.sic2 + i.fyear, vce clu sic2\n')
        f.write('capture noisily qui regress {} {} {} i.sic2 i.fyear'.format(dep, ind, ' '.join(control_variables)))
        f.write(', vce(cluster sic2)\n')
        f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
        f.write(' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, Industry)'.format(dep))
        f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

        # ind + control + up to you + i.sic2 + i.fyear + vce
        f.write('// ind + control + up to you + i.sic2 + i.fyear, vce clu sic2\n')
        f.write('capture noisily qui regress {} {} {} {} i.sic2 i.fyear'.format(dep, ind, ' '.join(control_variables),
                                                                                ' '.join(up_to_you)))
        f.write(', vce(cluster sic2)\n')
        f.write('outreg2 using {}/{}, drop(i.sic2 i.fyear) '.format(output_path, file_name))
        f.write(' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, Industry)'.format(dep))
        f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

    f.write('\n')
f.close()
