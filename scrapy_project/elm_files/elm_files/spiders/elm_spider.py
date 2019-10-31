# -*- coding: utf-8 -*-
import re
import scrapy
from __future__ import unicode_literals
from urlparse import *
import time
import json
import logging
from scrapy.utils.log import configure_logging
import scrapy


class ElmSpidersSpider(scrapy.Spider):
    name = 'elm_spiders'
    allowed_domains = ['h5.ele.me']
    start_urls = ['https://h5.ele.me/restapi/shopping/v2/restaurant/category?latitude=31.169905&longitude=121.395958']

    # url or url format used in this spider
    # restaurantListFormatUrl = 'https://h5.ele.me/restapi/shopping/v3/restaurants?latitude={0}&longitude={1}&offset={2}'
    # restaurant_list_url = 'https://h5.ele.me/restapi/shopping/v3/restaurants?latitude=31.272856&longitude=121.528798&offset=30&limit=30'
    # offset从0开始
    restaurant_list_url = 'https://h5.ele.me/restapi/shopping/v3/restaurants?latitude={}&longitude={}&offset={}&limit=30'


    restaurantDetailFormatUrl = 'https://h5.ele.me/pizza/shopping/restaurants/{0}/batch_shop?extras=%5B%22activities%22%2C%22albums%22%2C%22license%22%2C%22identification%22%2C%22qualification%22%5D'


    restaurantCommentsFormatUrl = 'https://h5.ele.me/pizza/ugc/restaurants/{0}/batch_comments?has_content=true&offset={1}&limit=180'
    restaurantRatingsFormatUrl = 'https://h5.ele.me/restapi/ugc/v3/restaurants/{0}/ratings?has_content=true&offset={1}&limit=180'
    headers = {
        "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        'referer': 'https://h5.ele.me/msite/food/',
        'x-uab':'121#yZmlkPXAVaQlVl2DxVhyllXYOa5RSujVs/gyHiyzwwRqXmrJbZEVBkwUAcfdK5j9lGgY+zp5KM9lOQrnqkDIlw9mOcMpgzjVlwgy+aPIpMmSTQrJEmD5lwLYAcfdD5jVVmgY+zP5KMlVA3rnEkD5bwLYOcMyFErtXQQVBIbvsbc9MtFPD0rOXYVbbZsdofpwpCibkZ0T83Smbgi0CeIaF960C6sDnjx9plX0CQZUM3BmC6JbCeHAFdMlC6ibnnC9pCibCZ0483B1bgi0CNIaFtFbbZsbnjGDpCD0Tqr/FmBmkJ01OWP9PofmyPi0IGhCAC94C6748u/m4lqLLHqwt5o2FJqFV09nWuLmFDuYdyn3lGd7vQSDb5CbiyJMAeBPELwUUJKE+DCVmKbSfBfEMW523aoLsMmnOnfvG85sST+G6uwhrxd4kWqcPvF6BBKfOG96B2lel+IlRseM6tPM1lZjZy/gzV+bNNNn00LB9SprAAcadFzp+jaLkigVQx+lJsUim/3JboxM/hjVEn5eSKXteZYDSFIrAcOgVx3NIPRJj6Aslnu0NptESzUxeMcRHNteRuuVCnvE1ZgT6jwE+1MB39r5Ww2zv/ScD4Kf6eMjSLV5hlz4PtsMbzaEtLJha3mLB6GKvaIh1sRTPYRiv/WB0xJtorGyMzhXTg4krlGKPvzucRTjHL0WmsAzTNvZ2Fk2o2A780lEHmIjIEAQMiQwCpV0w6mt6iCZ9MoauPfkhwot0cFXKZ8452yZOLK8JieBQOG4484dxQA04IA2RdVR6EXyD0cMvgtDTGSeDW1vL4fPsvOv+5zkU7+mDDwPD1m8VihAKwvxtKoRXg6eeoWWAzhMNzfveks7jWPrhUiFQ23+79gTNPB3E0PYtBm0zCXHhzZqZctJ6fhKKdqLEnw3KcqXbtoAkadNaJ2TeKzou2epcojw7f1UiDRwqOaEcrgCispoq3z+SvBdRBpjWv1Q2i6E+OXtFgTNUfrtRjTbRLVU4YokqzAx6EyE+lWj2g2LAI76XKj6K6OFxxTtUuhf8rqlEGjC6EroMctOSwLqSXV+f/vcg2H57dxvt1obr4xvZ0ChPsDuUl4/TDJDIzBeRZwYJiLv76dkxs05fGJYD1AqOGzZj1Vy1iUQBYVYSsBW+WAy4kPztRwPcwvMRK+J9gXHCFdInHpDI1hUuv73+QbwiIEZnBG44aX+rXTxybNfG8bMF2mqSADQ8RGd52G3aqN0Sb2WmFXXoRg5K1EAWN2XfgxaccOFtX8hObyANGdwRq2Df1VQNCpmNsiqoCmqx0thr84djT5wjb/KuRC4LHltY0cwqVjnNYhv+rUbmXFOUptXd5yC6c0l9mqYHyRqemccf5t='
    }

    cookies = {'UTUSER': '2000015383396', 'ut_ubt_ssid': '54ogwp73xed2nucrxwr7jl88y62j7vp5_2019-10-12', 'perf_ssid': '8bpfnwd93he89jkergefeb0oyz0i65gd_2019-08-15', 'isg': 'BEBAKgwHCaLT6PT5cpywocGBEc6-2ex2C8fiErrRDtvuNeRffdhdIRYHSftQhdxr', 'ubt_ssid': 'c70cp9mh0h8cirmpcyj40c342jruhv7k_2019-08-12', 'USERID': '2000015383396', '_bl_uid': 'agj90z8U8jzaCXc9tgvvfIsynOIh', 'ZDS': '1.0|1570874723|qdz1118RJ9hhzp2QFq63h7u6btCAYTrpn+O109IngV1VQPFloOT/wiAGq3j7kdWSW2QaczKBf8wm6c3QJP8yWA==', 'l': 'dB_hQoZuq2Y7XYM1BOCg5QKfZybOYIRAguSJG4D6i_5Cp6T6_HWOkigSEF96cjWftv8B4kYN3dw9-etl9KAzfGBdmW2KixDc.', 'pizza-rc-ca': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzEwMzMyNjUsInNhbHQxIjoiNzM2MGM2NzEzZmE2OGRmMTg5ZDZkZjM3NGYzZWMwNjUiLCJzYWx0MiI6IjEwZjI3Yjk4ZjdiMjhmNWRiZTY4YWIxZmVmNDEzMDhiIn0.IHIoTwloQ5o9UeuTut_qDOhUatS3KA8UgU1qFsdKljA', 'pizza73686f7070696e67': 'T6SMZdWdrIV-C79-irYz0cxzCAbhtH_-i9DgcggiKKafCNBvmklXQLVsI9K9DEzm', 'tzyy': '8ff093b69a6d3d1c29855356e7819a09', 'cna': 'tjTYFTlh6TcCAdz4DY4MEF4X', 'SID': 'gElsX0F3vpsg2aeYGixJAdBYWi9PlMJtEpaA', 'pizza-rc-ca-result': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbGciOiJIUzI1NiIsImV4cCI6MTU3MTAzNTAwNiwic2FsdDEiOiI3MzYwYzY3MTNmYTY4ZGYxODlkNmRmMzc0ZjNlYzA2NSIsInNhbHQyIjoiMTBmMjdiOThmN2IyOGY1ZGJlNjhhYjFmZWY0MTMwOGIifQ.lqIiUREoQJk54qKSG-CRsNO3aky8ayqB3t3RaWkUQCY', 'track_id': '1570874723|9a5d8acdcdf580bfdc14e4fc5cb9937a502bf39d066280d7ca|2ae7fae5766e3a4c74ad899574b1eec6', '_utrace': 'eed0003064ed381853c32e61c534d056_2019-08-12'}

    def parse(self, response):
        # Category_Item = CategoryItem()
        Category_Item = {}
        jsondata = json.loads(response.text)

        parsed = urlparse(response.url)
        params = parse_qs(parsed.query)
        latitude, = params['latitude']
        longitude, = params['longitude']

        Category_Item['all_count'] = jsondata[0]['count']
        Category_Item['all_name'] = jsondata[0]['name']
        first_category_ids = jsondata[0]['ids']

        first_name_id_count_s = []
        second_list = []
        second_id_list=[]

        for num1, first_category_id in enumerate(first_category_ids):
            first_dic = {}
            second_name_id_count_s = []

            first_name_id_count = [jsondata[num1 + 1]['name'], first_category_id, jsondata[num1 + 1]['count']]
            first_name_id_count_s.append(first_name_id_count)

            for x in jsondata[num1 + 1]['sub_categories'][1:]:
                second_name_id_count = [x['name'], x['id'], x['count']]
                second_name_id_count_s.append(second_name_id_count)
                second_id_list.append(x['id'])

            first_dic[first_category_id] = second_name_id_count_s
            second_list.append(first_dic)

        Category_Item['first_category_name_id_count_s'] = first_name_id_count_s
        Category_Item['firstID_map_second_category_all'] = second_list
        yield Category_Item
        separator = ''
        if len(second_id_list):
            num = len(second_id_list) // 30
            if num > 0:
                for i in range(num):
                    second_category_ids = []
                    url_1 = []
                    for x in second_id_list[:30]:

                        url_1.append('&restaurant_category_ids[]=%s' % x)
                        second_category_ids.append(x)
                        second_id_list.remove(x)
                    full_url = self.restaurantListFormatUrl.format(latitude, longitude, 0) + separator.join(url_1)
                    yield scrapy.Request(url=full_url, method='GET',
                                         callback=self.parseRestaurantList,
                                         meta={'second_category_ids': second_category_ids})

                if len(second_id_list):
                    second_category_ids = []
                    url_1 = []
                    for x in second_id_list[:30]:
                        url_1.append('&restaurant_category_ids[]=%s' % x)
                        second_category_ids.append(x)
                        second_id_list.remove(x)
                    full_url = self.restaurantListFormatUrl.format(latitude, longitude, 0) + separator.join(url_1)

                    yield scrapy.Request(url=full_url, method='GET',
                                         callback=self.parseRestaurantList,cookies=self.cookies,headers=self.headers,
                                         meta={'second_category_ids': second_category_ids})
            else:
                second_category_ids = []
                url_1 = []
                for x in second_id_list[:30]:
                    url_1.append('&restaurant_category_ids[]=%s' % x)
                    second_category_ids.append(x)
                    second_id_list.remove(x)
                full_url = self.restaurantListFormatUrl.format(latitude, longitude, 0) + separator.join(url_1)

                yield scrapy.Request(url=full_url, method='GET',
                                     callback=self.parseRestaurantList,cookies=self.cookies,headers=self.headers,
                                     meta={'second_category_ids': second_category_ids})

    def parseRestaurantList(self, response):
        # do stuff



        second_category_ids = response.meta['second_category_ids']
        jsondata = json.loads(response.text)
        print 'parseRestaurantList'
        for restaurant_data in jsondata['items']:
            restaurantId = restaurant_data['restaurant']['id']
            yield scrapy.Request(url=self.restaurantDetailFormatUrl.format(restaurantId), method='GET',cookies=self.cookies,headers=self.headers,
                                 callback=self.parseRestaurantDetail, meta={'restaurantId': restaurantId})
            # yield scrapy.Request(url = self.restaurantCommentsFormatUrl.format(restaurantId, 0), method = 'GET', callback = self.parseRestaurantComments,cookies=self.cookies,headers=self.headers, meta={'restaurantId':restaurantId})

            if (jsondata['has_next']):
                url_base = ''
                parsed = urlparse(response.url)
                params = parse_qs(parsed.query)
                latitude, = params['latitude']
                longitude, = params['longitude']
                offsetStr, = params['offset']
                offset = int(offsetStr)
                offset += 30
                self.logger.info('offset is ' + bytes(offset))
                separator = ''
                url_1 = []

                for id in second_category_ids:
                    url_1.append('&restaurant_category_ids[]=%s' % id)

                urlLocal = self.restaurantListFormatUrl.format(latitude, longitude, offset) + separator.join(url_1)
                yield scrapy.Request(url=urlLocal, method='GET',cookies=self.cookies,headers=self.headers)

    def parseRestaurantDetail(self, response):
        # item = RestaurantItem()
        item = {}
        print 'parseRestaurantDetail'
        matchObj = re.match(r'.*restaurants/(.*?)/.*', response.url, re.M | re.I)
        restaurantId = matchObj.group(1)

        responseData = json.loads(response.body)
        item['restaurantId'] = restaurantId
        item['menu'] = responseData['menu']
        item['recommend'] = responseData['recommend']
        item['redpack'] = responseData['redpack']
        item['rst'] = responseData['rst']
        if (len(responseData['rst']['flavors']) >= 1):
            item['rst_first_category'] = responseData['rst']['flavors'][0]['name']

        if (len(responseData['rst']['flavors']) >= 2):
            item['rst_second_category'] = responseData['rst']['flavors'][1]['name']
        yield item

    def parseRestaurantComments(self, response):
        # item = BatchCommentItem()
        item = {}
        print 'parseRestaurantComments'
        matchObj = re.match(r'.*restaurants/(.*?)/.*', response.url, re.M | re.I)
        restaurantId = matchObj.group(1)

        responseData = json.loads(response.body)
        item['restaurantId'] = restaurantId
        item['comments'] = responseData['comments']
        item['rating'] = responseData['rating']
        item['tags'] = responseData['tags']
        yield item

        totalCommentCount = 180
        for tag in responseData['tags']:
            if (tag['name'] == '全部'):
                totalCommentCount = tag['count']
                break

        i = 180
        while i < totalCommentCount:
            yield scrapy.Request(url=self.restaurantRatingsFormatUrl.format(response.meta['restaurantId'], i),
                                 method='GET', callback=self.parseRatings,
                                 meta={'restaurantId': response.meta['restaurantId']},cookies=self.cookies,headers=self.headers)
            i += 180

    def parseRatings(self, response):
        # item = CommentItem()
        item = {}
        print 'parseRatings'
        responseData = json.loads(response.body)
        item['restaurantId'] = response.meta['restaurantId']
        item['comments'] = responseData
        yield item

    def logListFailureMsg(self, msg):
        # list failure logger
        listFailureLogger = logging.getLogger('listFailureLogger')
        listFailureLogger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('listFailure.log', mode='a', encoding=None, delay=False)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        listFailureLogger.addHandler(fh)
        listFailureLogger.info(msg)
        listFailureLogger.removeHandler(fh)

    def logDetailFailureMsg(self, msg):
        detailFailureLogger = logging.getLogger('detailFailureLogger')
        detailFailureLogger.setLevel(logging.DEBUG)
        fh2 = logging.FileHandler('detailFailure.log', mode='a', encoding=None, delay=False)
        fh2.setLevel(logging.DEBUG)
        fh2.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        detailFailureLogger.addHandler(fh2)
        detailFailureLogger.info(msg)
        detailFailureLogger.removeHandler(fh2)

    def logCommentFailureMsg(self, msg):
        commentFailureLogger = logging.getLogger('commentFailureLogger')
        commentFailureLogger.setLevel(logging.DEBUG)
        fh3 = logging.FileHandler('commentFailure.log', mode='a', encoding=None, delay=False)
        fh3.setLevel(logging.DEBUG)
        fh3.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        commentFailureLogger.addHandler(fh3)
        commentFailureLogger.info(msg)
        commentFailureLogger.removeHandler(fh3)
