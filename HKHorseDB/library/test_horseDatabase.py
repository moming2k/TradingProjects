from unittest import TestCase
from horseDatabase import HorseDatabase

class TestHorseDatabase(TestCase):
    def test_connect(self):
        database = HorseDatabase()
        database.connect(dbname="horses", user="moming2k", password="kec7gopi")
        self.assertIsNot(database, None, "database connection failed to connect")