from unittest import TestCase
import unittest
from horseDataCache import HorseDataCache
from constant import path_info
import os

# https://code.tutsplus.com/tutorials/beginning-test-driven-development-in-python--net-30137


class TestHorseDataCache(TestCase):
    def setUp(self):
        self.cache = HorseDataCache()

    def test_cache_object_exist(self):
        self.assertIsInstance(self.cache, HorseDataCache, 'HorseDataCache object create failed')

    def test_get_html_cache_path(self):
        print(self.cache.get_html_cache_path())
        filepath = self.cache.get_html_cache_path()
        self.assertTrue(os.path.exists(filepath), "Cache folder {} not exist".format(filepath))

    def test_get_cache_path(self):
        demo_url = self.cache.get_cache_path("http://hk.racing.nextmedia.com/fullresult.php?date=20130206&page=05")
        print(demo_url)
        self.assertTrue(os.path.exists(demo_url), "Cache folder {} not exist".format(demo_url))

    def test_is_cache_html(self):
        url = "http://hk.racing.nextmedia.com/fullresult.php?date=20130206&page=05"
        result = self.cache.is_cache_html(url)
        self.assertTrue(result, "cached version of {} not found".format(url))

    def test_get_cache_html(self):
        url = "http://hk.racing.nextmedia.com/fullresult.php?date=20130206&page=05"
        html = self.cache.get_cache_html(url)
        self.assertIsNotNone(html, "cache cannot found for url = {}".format(url))

        url = "http://hk.racing.nextmedia.com/fullresult.php?date=20130206&page=12"
        html = self.cache.get_cache_html(url)
        self.assertIsNone(html, "cache should not be found for url = {}".format(url))


if __name__ == '__main__':
    unittest.main()