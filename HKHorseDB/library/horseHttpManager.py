import urllib.request, urllib.parse, urllib.error
from horseDataCache import HorseDataCache
from urllib import request as urlrequest
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import os
import os.path
import time

class HorseHttpManager:
    def __init__(self, encoding='utf-8', use_cache=False, save_to_cache=False, tag=""):
        self.encoding=encoding
        self.cache = HorseDataCache()
        self.cache.encoding = encoding
        self.use_cache = use_cache
        self.save_to_cache = save_to_cache

    def get_param_url(self, url, data_list=None):
        if data_list:
            url = "{}?{}".format(url, urllib.parse.urlencode(data_list))
        return url

    def get(self, url, data_list=None, max_try=5):

        url = self.get_param_url(url, data_list)

        query = urllib.request.Request(url)
        current_try = 0
        while current_try < max_try:
            try:
                # if (current_try == 0):
                #     proxy = 'http://127.0.0.1:8080'
                #     os.environ['http_proxy'] = proxy
                response = urllib.request.urlopen(query)
                # else:
                #     os.environ['http_proxy'] = ''
                #     response = urllib.request.urlopen(query)

                html = response.read()
                if (html != None):
                    response.close()
                    return html
                else:
                    print('retry')
                    current_try = current_try + 1
            except Exception as e:
                print('exception = {}'.format(e))
                current_try = current_try + 1
        raise Exception("Cannot open page {}".format(url))

    def get_content(self, url):
        html = None
        if(self.use_cache and self.cache.is_cache_html(url)):
            html = self.cache.get_cache_html(url)
        else:
            time.sleep(3)
            print("get new page")
            html = self.get(url)
            # print(self.encoding)
            html = str(html, self.encoding)

            if(self.save_to_cache):
                self.cache.save_cache_html(url, html)

        return html