#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: DownloadHKHorseDb
# @Date: 2016-12-29
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import urllib
import urllib2

from BeautifulSoup import BeautifulSoup
import pandas as pd

from hkhorsedb_ctrl import HkhorseDbCtrl


def get(url, data_list=None, max_try=3):
    if data_list:
        url = "{}?{}".format(url, urllib.urlencode(data_list))
    query = urllib2.Request(url)
    current_try = 0
    while current_try < max_try:
        try:
            response = urllib2.urlopen(query)
            html = response.read()
            response.close()
            return html
        except Exception, e:
            return None
    raise Exception("Cannot open page {}".format(url))


if __name__ == '__main__':
    from xvfbwrapper import Xvfb

    url = 'http://www.hkhorsedb.com/cseh/passodds.php'
    html = get(url)
    soup = BeautifulSoup(unicode(html, 'big5'))
    tr_list = soup.findAll('table')[15].findAll('tr')[1:]
    vdisplay = Xvfb(width=1366, height=768)
    vdisplay.start()

    horse_ctrl = HkhorseDbCtrl()
    horse_ctrl.start()

    result_path = '/home/wangzg/Documents/WangYouan/Trading/HKHorse/horse_win_loss_data'

    column_name = ['horse_name', 'win_loss_rate', 'is_winner']

    try:
        for tr in tr_list:
            for td in tr.findAll('td'):
                detail_date = td.text
                if detail_date == '--':
                    continue

                date_info = ''.join(detail_date.split('-'))
                normal_data = ''.join(reversed(detail_date.split('-')))
                save_dir = os.path.join(result_path, normal_data)

                print normal_data
                if not os.path.isdir(save_dir):
                    os.makedirs(save_dir)
                else:
                    continue

                result_info = horse_ctrl.get_win_loss_rate(date_info)

                for i in range(len(result_info)):
                    result = result_info[i]
                    df = pd.DataFrame(result, columns=column_name)
                    df.to_csv(os.path.join(save_dir, '{}.csv'.format(i + 1)), encoding='utf8')
                    df.to_pickle(os.path.join(save_dir, '{}.p'.format(i + 1)))


    except Exception:
        import traceback

        traceback.print_exc()

    finally:
        horse_ctrl.stop()
        vdisplay.stop()
