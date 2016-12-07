#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: get_sig_result_sic_all
# @Date: 2016-12-07
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import shutil


def is_significant_result(path):
    cons_sig = False
    pros_sig = False

    f = open(path)
    s = f.read()
    f.close()

    s_list = s.split('\n')
    for i in range(len(s_list)):
        line = s_list[i]
        is_sig = True
        if line.startswith('pros'):
            tag = 'pros'

        elif line.startswith('cons'):
            tag = 'cons'

        else:
            continue

        t_stat_line = set(s_list[i + 1].split('\t'))

        while '' in t_stat_line:
            t_stat_line.remove('')

        for t_value in t_stat_line:
            if abs(float(t_value[1:-1])) < 1:
                is_sig = False
                break

        if tag == 'pros':
            pros_sig = is_sig
        else:
            cons_sig = is_sig

    return cons_sig and pros_sig


root_path = '/home/wangzg/Documents/WangYouan/research/Glassdoor/winsor5_result'
sig_path = '/home/wangzg/Documents/WangYouan/research/Glassdoor/winsor5_sig_result'

result_dirs = ['winsor5_all_sic', 'winsor5_all_sic_com5', 'winsor5_all_sic_com1', 'winsor5_all_sic_com3']

for win_dir in result_dirs:
    win_path = os.path.join(root_path, win_dir)
    for result_dir in os.listdir(win_path):
        result_path = os.path.join(win_path, result_dir)

        if not os.path.isdir(result_path):
            continue

        for result_file in os.listdir(result_path):
            file_path = os.path.join(result_path, result_file)

            if not file_path.endswith('.txt'):
                continue

            if is_significant_result(file_path):
                sig_dir = os.path.join(sig_path, win_dir, result_dir)
                if not os.path.isdir(sig_dir):
                    os.makedirs(sig_dir)

                sig_file_path = os.path.join(sig_dir, result_file)
                shutil.copy(file_path, sig_file_path)

                shutil.copy('{}.xls'.format(file_path[:-4]), '{}.xls'.format(sig_file_path[:-4]))
