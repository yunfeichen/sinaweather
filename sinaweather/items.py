# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy import Item, Field


class SinaweatherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cityurl = scrapy.Field()
    citytemp = scrapy.Field()
    citycode = scrapy.Field()
    citycnname = scrapy.Field()
    cityenname = scrapy.Field()
    weathercode = scrapy.Field()
    weathername = scrapy.Field()
    pass
