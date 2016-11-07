#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: generate_regress_file
# Author: Mark Wang
# Date: 7/11/2016

import datetime

control_variables = ['oancf_std2oancf', 'sale_std2sale', 'lnassets', 'litigation', 'foreign', 'loss_avg',
                     'no_intangible', 'cap_intensity', 'cash_flow', 'restructure', 'age', 'btm']

up_to_you = ['pe_ratio', 'bleverage', 'accrual_lag', 'sgrowth', 'roa']

ind_vars = ['prosNum', 'consNum', 'allNum', 'prosComNum', 'prosP_simple', 'prosP_prosComNCh_sum',
            'prosP_prosComNCh_avgAll', 'prosP_prosComNCh_avgCom', 'prosP_prosComNCom_sum', 'prosP_prosComNCom_avgAll',
            'prosP_prosComNCom_avgCom', 'prosP_prosComNSt_sum', 'prosP_prosComNSt_avgAll', 'prosP_prosComNSt_avgCom',
            'prosP_prosComNWd_sum', 'prosP_prosComNWd_avgAll', 'prosP_prosComNWd_avgCom', 'prosP_prosNCh_sum',
            'prosP_prosNCh_avgAll', 'prosP_prosNCh_avgCom', 'prosP_prosNCom_sum', 'prosP_prosNCom_avgAll',
            'prosP_prosNCom_avgCom', 'prosP_prosNSt_sum', 'prosP_prosNSt_avgAll', 'prosP_prosNSt_avgCom',
            'prosP_prosNWd_sum', 'prosP_prosNWd_avgAll', 'prosP_prosNWd_avgCom', 'prosPM_simple',
            'prosPM_prosComNCh_sum', 'prosPM_prosComNCh_avgAll', 'prosPM_prosComNCh_avgCom', 'prosPM_prosComNCom_sum',
            'prosPM_prosComNCom_avgAll', 'prosPM_prosComNCom_avgCom', 'prosPM_prosComNSt_sum',
            'prosPM_prosComNSt_avgAll', 'prosPM_prosComNSt_avgCom', 'prosPM_prosComNWd_sum', 'prosPM_prosComNWd_avgAll',
            'prosPM_prosComNWd_avgCom', 'prosPM_prosNCh_sum', 'prosPM_prosNCh_avgAll', 'prosPM_prosNCh_avgCom',
            'prosPM_prosNCom_sum', 'prosPM_prosNCom_avgAll', 'prosPM_prosNCom_avgCom', 'prosPM_prosNSt_sum',
            'prosPM_prosNSt_avgAll', 'prosPM_prosNSt_avgCom', 'prosPM_prosNWd_sum', 'prosPM_prosNWd_avgAll',
            'prosPM_prosNWd_avgCom', 'consComNum', 'consP_simple', 'consP_consComNCh_sum', 'consP_consComNCh_avgAll',
            'consP_consComNCh_avgCom', 'consP_consComNCom_sum', 'consP_consComNCom_avgAll', 'consP_consComNCom_avgCom',
            'consP_consComNSt_sum', 'consP_consComNSt_avgAll', 'consP_consComNSt_avgCom', 'consP_consComNWd_sum',
            'consP_consComNWd_avgAll', 'consP_consComNWd_avgCom', 'consP_consNCh_sum', 'consP_consNCh_avgAll',
            'consP_consNCh_avgCom', 'consP_consNCom_sum', 'consP_consNCom_avgAll', 'consP_consNCom_avgCom',
            'consP_consNSt_sum', 'consP_consNSt_avgAll', 'consP_consNSt_avgCom', 'consP_consNWd_sum',
            'consP_consNWd_avgAll', 'consP_consNWd_avgCom', 'consPM_simple', 'consPM_consComNCh_sum',
            'consPM_consComNCh_avgAll', 'consPM_consComNCh_avgCom', 'consPM_consComNCom_sum',
            'consPM_consComNCom_avgAll', 'consPM_consComNCom_avgCom', 'consPM_consComNSt_sum',
            'consPM_consComNSt_avgAll', 'consPM_consComNSt_avgCom', 'consPM_consComNWd_sum', 'consPM_consComNWd_avgAll',
            'consPM_consComNWd_avgCom', 'consPM_consNCh_sum', 'consPM_consNCh_avgAll', 'consPM_consNCh_avgCom',
            'consPM_consNCom_sum', 'consPM_consNCom_avgAll', 'consPM_consNCom_avgCom', 'consPM_consNSt_sum',
            'consPM_consNSt_avgAll', 'consPM_consNSt_avgCom', 'consPM_consNWd_sum', 'consPM_consNWd_avgAll',
            'consPM_consNWd_avgCom', 'advNum', 'advComNum', 'advP_simple', 'advP_advComNCh_sum',
            'advP_advComNCh_avgAll',
            'advP_advComNCh_avgCom', 'advP_advComNCom_sum', 'advP_advComNCom_avgAll', 'advP_advComNCom_avgCom',
            'advP_advComNSt_sum', 'advP_advComNSt_avgAll', 'advP_advComNSt_avgCom', 'advP_advComNWd_sum',
            'advP_advComNWd_avgAll', 'advP_advComNWd_avgCom', 'advP_advNCh_sum', 'advP_advNCh_avgAll',
            'advP_advNCh_avgCom', 'advP_advNCom_sum', 'advP_advNCom_avgAll', 'advP_advNCom_avgCom', 'advP_advNSt_sum',
            'advP_advNSt_avgAll', 'advP_advNSt_avgCom', 'advP_advNWd_sum', 'advP_advNWd_avgAll', 'advP_advNWd_avgCom',
            'advPM_simple', 'advPM_advComNCh_sum', 'advPM_advComNCh_avgAll', 'advPM_advComNCh_avgCom',
            'advPM_advComNCom_sum', 'advPM_advComNCom_avgAll', 'advPM_advComNCom_avgCom', 'advPM_advComNSt_sum',
            'advPM_advComNSt_avgAll', 'advPM_advComNSt_avgCom', 'advPM_advComNWd_sum', 'advPM_advComNWd_avgAll',
            'advPM_advComNWd_avgCom', 'advPM_advNCh_sum', 'advPM_advNCh_avgAll', 'advPM_advNCh_avgCom',
            'advPM_advNCom_sum', 'advPM_advNCom_avgAll', 'advPM_advNCom_avgCom', 'advPM_advNSt_sum',
            'advPM_advNSt_avgAll', 'advPM_advNSt_avgCom', 'advPM_advNWd_sum', 'advPM_advNWd_avgAll',
            'advPM_advNWd_avgCom', 'allComNum', 'allP_simple', 'allP_allComNCh_sum', 'allP_allComNCh_avgAll',
            'allP_allComNCh_avgCom', 'allP_allComNCom_sum', 'allP_allComNCom_avgAll', 'allP_allComNCom_avgCom',
            'allP_allComNSt_sum', 'allP_allComNSt_avgAll', 'allP_allComNSt_avgCom', 'allP_allComNWd_sum',
            'allP_allComNWd_avgAll', 'allP_allComNWd_avgCom', 'allP_allNCh_sum', 'allP_allNCh_avgAll',
            'allP_allNCh_avgCom', 'allP_allNCom_sum', 'allP_allNCom_avgAll', 'allP_allNCom_avgCom', 'allP_allNSt_sum',
            'allP_allNSt_avgAll', 'allP_allNSt_avgCom', 'allP_allNWd_sum', 'allP_allNWd_avgAll', 'allP_allNWd_avgCom',
            'allPM_simple', 'allPM_allComNCh_sum', 'allPM_allComNCh_avgAll', 'allPM_allComNCh_avgCom',
            'allPM_allComNCom_sum', 'allPM_allComNCom_avgAll', 'allPM_allComNCom_avgCom', 'allPM_allComNSt_sum',
            'allPM_allComNSt_avgAll', 'allPM_allComNSt_avgCom', 'allPM_allComNWd_sum', 'allPM_allComNWd_avgAll',
            'allPM_allComNWd_avgCom', 'allPM_allNCh_sum', 'allPM_allNCh_avgAll', 'allPM_allNCh_avgCom',
            'allPM_allNCom_sum', 'allPM_allNCom_avgAll', 'allPM_allNCom_avgCom', 'allPM_allNSt_sum',
            'allPM_allNSt_avgAll', 'allPM_allNSt_avgCom', 'allPM_allNWd_sum', 'allPM_allNWd_avgAll',
            'allPM_allNWd_avgCom', 'ProsConsP_simple', 'ProsConsP_allComNCh_sum', 'ProsConsP_allComNCh_avgAll',
            'ProsConsP_allComNCh_avgCom', 'ProsConsP_allComNCom_sum', 'ProsConsP_allComNCom_avgAll',
            'ProsConsP_allComNCom_avgCom', 'ProsConsP_allComNSt_sum', 'ProsConsP_allComNSt_avgAll',
            'ProsConsP_allComNSt_avgCom', 'ProsConsP_allComNWd_sum', 'ProsConsP_allComNWd_avgAll',
            'ProsConsP_allComNWd_avgCom', 'ProsConsP_allNCh_sum', 'ProsConsP_allNCh_avgAll', 'ProsConsP_allNCh_avgCom',
            'ProsConsP_allNCom_sum', 'ProsConsP_allNCom_avgAll', 'ProsConsP_allNCom_avgCom', 'ProsConsP_allNSt_sum',
            'ProsConsP_allNSt_avgAll', 'ProsConsP_allNSt_avgCom', 'ProsConsP_allNWd_sum', 'ProsConsP_allNWd_avgAll',
            'ProsConsP_allNWd_avgCom', 'ProsConsPM_simple', 'ProsConsPM_allComNCh_sum', 'ProsConsPM_allComNCh_avgAll',
            'ProsConsPM_allComNCh_avgCom', 'ProsConsPM_allComNCom_sum', 'ProsConsPM_allComNCom_avgAll',
            'ProsConsPM_allComNCom_avgCom', 'ProsConsPM_allComNSt_sum', 'ProsConsPM_allComNSt_avgAll',
            'ProsConsPM_allComNSt_avgCom', 'ProsConsPM_allComNWd_sum', 'ProsConsPM_allComNWd_avgAll',
            'ProsConsPM_allComNWd_avgCom', 'ProsConsPM_allNCh_sum', 'ProsConsPM_allNCh_avgAll',
            'ProsConsPM_allNCh_avgCom', 'ProsConsPM_allNCom_sum', 'ProsConsPM_allNCom_avgAll',
            'ProsConsPM_allNCom_avgCom', 'ProsConsPM_allNSt_sum', 'ProsConsPM_allNSt_avgAll',
            'ProsConsPM_allNSt_avgCom',
            'ProsConsPM_allNWd_sum', 'ProsConsPM_allNWd_avgAll', 'ProsConsPM_allNWd_avgCom', 'ProsConsAdvP_simple',
            'ProsConsAdvP_allComNCh_sum', 'ProsConsAdvP_allComNCh_avgAll', 'ProsConsAdvP_allComNCh_avgCom',
            'ProsConsAdvP_allComNCom_sum', 'ProsConsAdvP_allComNCom_avgAll', 'ProsConsAdvP_allComNCom_avgCom',
            'ProsConsAdvP_allComNSt_sum', 'ProsConsAdvP_allComNSt_avgAll', 'ProsConsAdvP_allComNSt_avgCom',
            'ProsConsAdvP_allComNWd_sum', 'ProsConsAdvP_allComNWd_avgAll', 'ProsConsAdvP_allComNWd_avgCom',
            'ProsConsAdvP_allNCh_sum', 'ProsConsAdvP_allNCh_avgAll', 'ProsConsAdvP_allNCh_avgCom',
            'ProsConsAdvP_allNCom_sum', 'ProsConsAdvP_allNCom_avgAll', 'ProsConsAdvP_allNCom_avgCom',
            'ProsConsAdvP_allNSt_sum', 'ProsConsAdvP_allNSt_avgAll', 'ProsConsAdvP_allNSt_avgCom',
            'ProsConsAdvP_allNWd_sum', 'ProsConsAdvP_allNWd_avgAll', 'ProsConsAdvP_allNWd_avgCom',
            'ProsConsAdvPM_simple', 'ProsConsAdvPM_allComNCh_sum', 'ProsConsAdvPM_allComNCh_avgAll',
            'ProsConsAdvPM_allComNCh_avgCom', 'ProsConsAdvPM_allComNCom_sum', 'ProsConsAdvPM_allComNCom_avgAll',
            'ProsConsAdvPM_allComNCom_avgCom', 'ProsConsAdvPM_allComNSt_sum', 'ProsConsAdvPM_allComNSt_avgAll',
            'ProsConsAdvPM_allComNSt_avgCom', 'ProsConsAdvPM_allComNWd_sum', 'ProsConsAdvPM_allComNWd_avgAll',
            'ProsConsAdvPM_allComNWd_avgCom', 'ProsConsAdvPM_allNCh_sum', 'ProsConsAdvPM_allNCh_avgAll',
            'ProsConsAdvPM_allNCh_avgCom', 'ProsConsAdvPM_allNCom_sum', 'ProsConsAdvPM_allNCom_avgAll',
            'ProsConsAdvPM_allNCom_avgCom', 'ProsConsAdvPM_allNSt_sum', 'ProsConsAdvPM_allNSt_avgAll',
            'ProsConsAdvPM_allNSt_avgCom', 'ProsConsAdvPM_allNWd_sum', 'ProsConsAdvPM_allNWd_avgAll',
            'ProsConsAdvPM_allNWd_avgCom']

