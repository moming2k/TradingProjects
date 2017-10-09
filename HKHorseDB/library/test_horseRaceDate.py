from unittest import TestCase
from horseRaceDate import HorseRaceDate

class TestHorseRaceDate(TestCase):
    def setUp(self):
        self.race_date = HorseRaceDate()
        self.race_date.show_debug = True

    def test_update_use_html_cache(self):
        self.race_date = HorseRaceDate()
        self.race_date.use_html_cache = True
        result = self.race_date.get_dates()
        self.assertIsNotNone(result)
        print(result[0:10])

    def test_update_not_use_html_cache(self):
        self.race_date = HorseRaceDate()
        self.race_date.use_html_cache = False
        result = self.race_date.get_dates()
        self.assertIsNotNone(result)
        print(result[0:10])

    def test_update_not_use_cache_and_save_pickle_cache(self):
        self.race_date = HorseRaceDate()
        self.race_date.save_pickle_cache = True
        result = self.race_date.get_dates()
        self.assertIsNotNone(result)
        print(result[0:10])

    def test_update_use_pickle_cache(self):
        self.race_date = HorseRaceDate()
        self.race_date.use_pickle_cache = True
        result = self.race_date.get_dates()
        self.assertIsNotNone(result)
        print(result[0:10])

    def test_update_not_use_html_cache_and_save_cache(self):
        self.race_date = HorseRaceDate()
        self.race_date.save_html_cache = True
        result = self.race_date.get_dates()
        self.assertIsNotNone(result)
        print(result[0:10])
