from scrapy import Request,Spider
from twisted.web.http_headers import Headers as TwistedHeaders

TwistedHeaders._caseMappings.update({
    b'sdkversion': b'sdkversion',
    b'channelversion': b'channelversion',
    b'minaname': b'minaname',
    b'minaversion': b'minaversion',
})

class ShopsBaseinfo(Spider):
    name = 'test'

    api = 'https://m.dianping.com/wxmapi/shop/shoptuan?shopUuid={}&cityId={}'

    def start_requests(self):
        url = 'https://m.dianping.com/wxmapi/shop/shoptuan?shopUuid=93361578&cityId=1'
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
        yield Request(
            url=url,
            headers=headers,
            meta={
                'proxy':'http://127.0.0.1:8080'
            }
        )

    def parse(self, response):
        self.logger.info(f"Parse shop_detail {response.url}")
