import time

from redis import Redis

class MoveRedis:
    def __init__(self):
        # 本地连接
        self.client_local = Redis()
        # 服务器连接
        self.client_taiyou = Redis(host='118.31.66.50')

    def search_set_push(self):
        """
        查询本地所有set结构的数据
        调用远程插入程序
        """
        keys_local = self.client_local.keys("*")
        for i in keys_local:
            key_type = self.client_local.type(i).decode()
            if key_type == 'set':
                datas = self.client_local.smembers(i.decode())
                self.push_set(i.decode(),datas)


    def soul_search_push(self):
        keys = ['soul','soul:nicknames','soul:white_list']
        for key in keys:
            datas = self.client_local.smembers(key)
            self.push_set(key, datas)

    def push_set(self,key,values):
        """
        将key value 备份到阿里云redis
        """
        for d in values:
            data = d.decode()
            self.client_taiyou.sadd(key,data)
            print(key,data)

    def listen_local_soul(self):
        while True:
            self.soul_search_push()
            time.sleep(10)



if __name__ == '__main__':
    MoveRedis().listen_local_soul()