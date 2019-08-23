# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import AutohomespiderItem


class AutohomeSpiderSpider(scrapy.Spider):
    name = 'autohome_spider'

    custom_settings = {
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 1,

        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'accept-encoding': "gzip, deflate",
            'cache-control': "no-cache",
        },
        'REDIS_HOST': '127.0.0.1',
        'REDIS_PORT': '6379',
        'REDIS_DB': '0',
        'ITEM_PIPELINES': {
            'AutohomeSpider.pipelines.RedisStartUrlsPipeline': 301,
        },

    }

    start_urls = ['http://www.autohome.com.cn/grade/carhtml/{}.html'.format(chr(ord('A') + i))
                  for i in range(26)]
    # start_urls =['https://www.autohome.com.cn/grade/carhtml/A.html']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):

        for node in response.xpath('//li[@id]'):
            item = AutohomespiderItem()
            seriesid = node.xpath('./@id').extract()[0][1:]
            item['url'] = 'https://koubei.app.autohome.com.cn/autov8.3.5/alibi/seriesalibiinfos-pm2-ss{}-st0-p1-s20-isstruct0-o0.json'.format(seriesid)
            yield item


