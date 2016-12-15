#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: functions
# @Date: 2016-12-14
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


def calculate_score(tic1, tic2):
    if len(tic2) < 3 or tic1[0] != tic2[0]:
        return 0

    tic1 = tic1.upper()
    tic2 = tic2.upper()

    if len(tic1) > 4:
        tic1 = tic1[:4]

    score = 10

    is_same = [False] * max(len(tic1), len(tic2))
    is_same[0] = True

    for i in range(1, min(len(tic1), len(tic2))):
        if tic1[i] == tic2[i]:
            score += 10
            is_same[i] = True

    chr_dict = {}
    for i in range(1, len(tic1)):
        if is_same[i]:
          continue

        if tic1[i] in chr_dict:
            chr_dict[tic1[i]] += 1

        else:
            chr_dict[tic1[i]] = 1

    for i in range(1, len(tic2)):
        if is_same[i]:
          continue

        if tic2[i] in chr_dict:
            chr_dict[tic2[i]] -= 1
            if chr_dict[tic2[i]] == 0:
                del chr_dict[tic2[i]]

            score += 1

    return score


if __name__ == '__main__':
    tic1 = 'CACS'
    tic2 = 'CLNS'
    print calculate_score(tic1, tic2)
