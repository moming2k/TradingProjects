from bs4 import BeautifulSoup
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
from urllib.parse import urlparse, unquote_to_bytes, parse_qs
from urllib.parse import quote
from urllib.parse import unquote

from horseDataCache import HorseDataCache
from horseHttpManager import HorseHttpManager
from horseRaceDate import HorseRaceDate


class AppledailyRaceRecord():
    def __init__(self, show_debug=False, use_html_cache=True, save_html_cache=True, use_pickle_cache=True, save_pickle_cache=True ):
        self.appledaily_web_columns = \
            ['Date','RaceNumber','HorseNo','HorseId','HorseHref','HorseName','Age','JockeyName','JockeyHref','ActualWt',
             'Draw', 'Rate','Owner','DeclarHorseWt','WinOddBeforeNight','WinOddBeforeGate',
             'WinOdd','WinInTenThousand','PInTenThousand','P_Odd','PlaceInMiddle','Place',
             'TimeInMiddle','FinishTime','LBW']

        self.cache_manager = HorseDataCache()
        self.show_debug = show_debug
        self.use_html_cache = use_html_cache
        self.save_html_cache = save_html_cache
        self.use_pickle_cache = use_pickle_cache
        self.save_pickle_cache = save_pickle_cache

        self.race_result_template = {'HorseNo': None,
                                     'HorseId': None,
                                     'HorseHref': None,
                                    'HorseName': None,
                                    'Age': None,
                                    'JockeyName': None,
                                    'JockeyHref': None,
                                    'ActualWt': None,
                                    'Draw': None,
                                    'Rate': None,
                                    'Owner': None,
                                    'DeclarHorseWt': None,
                                    'WinOddBeforeNight': None,
                                    'WinOddBeforeGate': None,
                                    'WinOdd': None,
                                    'WinInTenThousand': None,
                                    'PInTenThousand': None,
                                    'P_Odd': None,
                                    'PlaceInMiddle': None,
                                    'Place': None,
                                    'TimeInMiddle': None,
                                    'FinishTime': None,
                                    'LBW': None
                        }

        self.horse_overall_ranking_df_template = [
            'horse_id',
            'condition',
            'ground',
            'total',
            't1',
            't2',
            't3',
            'loss']

        self.horse_overall_ranking_template = {
            'horse_id': None,
            'condition': None,
            'ground': None,
            'total': None,
            't1': None,
            't2': None,
            't3': None,
            'loss': None
        }

        self.horse_track_ranking_df_template = [
            'horse_id',
            'course',
            'ground',
            'distance',
            'total',
            't1',
            't2',
            't3',
            'loss']

        self.horse_track_ranking_template = {
            'horse_id': None,
            'course': None,
            'ground': None,
            'distance': None,
            'total': None,
            't1': None,
            't2': None,
            't3': None,
            'loss': 0
        }

    def get_race_records(self):
        if (self.use_pickle_cache):
            with open("data/race_date_concat.p", "rb") as f:
                race_result_records = pickle.load(f)
            if (self.show_debug):
                print("load race records detail from pickle")
            return race_result_records
        else:
            pd_array = []
            records_ids = self.get_race_records_ids()
            for race_date_record_id in records_ids:
                if(self.show_debug):
                    print("processing date at {}".format(race_date_record_id))
                    decoded_records = self.get_race_record_by_race_record_id(race_date_record_id)
                    if (decoded_records is not None):
                        pd_array.append(decoded_records)

            print("processed records count = {}".format(len(pd_array)))

            race_date_concat = pd.concat(pd_array, ignore_index=True)

            if(self.save_pickle_cache):
                if(self.show_debug):
                    print("saving all race records to pickle_cache")

                with open("data/race_date_concat.p", "wb") as f:
                    pickle.dump(race_date_concat, f)

                if (self.show_debug):
                    print("saved all race records to pickle_cache")

            return race_date_concat

    def get_race_records_ids(self):
        if (self.use_pickle_cache):
            with open("data/race_csv_array.p", "rb") as f:
                race_records_ids = pickle.load(f)
            if (self.show_debug):
                print("load race date with race id from pickle")
            return race_records_ids
        else:
            horse_race_date = HorseRaceDate()
            horse_race_date.use_pickle_cache = True
            horse_race_dates = horse_race_date.get_dates()

            race_records_ids = []
            for race_date in horse_race_dates:
                count = self.race_count_by_date(race_date)
                for index in range(1, count + 1):
                    race_index = str(index).zfill(2)
                    race_records_ids.append("{}_{}".format(race_date, race_index))

            if(self.save_pickle_cache):
                if (self.show_debug):
                    print("save to pickle cache")
                with open("data/race_csv_array.p", "wb") as f:
                    pickle.dump(race_records_ids, f)

            return race_records_ids

    def get_race_record_by_race_record_id(self, race_record_id=""):
        if "_" in race_record_id:
            date_str , race_id = race_record_id.split("_")
            return self.get_race_record(date_str, race_id)
        else:
            raise Exception("record id doesn't contain underscore")

    def get_race_record(self, date_str="", race_id=""):
        url = 'http://hk.racing.nextmedia.com/fullresult.php?date={}&page={}'.format(date_str, race_id)

        # print(url)
        http_manager = HorseHttpManager(encoding='utf-8')
        http_manager.use_cache = self.use_html_cache
        http_manager.save_to_cache = self.save_html_cache
        html = http_manager.get_content(url)

        records = self.process_race_record_html(html, date_str, race_id)

        return records

    def process_race_record_html(self, html, date_str, race_id):  # , driver, race_course='ST'):

        result_df = pd.DataFrame(columns=self.appledaily_web_columns)

        filename = '{}_{}.xlsx'.format(date_str, race_id)

        failed_info = ''

        soup = BeautifulSoup(html, "html.parser")
        tables = soup.findAll('table')
        if(len(tables) < 3):
            return None

        table = tables[2]
        record_trs = table.findAll('tr')[2:-1]

        try:
            for index in range(0, len(record_trs) - 1):
                tmp_result = self.race_result_template.copy()

                next_td_list = record_trs[index].findAll('td')

                try:
                    tmp_result['Date'] = date_str
                except:
                    print('Can not find Date')

                try:
                    tmp_result['RaceNumber'] = race_id
                except:
                    print('Can not find Race Number')

                try:
                    tmp_result['HorseNo'] = self.convert_str_to_int(next_td_list[0].text)
                except IndexError:
                    print('Can not find HorseNo')

                try:
                    tmp_result['HorseHref'] = next_td_list[1].findAll('a')[0].attrs['href']
                except IndexError:
                    print('Can not find HorseId')

                try:
                    tmp_result['HorseName'] = next_td_list[1].text
                except IndexError:
                    print('Can not find HorseName')
                    continue

                try:
                    tmp_result['Age'] = self.convert_str_to_int(next_td_list[2].text)
                except IndexError:
                    print('Can not find Age')

                try:
                    tmp_result['JockeyName'] = next_td_list[3].text
                except IndexError:
                    print('Can not find JockeyName')

                try:
                    tmp_result['JockeyHref'] = next_td_list[3].findAll('a')[0].attrs['href']
                except IndexError:
                    print('Can not find Jockey Href')

                try:
                    tmp_result['ActualWt'] = self.convert_str_to_int(next_td_list[4].text)
                except IndexError:
                    print('Can not find ActualWt')

                try:
                    tmp_result['Draw'] = self.convert_str_to_int(next_td_list[5].text)
                except IndexError:
                    print('Can not find Draw')

                try:
                    tmp_result['Rate'] = self.convert_str_to_int(next_td_list[6].text)
                except IndexError:
                    print('Can not find Rate')

                try:
                    tmp_result['Owner'] = next_td_list[7].text
                except IndexError:
                    print('Can not find Owner')

                try:
                    tmp_result['DeclarHorseWt'] = self.convert_str_to_int(next_td_list[8].text)
                except IndexError:
                    print('Can not find DeclarHorseWt')

                try:
                    tmp_result['WinOddBeforeNight'] = self.convert_str_to_float(next_td_list[9].text)
                except IndexError:
                    print('Can not find WinOddBeforeNight')

                try:
                    tmp_result['WinOddBeforeGate'] = self.convert_str_to_float(next_td_list[10].text)
                except IndexError:
                    print('Can not find WinOddBeforeGate')

                try:
                    tmp_result['WinOdd'] = self.convert_str_to_float(next_td_list[11].text)
                except IndexError:
                    print('Can not find WinOdd')

                try:
                    tmp_result['WinInTenThousand'] = self.convert_str_to_float(next_td_list[12].text)
                except IndexError:
                    print('Can not find WinInTenThousand')

                try:
                    tmp_result['PInTenThousand'] = self.convert_str_to_float(next_td_list[13].text)
                except IndexError:
                    print('Can not find PInTenThousand')

                try:
                    tmp_result['P_Odd'] = self.convert_str_to_float(next_td_list[14].text)
                except IndexError:
                    print('Can not find P_Odd')

                try:
                    tmp_result['PlaceInMiddle'] = next_td_list[15].text
                except IndexError:
                    print('Can not find PlaceInMiddle')

                try:
                    tmp_result['Place'] = self.convert_str_to_int(next_td_list[16].text)
                except IndexError:
                    print('Can not find Place')

                if (len(next_td_list) == 20):
                    try:
                        tmp_result['TimeInMiddle'] = next_td_list[17].text
                    except IndexError:
                        print('Can not find TimeInMiddle')

                    try:
                        tmp_result['FinishTime'] = next_td_list[18].text
                    except IndexError:
                        print('Can not find FinishTime')

                    try:
                        tmp_result['LBW'] = next_td_list[19].text
                    except IndexError:
                        print('Can not find LBW')
                else:
                    try:
                        tmp_result['FinishTime'] = next_td_list[17].text
                    except IndexError:
                        print('Can not find FinishTime')

                    try:
                        tmp_result['LBW'] = next_td_list[18].text
                    except IndexError:
                        print('Can not find LBW')

                result_df.loc[index] = tmp_result

            # result_df.to_excel(os.path.join(save_path, '{}_{}.xlsx'.format(date_str, race_id)), index=False)
            # result_df.to_csv(os.path.join(save_path, '{}_{}.cvs'.format(date_str, race_id)), index=False)

        except Exception as err:
            failed_info = '{} {}: test_failed as {}'.format(failed_info, datetime.today().strftime('%Y-%m-%d'), err)
            print(failed_info)
        return result_df

    def update(self):
        url = 'http://www.hkhorsedb.com/cseh/passodds.php'
        self.html = None

        http_manager = HorseHttpManager(encoding='big5')
        http_manager.use_cache = self.use_html_cache
        http_manager.save_to_cache = self.save_html_cache
        self.html = http_manager.get_content(url)

        if (self.html is None or self.html == ''):
            raise Exception("Failed to update the race date array")

        self.race_date_array = self.process_html()

        if (self.save_pickle_cache):
            if(self.show_debug):
                print("save to pickle cache")
            with open("data/race_date_array.p", "wb") as f:
                pickle.dump(self.race_date_array, f)

        return self.race_date_array

    def process_html(self):
        if(self.html is None or self.html == ''):
            raise Exception("HTML for race date is not there to be process")

        soup = BeautifulSoup(self.html, "html.parser")
        tr_list = soup.findAll('table')[15].findAll('tr')[1:]

        race_date_array = []

        for i in range(0, len(tr_list) - 1):
            tr = tr_list[i]
            tds = tr.findAll('td')

            for j in range(0, len(tds)):
                detail_date = tds[j].text

                if (detail_date != "-"):
                    normal_data = ''.join(reversed(detail_date.split('-')))

                    if (normal_data != ""):
                        race_date_array.append(normal_data)

        return race_date_array

    def race_count_by_date(self, date_str):
        url = 'http://hk.racing.nextmedia.com/fullresult.php?date={}&page=01'.format(date_str)

        http_manager = HorseHttpManager(encoding='utf-8')
        http_manager.use_cache = self.use_html_cache
        http_manager.save_to_cache = self.save_html_cache
        html = http_manager.get_content(url)

        soup = BeautifulSoup(html, "html.parser")
        try:
            return len(soup.findAll('table')[1].findAll('tr')[0].findAll('td')[0].findAll('a', href=True))
        except Exception as err:
            return -1

    # def get_all_horse_detail(self):
    #     race_records = self.get_race_records()
    #     print("race_records count = {}".format(len(race_records)))
    #     for index, row in race_records.iterrows():
    #         print("index = {}".format(index))
    #         try:
    #             self.get_horse_detail(row['HorseHref'])
    #         except Exception as err:
    #             print("failed to handle href = {}".format(row['HorseHref']))

    def get_all_horse_detail(self):
        race_records = self.get_race_records()
        horse_hrefs = race_records['HorseHref'].unique()

        horse_overall_ranking = None
        horse_track_ranking = None

        if (False and self.use_pickle_cache):
            with open("data/horse_overall_ranking.p", "rb") as f:
                horse_overall_ranking = pickle.load(f)
            if (self.show_debug):
                print("load horse overall ranking from pickle")

            with open("data/horse_track_ranking.p", "rb") as f:
                horse_overall_ranking = pickle.load(f)
            if (self.show_debug):
                print("load horse track ranking from pickle")

            return [horse_overall_ranking, horse_overall_ranking]
        else:
            horse_overall_ranking_df_array = []
            horse_track_ranking_df_array = []

            print("horse href count = {}".format(len(horse_hrefs)))
            # for index, row in horse_hrefs.iterrows():
            index = 1
            for row_index in range(0, len(horse_hrefs)-1):
                print("index = {}".format(row_index))

                try:
                    horse_id = horse_hrefs[row_index]
                    html = self.get_horse_detail(horse_id)
                    horse_overall_ranking_df, horse_track_ranking_df = self.process_horse_detail(horse_id, html)
                    horse_overall_ranking_df_array.append(horse_overall_ranking_df)
                    horse_track_ranking_df_array.append(horse_track_ranking_df)
                except Exception as err:
                    print("failed to handle href = {} with error = {}".format(horse_hrefs[row_index], err))
                index = index + 1

            horse_overall_ranking = pd.concat(horse_overall_ranking_df_array, ignore_index=True)
            horse_track_ranking = pd.concat(horse_track_ranking_df_array, ignore_index=True)

            if (self.save_pickle_cache):
                if (self.show_debug):
                    print("save to pickle cache")
                with open("data/horse_overall_ranking.p", "wb") as f:
                    pickle.dump(horse_overall_ranking, f)

                with open("data/horse_track_ranking.p", "wb") as f:
                    pickle.dump(horse_track_ranking, f)

            return [horse_overall_ranking, horse_track_ranking]

    def get_horse_detail(self, href):
        url = 'http://hk.racing.nextmedia.com/{}'.format(href)
        http_manager = HorseHttpManager(encoding='utf-8')
        http_manager.use_cache = self.use_html_cache
        http_manager.save_to_cache = self.save_html_cache
        html = http_manager.get_content(url)
        return html

    def process_horse_detail(self, horse_id, html):

        parsed_url = urlparse(horse_id)
        qs_horse = parse_qs(parsed_url.query)
        # print(qs_horse)

        horse_actual_id = qs_horse['temp_horid'][0]
        # print("horse_actual_id = {}".format(horse_actual_id))

        soup = BeautifulSoup(html, "html.parser")
        tables = soup.findAll('table')
        table = tables[2]
        results = soup.find('img', {'src': './img/search/button_03.gif'}).find_parents('table')
        index_all = 0
        index_course = 0
        index = 0
        table = results[1]
        # print(table.prettify())

        horse_overall_ranking_df = pd.DataFrame(columns=self.horse_overall_ranking_df_template)
        horse_track_ranking_df = pd.DataFrame(columns=self.horse_track_ranking_df_template)

        a_s = table.find_all('a', {'class':'arttextbold'})
        for result in a_s:
            # print("-------- {} ------- ".format(index))
            # print(result.prettify())
            # print(result.parent()[0].prettify())
            # print(result.parent()[0].attrs['href'])
            urls = urlparse(result.parent()[0].attrs['href'])
            url_unquote_raw = unquote_to_bytes(result.parent()[0].attrs['href']).decode('big5')
            # print(url_unquote_raw)
            parsed_url = urlparse(url_unquote_raw)
            # print(parsed_url)

            qs = parse_qs(parsed_url.query)
            # print(qs)
            if('t_go_condition' in qs):

                # print('t_go_condition {} - t_ground {} - tot {} - t1 {} - t2 {} - t3 {} - t4 {}'.format(
                #     qs['t_go_condition'][0].strip(),
                #     qs['t_ground'][0],
                #     qs['tot'][0],
                #     qs['t1'][0],
                #     qs['t2'][0],
                #     qs['t3'][0],
                #     qs['t4'][0]
                # ))
                tmp_result = self.horse_overall_ranking_template.copy()
                tmp_result['horse_id'] = horse_actual_id
                tmp_result['condition'] = qs['t_go_condition'][0].strip()
                tmp_result['ground'] = qs['t_ground'][0]
                tmp_result['total'] = qs['tot'][0]
                tmp_result['t1'] = qs['t1'][0]
                tmp_result['t2'] = qs['t2'][0]
                tmp_result['t3'] = qs['t3'][0]
                tmp_result['loss'] = qs['t4'][0]

                horse_overall_ranking_df.loc[index_all] = tmp_result

                index_all = index_all + 1
            # except:
            #     i = 0

            else:
                # print('t_course {} - t_ground {} - t_distance {} - tot {} - t1 {} - t2 {} - t3 {} - t4 {}'.format(
                #     qs['t_course'][0],
                #     qs['t_ground'][0],
                #     qs['t_distance'][0],
                #     int(qs['tot'][0]),
                #     int(qs['t1'][0]),
                #     int(qs['t2'][0]),
                #     int(qs['t3'][0]),
                #     int(qs['t4'][0])
                # ))

                tmp_result = self.horse_track_ranking_template.copy()
                tmp_result['horse_id'] = horse_actual_id
                tmp_result['course'] = qs['t_course'][0]
                tmp_result['ground'] = qs['t_ground'][0]
                tmp_result['distance'] = qs['t_distance'][0]
                tmp_result['total'] = qs['tot'][0]
                tmp_result['t1'] = qs['t1'][0]
                tmp_result['t2'] = qs['t2'][0]
                tmp_result['t3'] = qs['t3'][0]
                tmp_result['loss'] = qs['t4'][0]
                # print(tmp_result['ground'][0])
                horse_track_ranking_df.loc[index_course] = tmp_result

                index_course = index_course + 1
            # except:
            #     i = 0

            # print(result.parent()[1].prettify())
            # print(result.parent()[2].text)
            index = index + 1

        return [horse_overall_ranking_df, horse_track_ranking_df]
        # for result in results:
        #     print("-------- {} ------- ".format(index))
        #     print(result.prettify())
        #     index = index + 1

    def convert_str_to_int(self, int_str):
        try:
            return int(int_str)
        except Exception as err:
            return int_str

    def convert_str_to_float(self, int_str):
        try:
            return float(int_str)
        except Exception as err:
            return int_str