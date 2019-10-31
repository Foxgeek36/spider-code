#!/usr/bin/env python
# coding:utf-8
import logging
import os
from push_token_to_redis import CityTokenToRedis
from mysql_helper import MysqlHelper
from redis_helper import RedisHelper
from kafka_helper import Kafka
import time
import requests
import json
import sort_helper
import proxy_helper
import proxy_helper_copy
path = os.getcwd()
MysqlHelper = MysqlHelper()
count = 0


def request_url_response(url, method="GET", headers=None, params=None, proxy=None, data=None, verify=False):
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params, verify=False, proxies=proxy, timeout=20)
            return response
        else:
            response = requests.post(url, headers=headers, data=data, verify=False, proxies=proxy, timeout=20)
            time.sleep(3)
            return response
    except Exception as e:
        print("请求失败:%s" % e)
        return False
        pass


def get_new_token(redis_helper):
    """
    这个函数只是取请求相关参数
    :param page:
    :param params:
    :param location_point:
    :return:
    """
    try:
        param = redis_helper.spop_data("token_url_header")
        return param
    except Exception as e:
        print e


def get_shop_detail(redis_helper,page_index,param,location_point,count,flag):
    """
    获取列表页到详情页的数据
    :param page:
    :return:
    """
    wm_longitude_before = location_point[0].encode("utf-8")
    wm_latitude_before = location_point[1].encode('utf-8')
    wm_longitude = wm_longitude_before.replace('.', '')
    wm_latitude = wm_latitude_before.replace('.', '')
    print wm_longitude_before, wm_latitude_before, wm_longitude, wm_latitude
    page_index = int(page_index)
    print('当前页数为:%s'% page_index)
    # 列表页的url
    shop_list_url = param[0].encode('utf-8')
    # 请求头
    headers = json.loads(param[1])
    # 请求体
    data = json.loads(param[2])
    data['page_index'] = str(page_index)
    data['wm_longitude'] = str(wm_longitude)
    data["wm_latitude"] = str(wm_latitude)
    data['sort_type'] = '5'
    # data['wm_longitude'] = "121396406"
    # data["wm_latitude"] = "31169214"
    # 详情页的url
    shop_detail_url = shop_list_url.replace('v2/poi/channelpage', 'v1/poi/food')
    # 商家基本信息页面url:
    shop_base_info_url = shop_list_url.replace('v2/poi/channelpage', 'v1/poi/info')
    # 列表页的响应数据
    try:
        item = {}
        # proxy = proxy_helper.judge_ip()
        proxy = proxy_helper_copy.get_ip()
        print proxy
        response_list = ""
        for tmp in range(3):
            response_list = request_url_response(shop_list_url, method="POST", headers=headers, data=data, proxy=proxy, verify=False)
            print response_list
            if not response_list:
                proxy = proxy_helper_copy.get_ip()
                continue
            else:
                break
        if not response_list:
            # 请求失败怎么处理，返回False
            print ("请求失败记录token的爬取数量")
            MysqlHelper.update_params_count(count, shop_list_url)
            print("切换token值")
            param = get_new_token(redis_helper)
            if param != None:
                count = 0
                get_shop_detail(redis_helper, page_index, param, location_point, count, flag)
            else:
                keys = 'lgt_lat_page'
                values = (wm_latitude_before, wm_latitude_before, page_index)
                redis_helper.lpush_data(keys, values)
                return
        elif response_list.status_code == 200:
            json_data_list = json.loads(response_list.text)
            if not json_data_list.get('data'):
                # 记录token的访问数量
                MysqlHelper.update_params_count(count, shop_list_url)
                count = 0
                param = get_new_token(redis_helper)
                if param != None :
                    get_shop_detail(redis_helper, page_index, eval(param), location_point, count, flag)
                else:
                    print ('记录当前点的翻页数量')
                    MysqlHelper.update_location_state_page(wm_longitude_before, wm_latitude_before, page_index)
                    print ('token is null')
                    keys = 'lgt_lat_page'
                    values = (wm_latitude_before, wm_latitude_before, page_index)
                    redis_helper.lpush_data(keys, values)

                    return
            # 列表页的店铺数据
            else:
                response_list_datas = json.loads(response_list.text)['data']['poilist']
                # 判断列表页是不是为空列表，如果为空列表改变点的状态。
                if response_list_datas == []:
                    print ('list is None')
                    print ('该点的店铺数量为0，改变的状态')
                    MysqlHelper.update_location_state(wm_longitude_before, wm_latitude_before, page_index)
                    print('获取新的经纬度点')
                    location_point = redis_helper.spop_data('lgt_lat_page')
                    location_point = eval(location_point)
                    page_index = location_point[2]
                    get_shop_detail(redis_helper, page_index, param, location_point, count, flag)
                else:
                    get_detail_content(item, response_list, response_list_datas, data,param, shop_base_info_url, shop_detail_url, headers,location_point, count, shop_list_url, page_index, flag,wm_longitude_before,wm_latitude_before,proxy)
    except Exception as e:
        print e


