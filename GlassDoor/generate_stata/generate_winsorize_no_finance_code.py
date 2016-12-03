#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: generate_winsorize_no_finance_code
# @Date: 2016-12-03
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os

from constants import suffix_dict, dd_dep_vars, da_dep_vars, up_to_you, control_variables, independent_variables

root_path = '/home/wangzg/Documents/WangYouan/research/Glassdoor'

output_path = os.path.join(root_path, 'winsor5_result')

da_f = open('da_win_reg_no_finance.do', 'w')
da_f.write('use "/home/wangzg/Documents/WangYouan/research/Glassdoor/result/da_commun_dropna.dta"\n\n')
da_f.write('winsor2 {}, replace cuts(5 95)\n\n'.format(' '.join(independent_variables)))

dd_f = open('dd_win_reg_no_finance.do', 'w')
dd_f.write('use "/home/wangzg/Documents/WangYouan/research/Glassdoor/result/dd_commun_dropna.dta"\n\n')
dd_f.write('winsor2 {}, replace cuts(5 95)\n\n'.format(' '.join(independent_variables)))

for comment_num in [None, 1, 3, 5]:
    if comment_num is None:
        result_path = os.path.join(output_path, 'winsor5_no_finance')
        option = 'if sic2 > 68 | sic2 < 60'

    else:
        result_path = os.path.join(output_path, 'winsor5_no_finance_com{}'.format(comment_num))
        option = 'if allNum > {} & (sic2 > 68 | sic2 < 60)'.format(comment_num)

    result_path_dd = os.path.join(result_path, 'dd_reg_result')
    result_path_da = os.path.join(result_path, 'da_reg_result')

    if not os.path.isdir(result_path_da):
        os.makedirs(result_path_da)

    if not os.path.isdir(result_path_dd):
        os.makedirs(result_path_dd)

    path = result_path_dd
    f = dd_f
    for dep in dd_dep_vars:
        for suffix in suffix_dict:
            file_name = os.path.join(path, '{}_{}.xls'.format(dep, suffix))

            for ind in suffix_dict[suffix]:
                # ind
                f.write('// ind only\n')
                f.write('capture noisily qui regress {} {} {}\n'.format(dep, ind, option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(' addtext(Year Dummy, No, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control
                f.write('// ind + control\n')
                f.write(
                    'capture noisily qui regress {} {} {} {}\n'.format(dep, ind, ' '.join(control_variables), option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(' addtext(Year Dummy, No, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you
                f.write('// ind + control + up to you\n')
                f.write('capture noisily qui regress {} {} {} {} {}\n'.format(dep, ind, ' '.join(control_variables),
                                                                              ' '.join(up_to_you), option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(' addtext(Year Dummy, No, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + i.fyear
                f.write('// ind + control + i.fyear\n')
                f.write(
                    'capture noisily qui regress {} {} {} i.fyear {}\n'.format(dep, ind, ' '.join(control_variables),
                                                                               option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + i.sic2
                f.write('// ind + control + i.sic2\n')
                f.write('capture noisily qui regress {} {} {} i.sic2 {}\n'.format(dep, ind, ' '.join(control_variables),
                                                                                  option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(
                    ' addtext(Year Dummy, No, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + i.sic2 + i.fyear
                f.write('// ind + control + i.fyear + i.sic2\n')
                f.write(
                    'capture noisily qui regress {} {} {} i.sic2 i.fyear {}\n'.format(dep, ind,
                                                                                      ' '.join(control_variables),
                                                                                      option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you + i.fyear
                f.write('// ind + control + up to you + i.fyear\n')
                f.write(
                    'capture noisily qui regress {} {} {} {} i.fyear {}\n'.format(dep, ind, ' '.join(control_variables),
                                                                                  ' '.join(up_to_you), option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you + i.sic2
                f.write('// ind + control + up to you + i.sic2\n')
                f.write(
                    'capture noisily qui regress {} {} {} {} i.sic2 {}\n'.format(dep, ind, ' '.join(control_variables),
                                                                                 ' '.join(up_to_you), option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(
                    ' addtext(Year Dummy, No, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you + i.sic2 + i.fyear
                f.write('// ind + control + up to you + i.sic2 + i.fyear\n')
                f.write(
                    'capture noisily qui regress {} {} {} {} i.sic2 i.fyear {}\n'.format(dep, ind,
                                                                                         ' '.join(control_variables),
                                                                                         ' '.join(up_to_you),
                                                                                         option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + i.sic2 + i.fyear + vce
                f.write('// ind + control + i.sic2 + i.fyear, vce clu sic2\n')
                f.write(
                    'capture noisily qui regress {} {} {} i.sic2 i.fyear {}'.format(dep, ind,
                                                                                    ' '.join(control_variables),
                                                                                    option))
                f.write(', vce(cluster sic2)\n')
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, Industry)'.format(
                        dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you + i.sic2 + i.fyear + vce
                f.write('// ind + control + up to you + i.sic2 + i.fyear, vce clu sic2\n')
                f.write(
                    'capture noisily qui regress {} {} {} {} i.sic2 i.fyear {}'.format(dep, ind,
                                                                                       ' '.join(control_variables),
                                                                                       ' '.join(up_to_you), option))
                f.write(', vce(cluster sic2)\n')
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, Industry)'.format(
                        dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

    path = result_path_da
    f = da_f
    for dep in da_dep_vars:
        for suffix in suffix_dict:
            file_name = os.path.join(path, '{}_{}.xls'.format(dep, suffix))

            for ind in suffix_dict[suffix]:
                # ind
                f.write('// ind only\n')
                f.write('capture noisily qui regress {} {} {}\n'.format(dep, ind, option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(' addtext(Year Dummy, No, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control
                f.write('// ind + control\n')
                f.write(
                    'capture noisily qui regress {} {} {} {}\n'.format(dep, ind, ' '.join(control_variables), option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(' addtext(Year Dummy, No, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you
                f.write('// ind + control + up to you\n')
                f.write('capture noisily qui regress {} {} {} {} {}\n'.format(dep, ind, ' '.join(control_variables),
                                                                              ' '.join(up_to_you), option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(' addtext(Year Dummy, No, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + i.fyear
                f.write('// ind + control + i.fyear\n')
                f.write(
                    'capture noisily qui regress {} {} {} i.fyear {}\n'.format(dep, ind, ' '.join(control_variables),
                                                                               option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + i.sic2
                f.write('// ind + control + i.sic2\n')
                f.write('capture noisily qui regress {} {} {} i.sic2 {}\n'.format(dep, ind, ' '.join(control_variables),
                                                                                  option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(
                    ' addtext(Year Dummy, No, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + i.sic2 + i.fyear
                f.write('// ind + control + i.fyear + i.sic2\n')
                f.write(
                    'capture noisily qui regress {} {} {} i.sic2 i.fyear {}\n'.format(dep, ind,
                                                                                      ' '.join(control_variables),
                                                                                      option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you + i.fyear
                f.write('// ind + control + up to you + i.fyear\n')
                f.write(
                    'capture noisily qui regress {} {} {} {} i.fyear {}\n'.format(dep, ind, ' '.join(control_variables),
                                                                                  ' '.join(up_to_you), option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, No, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you + i.sic2
                f.write('// ind + control + up to you + i.sic2\n')
                f.write(
                    'capture noisily qui regress {} {} {} {} i.sic2 {}\n'.format(dep, ind, ' '.join(control_variables),
                                                                                 ' '.join(up_to_you), option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(
                    ' addtext(Year Dummy, No, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you + i.sic2 + i.fyear
                f.write('// ind + control + up to you + i.sic2 + i.fyear\n')
                f.write(
                    'capture noisily qui regress {} {} {} {} i.sic2 i.fyear {}\n'.format(dep, ind,
                                                                                         ' '.join(control_variables),
                                                                                         ' '.join(up_to_you),
                                                                                         option))
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, No)'.format(dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + i.sic2 + i.fyear + vce
                f.write('// ind + control + i.sic2 + i.fyear, vce clu sic2\n')
                f.write(
                    'capture noisily qui regress {} {} {} i.sic2 i.fyear {}'.format(dep, ind,
                                                                                    ' '.join(control_variables),
                                                                                    option))
                f.write(', vce(cluster sic2)\n')
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, Industry)'.format(
                        dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

                # ind + control + up to you + i.sic2 + i.fyear + vce
                f.write('// ind + control + up to you + i.sic2 + i.fyear, vce clu sic2\n')
                f.write(
                    'capture noisily qui regress {} {} {} {} i.sic2 i.fyear {}'.format(dep, ind,
                                                                                       ' '.join(control_variables),
                                                                                       ' '.join(up_to_you), option))
                f.write(', vce(cluster sic2)\n')
                f.write('outreg2 using {}, drop(i.sic2 i.fyear) '.format(file_name))
                f.write(
                    ' addtext(Year Dummy, Yes, Industry Dummy, Yes, Dependent Variable, {}, Cluster, Industry)'.format(
                        dep))
                f.write(' tstat bdec(2) tdec(2) rdec(2) nolabel append\n\n')

da_f.close()
dd_f.close()
