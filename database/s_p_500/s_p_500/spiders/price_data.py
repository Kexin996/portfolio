#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Using Scrapy to load data from AlphaVantage
"""

import scrapy

# define a spider class for getting price data
class PricesSpider(scrapy.Spider):
    # name: the name of spider
    name = "price"
    custom_settings = {'CONCURRENT_REQUESTS': 100}
    # define a function to start requests
    def start_requests(self):
        avt_base_url = 'https://www.alphavantage.co'
        print(scrapy.Request(url = avt_base_url,callback = self.parse))
    def parse(self):
        print()
    
temp = PricesSpider()
temp.start_requests()