#!/usr/bin/env python
# encoding: utf-8
import json
import re

import pymysql
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.utils import bytes_to_str
from redis import Redis
# from tarantula.util.mysql import get_mysql_client
# from tarantula.util.redis import get_redis_client
# from tarantula.items.dianping.shop_items import ShopItem
from scrapy.extensions.logstats import LogStats

class ShopsBaseinfo(RedisSpider):
    """
    shops_baseinfo:items 保存店铺的id等信息   提供给评论和点评详情来调用
    """

    name = 'shops_baseinfo'

    # 拿到店铺列表信息的api
    api = 'http://m.api.dianping.com/searchshop.json?&regionid={}&categoryid={}&sortid=0&cityid={}&start=0&limit=50'
    sql = 'select dp_city.id as cityid,dp_meta.real_id as regionid,dp_category.id as cateid from dp_city,dp_meta,dp_category where dp_city.need_crawl=1 and dp_meta.city_id=dp_city.id;'
    redis_cli = Redis()

    custom_settings = {
        'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
        'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
        'DUPEFILTER_DEBUG': True,
        'SCHEDULER_PERSIST': True,
        'SCHEDULER_QUEUE_CLASS': 'scrapy_redis.queue.PriorityQueue',
        'REDIS_START_URLS_AS_SET':True,
        # 'REDIS_HOST':'127.0.0.1',

        # 'ITEM_PIPELINES': {
        #     'tarantula.cp.dianping.shops_baseinfo_pipelines.ShopsBaseinfoPipeline': 300,
        # },
        'REDIS_ITEMS_KEY': '%(spider)s:items',
        'REDIS_START_URLS_KEY': '%(name)s:start_urls',

        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_TIMEOUT': 60,
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'tarantula.cdm.XundailiProxy.ProxyMiddleware': 610,
        #     'tarantula.cdm.RandomUserAgent.UserAgentMiddleware': 560,
        # },
        'DOWNLOAD_DELAY': 5,
        # 'SPIDER_MIDDLEWARES': {
        #     'tarantula.cm.scrapy_magicfields.MagicFieldsMiddleware': 100,
        # },
    }



    def make_request_from_data(self, data):
        """
        scrapy-redis自帶去重功能失效，實現去重
        """
        url = bytes_to_str(data, self.redis_encoding)
        if self.redis_cli.sismember('shops_baseinfo:urls_successed',url):
            return None
        return self.make_requests_from_url(url)



    def parse(self, response):
        self.logger.info(f"Parse List {response.url}")
        try:
            infos = json.loads(response.text)
            shop_baseinfos = infos['list']
        except:
            self.logger.info('相應題解析失敗：  ',response.text)
            return
        # 返回列表數據
        # item = ShopItem()
        item = {}
        for info in shop_baseinfos:
            try:
                item['category_id'] = info['categoryId']
                item['sub_category_name'] = info['categoryName']
                item['city_id'] = info['cityId']
                item['match_text'] = info['matchText']
                item['shop_name'] = info['name']
                try:
                    item['avg_price'] = info['priceText']
                except:
                    item['avg_price'] = ''
                item['region_name'] = info['regionName']
                item['comment_total'] = info['reviewCount']
                item['power'] = info['shopPower']
                shop_state =info['shopStateInformation']
                if shop_state:
                    shop_state = shop_state[0]['text']
                item['shop_state'] = shop_state
                item['shopuuid'] = info['shopuuid']
                yield item
                # 加入請求成功隊列
                # self.redis_cli.sadd('shops_baseinfo:urls_successed', response.url)
            except:
                print(info)

        # 如果還能遍歷，那麼繼續翻頁
        if shop_baseinfos:
            pagestart = re.findall('start=(\d+)',response.url)
            if pagestart:
                pagestart = int(pagestart[0])
                nexpagestart = pagestart + 50
                nexturl = re.sub('start=\d+','start='+str(nexpagestart),response.url)
                # print(f'oldpage:{response.url}\n  nextpage: {nexturl}')
                if not self.redis_cli.sismember('shops_baseinfo:urls_successed', nexturl):
                    yield Request(
                        url=nexturl,
                        callback=self.parse
                    )




