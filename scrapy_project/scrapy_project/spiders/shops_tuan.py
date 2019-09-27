#!/usr/bin/env python
# encoding: utf-8
import json
from fake_useragent import UserAgent
import execjs
from lxml import etree
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from tarantula.util.redis import get_redis_client
from tarantula.items.dianping.tuan_items import TuanItem
from twisted.web.http_headers import Headers as TwistedHeaders

TwistedHeaders._caseMappings.update({
    b'sdkversion': b'sdkversion',
    b'channelversion': b'channelversion',
    b'minaname': b'minaname',
    b'minaversion': b'minaversion',
})

# UA 必须使用下面的(大概率是检测手机ua)

class ShopsBaseinfo(RedisSpider):
    """
    shops_baseinfo:items 保存店铺的id等信息   提供给评
    和点评详情来调用
    """

    name = 'shops_tuan'
    redis_key = 'shops_tuan:start_urls'

    # 团购促销 api
    api = 'https://m.dianping.com/wxmapi/shop/shoptuan?shopUuid={}&cityId={}'


    redis_cli = get_redis_client()

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
            'tarantula.cp.dianping.shops_tuan_pipelines.ShopsTuanPipeline': 300,
        },
        'REDIS_ITEMS_KEY': '%(spider)s:items',
        'REDIRECT_ENALBED':False,
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_TIMEOUT': 60,
        'DOWNLOADER_MIDDLEWARES': {
            'tarantula.cdm.XundailiProxy.ProxyMiddleware': 610,
            # 'tarantula.cdm.RandomUserAgent.UserAgentMiddleware': 560,
        },
        'DOWNLOAD_DELAY': 5,
        'SPIDER_MIDDLEWARES': {
            'tarantula.cm.scrapy_magicfields.MagicFieldsMiddleware': 100,
        },
    }


    def make_request_from_data(self, data):
        """
        微信小程序的接口，只要请求头对了即可
        """
        data = json.loads(data)
        shopuuid = data['shopuuid']
        city_id = data['city_id']
        headers = {
            "charset": "utf-8",
            "Accept-Encoding": "gzip",
            "referer": "https://servicewechat.com/wx734c1ad7b3562129/138/page-frame.html",
            "wechatversion": "7.0.6",
            "sdkversion": "2.8.3",
            "channelversion": "7.0.6",
            "minaname": "dianping-wxapp",
            "minaversion": "4.20.0",
            "channel": "weixin",
            "content-type": "application/json",
            "platformversion": "9",
            "platform": "Android",
            "User-Agent": "Mozilla/5.0 (Linux; Android 9; MI 8 Build/PKQ1.180729.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.132 Mobile Safari/537.36 MicroMessenger/7.0.6.1500(0x2700063D) Process/appbrand0 NetType/WIFI Language/zh_CN",
            "Host": "m.dianping.com",
            "Connection": "Keep-Alive"
        }

        url = self.api.format(shopuuid,city_id)
        # 推送给请求详情的爬虫
        self.redis_cli.sadd('shops_detail:start_urls',json.dumps(data))
        return Request(
            url=url,
            meta={'id':shopuuid},
            headers=headers,
        )

    def parse(self, response):
        shopuuid = response.meta['id']
        item = TuanItem()
        status = False
        self.logger.info(f"Parse shop_detail {response.url}")
        try:
            shopTuan = json.loads(response.text)['shopTuan']
        except:
            print(response.text)
            return
        if shopTuan:
            status = True
            for i in shopTuan:
                print(i)
        else:
            self.logger.info(f'该商铺没有团购信息    {response.url}')
        item['exist_status'] = status
        item['tuan_list'] = shopTuan
        item['shop_id'] = shopuuid
        yield item


