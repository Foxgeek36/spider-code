#!/usr/bin/env python
# encoding: utf-8
import json
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from tarantula.util.redis import get_redis_client
from tarantula.items.dianping.comment_items import CommentItem


class ShopsBaseinfo(RedisSpider):
    """
    shops_baseinfo:items 保存店铺的id等信息   提供给评论和点评详情来调用
    """

    name = 'shops_comments_top500'

    # 拿到店铺评论的api
    # pageSize 最大能拿到500条
    api = 'https://m.dianping.com/ugc/review/shop/shopreview?pageSize=500&mtsiReferrer=pages/detail/detail?shopUuid={}&online=1&shopuuid={}&shopId={}&pageName=shop&shopUuid={}'
    redis_cli = get_redis_client()
    redis_key = 'shops_baseinfo:items'

    custom_settings = {
        'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
        'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
        'DUPEFILTER_DEBUG': True,
        'SCHEDULER_PERSIST': True,
        'SCHEDULER_QUEUE_CLASS': 'scrapy_redis.queue.PriorityQueue',
        # 队列用set结构
        'REDIS_START_URLS_AS_SET':True,
        # 'REDIS_HOST':'127.0.0.1',

        'ITEM_PIPELINES': {
            'tarantula.cp.dianping.shops_comments_pipelines.ShopsCommentsPipeline': 300,
        },
        'REDIS_ITEMS_KEY': '%(spider)s:items',

        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_TIMEOUT': 60,
        'DOWNLOADER_MIDDLEWARES': {
            'tarantula.cdm.XundailiProxy.ProxyMiddleware': 610,
            'tarantula.cdm.RandomUserAgent.UserAgentMiddleware': 560,
        },
        'DOWNLOAD_DELAY': 5,
        'SPIDER_MIDDLEWARES': {
            'tarantula.cm.scrapy_magicfields.MagicFieldsMiddleware': 100,
        },
    }


    def make_request_from_data(self, data):
        id = json.loads(data)['shopuuid']
        # pop出来的 店铺基础信息，插入到爬详情的请求队列
        self.redis_cli.sadd('shops_tuan:start_urls',data)
        url = self.api.format(id,id,id,id)
        return Request(url, meta={'id':id})

    def parse(self, response):
        self.logger.info(f"Parse Comments {response.url}")
        try:
            infos = json.loads(response.text)
            comments_list = infos['shopReviewInfo']['reviewList']
        except:
            self.logger.info('comments解析失敗：  ',response.text)
            return
        item = CommentItem()
        shop_id = response.meta['id']
        item['shop_id'] = shop_id
        item['comments_list'] = comments_list
        yield item