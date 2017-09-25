# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InterninfoItem(scrapy.Item):
    #招聘标题
    title = scrapy.Field()
    #招聘内容
    content = scrapy.Field()
    #链接地址
    url = scrapy.Field()
