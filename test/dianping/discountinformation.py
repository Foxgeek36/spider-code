from lxml import etree
import requests
import execjs


class DiscountInfo:
    def get_htmlcontent(self):
        """
        测试使用，从本地拿到Html
        :return: html dom
        """
        with open('大众点评优惠信息.html')as f:
            html = f.read().strip()
            html_dom = etree.HTML(html)
            return html_dom


    def product_cookies(self):
        """
        需要配置Nodejs环境
        :return: js生成的cookies
        """
        content = """
        function Gn() {
            return +new Date;
        };
        function Hr() {
            return Math.floor(1 + 65535 * Math.random()).toString(16).substring(1);
        };
        function findLongR() {
            return Gn().toString(16) + "-" + Hr() + "-" + Hr() + "-" + Hr();
        };
        """
        js = execjs.compile(content)
        _lxsdk_s = js.call('findLongR')
        return _lxsdk_s

    def request_htmlcontent(self):
        """
        携带cookies和请求头访问m 端拿到详情页数据
        :return: html source code dom tree
        """
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7",
            "Connection": "keep-alive",
            "Host": "m.dianping.com",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cookie":"_lxsdk_s={}".format(self.product_cookies()),
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36",
        }
        url = 'https://m.dianping.com/shop/131710927'
        response = requests.get(url,headers=headers)
        html_dom = etree.HTML(response.text)
        return html_dom

    def parse(self):
        """
        抽取优惠信息（团购）的详情页url，标题，销量，促销价格，原始价格
        :return: 所有优惠信息列表
        """
        html = self.request_htmlcontent()
        tuaninfos = html.xpath('//div[@class="tuan-list"]/a')
        tuaninfos_list = []
        for tuan in tuaninfos:
            tuan_detail_url = tuan.xpath('./@href')[0]
            tuan_title = tuan.xpath('.//div[@class="newtitle"]/text()')[0]
            sales_num = tuan.xpath('.//span[@class="soldNumNew"]/text()')[0]
            low_price = tuan.xpath('.//div[@class="symbol"]/following::div[1]/text()')[0]
            low_price_money_tag = tuan.xpath('.//div[@class="symbol"]/text()')[0]
            high_price = tuan.xpath('.//div[@class="symbol2"]/following::div[1]/text()')[0]
            high_price_money_tag = tuan.xpath('.//div[@class="symbol2"]/text()')[0]
            tuaninfo = {
                'tuan_detail_url':tuan_detail_url,
                'tuan_title':tuan_title,
                'sales_num':sales_num,
                'low_price':low_price,
                'low_price_money_tag':low_price_money_tag,
                'high_price':high_price,
                'high_price_money_tag':high_price_money_tag,
            }
            tuaninfos_list.append(tuaninfo)
        return tuaninfos_list

if __name__ == '__main__':
    discount_info = DiscountInfo()
    tuaninfos = discount_info.parse()
    print(tuaninfos)






