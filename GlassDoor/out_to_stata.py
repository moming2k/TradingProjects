#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: out_to_stata
# Author: Mark Wang
# Date: 26/10/2016

import os

import pandas as pd


def process_name(name):
    new_name = name.replace('CommunGNLP', '')
    new_name = new_name.replace('_firmYear_', '_')
    new_name = new_name.replace('netProsConsAdviceNum', 'allNum')
    new_name = new_name.replace('netProsConsAdviceCommunNum', 'allCommunNum')
    new_name = new_name.replace('netProsConsCommunNum', 'allCommunNum')
    new_name = new_name.replace('netProsConsNum', 'allNum')
    new_name = new_name.replace('net', '')
    new_name = new_name.replace('average', 'avg')
    new_name = new_name.replace('Advice', 'Adv')
    new_name = new_name.replace('advice', 'adv')
    new_name = new_name.replace('Commun', 'Com')
    new_name = new_name.replace('NumWord', 'NWd')
    new_name = new_name.replace('NumSent', 'NSt')
    new_name = new_name.replace('NumChar', 'NCh')
    new_name = new_name.replace('NumCom', 'NCom')
    new_name = new_name.replace('Pol', 'P')
    new_name = new_name.replace('Mag', 'M')
    return new_name


s = process_name('netProsConsAdviceCommunGNLPPol_firmYear_netProsConsAdviceCommunNumWord_averageCommun')
print s
print len(s)