def get_detail_content(item,response_list, response_list_datas, data,param, shop_base_info_url, shop_detail_url, headers,location_point,count,shop_list_url,page_index,flag,wm_longitude_before,wm_latitude_before,proxy):
    """
    处理详情页的数据
    :param response_list_datas:
    :return:
    """
    shop_distances_list = []
    for list_data in response_list_datas:
        # 获取距离
        distance = list_data['distance']
        name = list_data['name']
        print distance, name
        shop_distances_list.append(distance)
    if sort_helper.handle_sort_distace(shop_distances_list):
        print len(shop_distances_list)
        if len(shop_distances_list) == 20:
            count += len(shop_distances_list)
            print count
            for shop_data in response_list_datas:
                shop_name = shop_data['name']
                shop_id = shop_data['id']
                print shop_name, shop_id
                data['wm_poi_id'] = str(shop_id)
                data['wmpoiid'] = str(shop_id)
                # 发起详情页的请求
                detail_response = request_url_response(shop_detail_url, method="POST", headers=headers, data=data,proxy=proxy, verify=False)
                # 提取详情页的产品
                response_detail_data = json.loads(detail_response.text).get('data')
                # 发起商家基本信息请求
                time.sleep(3)
                base_info_response = request_url_response(shop_base_info_url, method="POST", headers=headers, data=data,proxy=proxy, verify=False)
                # 获取商家基本信息数据
                base_info_data = json.loads(base_info_response.text).get("data")
                item['shop_info'] = shop_data
                item['city'] = 'xiamenshi'
                item['base_info'] = base_info_data
                item['detail'] = response_detail_data
                kafka = Kafka()
                kafka.process_item(item)
            # 判断下一页的参数是否存在，如果存在继续访问下一页，如果不存在，切换点，data值不变
            print json.loads(response_list.text)['data']['poi_has_next_page']
            if json.loads(response_list.text)['data']['poi_has_next_page']:
                page_index += 1
                get_shop_detail(redis_helper, page_index, param, location_point, count, flag)
            else:
                # 下一页的参数为false,没有翻页数据，换点
                print ('没有翻页参数换点')
                location_point = redis_helper.spop_data('lgt_lat_page')
                location_point = eval(location_point)
                page_index = location_point[2].encode('utf-8')
                # 改变点的状态
                print ('改变点的状态')
                MysqlHelper.update_location_state(wm_longitude_before, wm_latitude_before, page_index)
                get_shop_detail(redis_helper, page_index, param, eval(location_point), count, flag)
        # 如果是升序，判断列表是不是小于20，如果小于20，判断距离是不是大于4公里，如果大于四公里，切换token值
        if len(response_list_datas) < 20:
            length = len(response_list_datas)
            count += length
            print count
            list = sort_helper.handle_sort_distace_2(shop_distances_list)
            for distance in list[0]:
                print distance
                if distance > 5000:
                    print ('该点的店铺数量小于20，升序，第一个点大于5000,经纬度的点，记录经纬度的翻页数量')
                    MysqlHelper.update_location_state_page(wm_longitude_before, wm_latitude_before, page_index)
                    print ('记录token的请求数量')
                    MysqlHelper.update_params_count(count, shop_list_url)
                    count = 0
                    param = get_new_token(redis_helper)
                    if param != None:
                        get_shop_detail(redis_helper, page_index, eval(param), location_point, count, flag)
                    else:
                        keys = 'lgt_lat_page'
                        values = (wm_latitude_before, wm_latitude_before, page_index)
                        redis_helper.lpush_data(keys, values)
                        return
                else:
                    for data in response_list_datas:
                        shop_name = data['name']
                        shop_id = data['id']
                        print shop_name, shop_id
                        data['wm_poi_id'] = str(shop_id)
                        data['wmpoiid'] = str(shop_id)
                        # 发起详情页的请求
                        detail_response = request_url_response(shop_detail_url, method="POST", headers=headers,data=data, verify=False)
                        # 提取详情页的产品
                        response_detail_data = json.loads(detail_response.text)['data']
                        # 发起商家基本信息请求
                        base_info_response = request_url_response(shop_base_info_url, method="POST", headers=headers,data=data,proxy=proxy, verify=False)
                        # 获取商家基本信息数据
                        base_info_data = json.loads(base_info_response.text)['data']
                        item['shop_info'] = data
                        item['city'] = 'xiamenshi'
                        item['base_info'] = base_info_data
                        item['detail'] = response_detail_data
                        # 设计一张表 id 自增 json: string creat_time update_time  is_detial
                        # 设计表两张表 一张店铺表  一张店铺中数据表
                        # id 店铺的名称 店铺的ID 经纬度 create_time update_time  is_detial
                        # 店铺详情表 ID shop_id (关联店铺的ID) 店铺的基本信息 create_time update_time  is_detial
                        kafka = Kafka()
                        kafka.process_item(item)
    else:
        # 记录token的请求个数
        # print len(shop_distances_list)
        # if json.loads(response_list.text)['data']['poi_has_next_page']:
        print ('该点不是升序，改变点的状态')
        MysqlHelper.update_location_state_page(wm_longitude_before, wm_latitude_before, page_index)
        print ('该点不是升序排序，切换token')
        for shop_data in response_list_datas:
            shop_name = shop_data['name']
            shop_id = shop_data['id']
            print shop_name, shop_id
            data['wm_poi_id'] = str(shop_id)
            data['wmpoiid'] = str(shop_id)
            # 发起详情页的请求
            detail_response = request_url_response(shop_detail_url, method="POST", headers=headers, data=data,verify=False)
            # 提取详情页的产品
            response_detail_data = json.loads(detail_response.text).get('data')
            # 发起商家基本信息请求
            base_info_response = request_url_response(shop_base_info_url, method="POST", headers=headers, data=data,verify=False)
            # 获取商家基本信息数据
            base_info_data = json.loads(base_info_response.text).get("data")
            item['shop_info'] = shop_data
            item['city'] = 'xiamenshi'
            item['base_info'] = base_info_data
            item['detail'] = response_detail_data
            kafka = Kafka()
            kafka.process_item(item)
        print ('切换token的值')
        MysqlHelper.update_params_count(count, shop_list_url)
        param = get_new_token(redis_helper)
        if param != None:
            count = 0
            get_shop_detail(redis_helper, page_index, eval(param), location_point, count, flag)
        else:
            keys = 'lgt_lat_page'
            values = (wm_latitude_before, wm_latitude_before, page_index)
            redis_helper.lpush_data(keys, values)
            return


if __name__ == '__main__':
    redis_helper = RedisHelper()
    param = redis_helper.spop_data("token_url_header")
    if param != None:
        location_point = redis_helper.spop_data('lgt_lat_page')
        location_point = eval(location_point)
        page_index =location_point[2].encode('utf-8')
        count = 0
        flag = 0
        get_shop_detail(redis_helper, page_index, eval(param), location_point, count, flag)





