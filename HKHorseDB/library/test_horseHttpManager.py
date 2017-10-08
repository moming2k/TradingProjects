from unittest import TestCase
import unittest
from horseHttpManager import HorseHttpManager

if __name__ == '__main__':
    unittest.main()


class TestHorseHttpManager(TestCase):
    def setUp(self):
        self.http_manager = HorseHttpManager(encoding='big5')

    def test_get_content(self):
        html_content = self.http_manager.get_content("http://www.hkhorsedb.com/cseh/passodds.php")
        self.assertIsNotNone(html_content)