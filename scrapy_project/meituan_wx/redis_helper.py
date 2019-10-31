# coding:utf-8
import redis

redisClient = redis.Redis(host="localhost", port=6379, db=1)


class RedisHelper(object):
    def __init__(self):
        pass

    def lpush_data(self, key, value):
        redisClient.sadd(key, value)

    def spop_data(self, keys):
        datas = redisClient.spop(keys)
        return datas

if __name__ == '__main__':
    RedisHelper = RedisHelper()
    # values = ('118,174012','24.778307',1)
    # RedisHelper.lpush_data("lgt_lat_page",values)
    RedisHelper.spop_data("lgt_lat_page")
