from bs4 import BeautifulSoup
import pickle

from horseDataCache import HorseDataCache
from horseHttpManager import HorseHttpManager
from horseRaceDate import HorseRaceDate

class AppledailyRaceRecord():
    def __init__(self, show_debug=False, use_html_cache=True, save_html_cache=True, use_pickle_cache=True, save_pickle_cache=True ):
        self.appledaily_web_columns = \
            ['Date','RaceNumber','HorseNo','HorseName','Age','JockeyName','ActualWt',
             'Draw', 'Rate','Owner','DeclarHorseWt','WinOddBeforeNight','WinOddBeforeGate',
             'WinOdd','WinInTenThousand','PInTenThousand','P_Odd','PlaceInMiddle','Place',
             'TimeInMiddle','FinishTime','LBW']

        self.cache_manager = HorseDataCache()
        self.show_debug = show_debug
        self.use_html_cache = use_html_cache
        self.save_html_cache = save_html_cache
        self.use_pickle_cache = use_pickle_cache
        self.save_pickle_cache = save_pickle_cache

    def get_race_records(self):
        if (self.use_pickle_cache):
            with open("data/race_date_concat.p", "rb") as f:
                race_result_records = pickle.load(f)
            if (self.show_debug):
                print("load race records detail from pickle")
            return race_result_records
        else:
            raise Exception("No yet implement")

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

    def get_race_record(self, date_str="", race_id=""):
        url = 'http://hk.racing.nextmedia.com/fullresult.php?date={}&page={}'.format(date_str, race_id)
        race_date_array = None
        if(self.use_pickle_cache):
            with open("data/race_date_array.p", "rb") as f:
                race_date_array = pickle.load(f)
            if(self.show_debug):
                print("load race date from pickle")
            return race_date_array
        else:
            raise Exception("No yet implement")

        race_date_array = self.update()

        return race_date_array

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