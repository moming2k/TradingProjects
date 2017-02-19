#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step2_drow_pictures_calculate_result
# @Date: 2017-01-30
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os

import pandas as pd

from constants.path_info import temp_path, result_path

wealth_path = os.path.join(temp_path, 'buy_only_drawdown_wealth')
save_path = os.path.join(result_path, 'buy_only_cost_no_down')

wealth_df = pd.read_pickle(os.path.join(result_path, '_only_buy_no_cost_drawdown.p'))