dep_vars = ['da_cf', 'da_cf_roa', 'dd_quality']

f = open('regress.do', 'w')

today = datetime.date.today().strftime('%Y%m%d')

for ind in ind_vars:
    for dep in dep_vars:
        # ind
        f.write('capture noisily qui regress {} {}\n'.format(dep, ind))
        f.write('outreg2 using {}{}result.xls, drop(i.sic2 i.fyear) '.format(today, ind))
        f.write(' add text(Year Dummy, No, Industry Dummy, No, Dependent Variable, {})'.format(dep))
        f.write(' pvalue bdec(2) tdec(2) rdec(2) nolabel\n')

        # ind + control
        f.write('capture noisily qui regress {} {} {}\n'.format(dep, ind, ' '.join(control_variables)))
        f.write('outreg2 using {}{}result.xls, drop(i.sic2 i.fyear) '.format(today, ind))
        f.write(' add text(Year Dummy, No, Industry Dummy, No, Dependent Variable, {})'.format(dep))
        f.write(' pvalue bdec(2) tdec(2) rdec(2) nolabel\n')

        # ind + control + up to you
        f.write('capture noisily qui regress {} {} {} {}\n'.format(dep, ind, ' '.join(control_variables),
                                                                   ' '.join(up_to_you)))
        f.write('outreg2 using {}{}result.xls, drop(i.sic2 i.fyear) '.format(today, ind))
        f.write(' add text(Year Dummy, No, Industry Dummy, No, Dependent Variable, {})'.format(dep))
        f.write(' pvalue bdec(2) tdec(2) rdec(2) nolabel\n')

        # ind + control + i.fyear
        f.write('capture noisily qui regress {} {} {} i.fyear\n'.format(dep, ind, ' '.join(control_variables)))
        f.write('outreg2 using {}{}result.xls, drop(i.sic2 i.fyear) '.format(today, ind))
        f.write(' add text(Year Dummy, No, Industry Dummy, No, Dependent Variable, {})'.format(dep))
        f.write(' pvalue bdec(2) tdec(2) rdec(2) nolabel\n')
