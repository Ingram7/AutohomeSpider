# -*- coding: utf-8 -*-

import json
import re
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from ..items import KoubeispiderItem


class KoubeiSpiderSpider(RedisSpider):

    name = 'koubei_spider'
    # allowed_domains = ['autohome.com.cn']

    koubei_url = 'https://koubei.app.autohome.com.cn/autov8.3.5/alibi/seriesalibiinfos-pm2-ss{}-st0-p1-s20-isstruct0-o0.json'
    koubei_info_url = 'https://koubei.app.autohome.com.cn/autov8.3.5/alibi/alibiinfobase-pm2-k{}.json'

    custom_settings = {
        'CONCURRENT_REQUESTS': 32,
        'DOWNLOAD_DELAY': 0.1,

        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN',
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'accept-encoding': "gzip, deflate",
            'cache-control': "no-cache",
        },

        'MONGO_URI': '127.0.0.1:27017',
        'MONGO_DATABASE': 'koubei',

        'REDIS_START_URLS_AS_SET': True,

        'ITEM_PIPELINES': {
            'AutohomeSpider.pipelines.MongoPipeline': 301,
        },
    }

    def parse(self, response):
        """
        口碑列表
        """
        if re.findall('st0-p1-s20', response.url):
            # 如果是第1页，一次性获取后面的所有页
            result = json.loads(response.text)
            pagecount = result.get('result').get('pagecount')
            if pagecount:
                pagecount = int(pagecount)
                for page_num in range(2, pagecount + 1):
                    page_url = response.url.replace('st0-p1-s20', 'st0-p{}-s20'.format(page_num))
                    yield Request(page_url, self.parse, dont_filter=True,
                                  # headers={'User-Agent': self.mobile_ua, 'Referer': response.url}
                                  )
        """
        解析本页的数据 获取 Koubeiid
        """
        result = json.loads(response.text)
        data_list = result.get('result').get('list')
        for node in data_list:
            Koubeiid = node.get('Koubeiid')
            yield Request(self.koubei_info_url.format(Koubeiid), callback=self.parse_koubei,
                          meta={'Koubeiid': Koubeiid}, dont_filter=True)


    def parse_koubei(self, response):
        """
        口碑详情页
        """
        item = KoubeispiderItem()
        result = json.loads(response.text)

        item['Koubeiid'] = response.meta['Koubeiid']
        item['memberid'] = result.get('result').get('memberid')
        item['membername'] = result.get('result').get('membername')
        item['brandid'] = result.get('result').get('brandid')
        item['brandname'] = result.get('result').get('brandname')
        item['seriesid'] = result.get('result').get('seriesid')
        item['seriesname'] = result.get('result').get('seriesname')
        item['specid'] = result.get('result').get('specid')
        item['specname'] = result.get('result').get('specname')
        item['lastedit'] = result.get('result').get('lastedit')
        item['commentcount'] = result.get('result').get('commentcount')
        item['helpfulcount'] = result.get('result').get('helpfulcount')
        item['visitcount'] = result.get('result').get('visitcount')
        content = result.get('result').get('content').replace('\r\n','')
        content = ''.join([x.strip() for x in content])
        item['content'] = content
        yield item






