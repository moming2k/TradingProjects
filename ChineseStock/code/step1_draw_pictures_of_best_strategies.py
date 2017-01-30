#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step1_draw_pictures_of_best_strategies
# @Date: 2017-01-30
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

from util_function import plot_picture
from path_info import result_path

save_path = os.path.join(result_path, 'buy_only_no_cost_no_down')
best_strategies_path = os.path.join(save_path, 'pictures')
if not os.path.isdir(best_strategies_path):
    os.makedirs(best_strategies_path)

best_strategies_df = pd.read_pickle(os.path.join(save_path, '20170129_best_strategies.p'))
wealth_df = pd.read_pickle(os.path.join(save_path, '20170129_only_buy_no_cost_no_drawdown_wealth.p'))

for name in best_strategies_df['name']:
    plot_picture(wealth_df[name], name, os.path.join(best_strategies_path, '{}.png'.format(name)))
