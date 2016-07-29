#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: QuestionFromProfWang
# File name: google_map_spider
# Author: Mark Wang
# Date: 29/7/2016


import scrapy


class GoogleMapSpider(scrapy.Spider):
    name = "google map"
    allowed_domains = ["google.com"]
    start_urls = [
        "https://maps.google.com/?cid=16573829435820636979",
    ]

    def parse(self, response):
        filename = 'google_page.html'
        print dir(response)
        with open(filename, 'wb') as f:
            f.write(response.body)
