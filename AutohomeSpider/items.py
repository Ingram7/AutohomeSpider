# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import  Field


class AutohomespiderItem(scrapy.Item):

    url = Field()

class KoubeispiderItem(scrapy.Item):

    Koubeiid = Field()
    memberid = Field()
    membername = Field()
    brandid = Field()
    brandname = Field()
    seriesid = Field()
    seriesname = Field()
    specid = Field()
    specname = Field()
    lastedit = Field()
    commentcount = Field()
    helpfulcount = Field()
    visitcount = Field()
    content = Field()