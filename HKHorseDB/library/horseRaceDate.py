from bs4 import BeautifulSoup
import pickle

from horseDataCache import HorseDataCache
from horseHttpManager import HorseHttpManager

class HorseRaceDate():
    def __init__(self, show_debug=False, use_html_cache=False, save_html_cache=False, use_pickle_cache=False, save_pickle_cache=False ):
        self.cache_manager = HorseDataCache()
        self.show_debug = show_debug
        self.use_html_cache = use_html_cache
        self.save_html_cache = save_html_cache
        self.use_pickle_cache = use_pickle_cache
        self.save_pickle_cache = save_pickle_cache

    def get_dates(self):
        race_date_array = None
        if(self.use_pickle_cache):
            with open("data/race_date_array.p", "rb") as f:
                race_date_array = pickle.load(f)
            if(self.show_debug):
                print("load race date from pickle")
            return race_date_array

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