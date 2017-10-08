from bs4 import BeautifulSoup

from horseDataCache import HorseDataCache
from horseHttpManager import HorseHttpManager

class HorseRaceDate():
    def __init__(self, show_debug=False):
        self.cache_manager = HorseDataCache()
        self.show_debug = show_debug


    def update(self, use_cache=False):
        url = 'http://www.hkhorsedb.com/cseh/passodds.php'
        self.html = None

        if( self.cache_manager.is_cache_html(url) and use_cache ):
            if(self.show_debug):
                print("use cache race date")
            self.html = self.cache_manager.get_cache_html(url)
        else:
            if (self.show_debug):
                print("not use cache race date")
            http_manager = HorseHttpManager(encoding='big5')
            self.html = http_manager.get_content("http://www.hkhorsedb.com/cseh/passodds.php")

        if (self.html is None):
            raise Exception("Failed to update the race date array")

        self.race_date_array = self.process_html()

        return self.race_date_array

    def process_html(self):
        if(self.html is None):
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