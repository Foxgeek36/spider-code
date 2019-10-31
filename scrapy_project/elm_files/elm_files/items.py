# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ElmFilesItem(scrapy.Item):
    # define the fields for your item here like:
    timeStamp = scrapy.Field()
    restaurantId = scrapy.Field()
    menu = scrapy.Field()
    recommend = scrapy.Field()
    redpack = scrapy.Field()
    rst = scrapy.Field()
    rst_first_category = scrapy.Field()
    rst_second_category = scrapy.Field()
    spider_type=scrapy.Field()
    crawling_city=scrapy.Field()
    # rating=scrapy.Field()
    # tags=scrapy.Field()
    # aptitude_info = scrapy.Field()