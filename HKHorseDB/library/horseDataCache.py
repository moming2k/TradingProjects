import os
import sys
import urllib

sys.path.append(os.path.join(os.getcwd(), '..'))

# sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
from selenium import webdriver
from constant import path_info


class HorseDataCache():
    def __init__(self):
        self.browser = None
        self.encoding = 'utf-8'

        current_path = os.getcwd()
        project_path = os.path.dirname(current_path)
        self.html_cache = project_path + "/data/cache"

    def get_html_cache_path(self):
        return self.html_cache

    def get_cache_path(self, url):
        url_path = urllib.parse.quote(url).replace('/', '_')
        file_path = "{}/{}".format(self.html_cache, url_path)
        return file_path

    def is_cache_html(self, url):
        filepath = self.get_cache_path(url)
        if (os.path.isfile(filepath)):
            return True
        else:
            return False

    def get_cache_html(self, url, debug = False):
        filepath = self.get_cache_path(url)
        if (os.path.isfile(filepath)):
            if(debug):
                print("url = {} exist in cache".format(url))
            with open(filepath, 'r', encoding=self.encoding) as io_file:
                html = io_file.read()
            return html
        else:
            if (debug):
                print("url = {} not exist in cache".format(url))
            return None

    def save_cache_html(self, url, html):
        filepath = self.get_cache_path(url)

        with open(filepath, 'w', encoding=self.encoding) as out:
            out.write(html)

        return True