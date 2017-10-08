from unittest import TestCase
from horseRaceDate import HorseRaceDate

class TestHorseRaceDate(TestCase):
    def setUp(self):
        self.race_date = HorseRaceDate()

    def test_update(self):
        self.race_date.update()

    def test_update_use_cache(self):
        self.race_date.update(use_cache=True)