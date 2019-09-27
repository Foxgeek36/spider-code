import pymysql
import os
import json
from copy import deepcopy

class DataMachine:
    def __init__(self):
        self.connect = pymysql.connect(
            host='172.102.2.150',
            user='app',
            password='wechat0717',
            database='fosun_spider',
            charset='utf8'
        )
        self.cursor = self.connect.cursor()
        # self.cursor.execute()

    def get_catgorys_insert(self):
        path = '/home/dragon/Documents/mycodes/spider-code/test/dianping/region/'
        files = os.listdir(path)
        for file in files:
            with open(path+file)as f:
                data = json.loads(f.read())
                catgory = data['category']
                newcatgory = self.remove_one_categroy(catgory)
                self.insert_catgory(newcatgory)

    def get_categ_region_metro_insert(self):
        path = '/home/dragon/Documents/mycodes/spider-code/test/dianping/region/'
        files = os.listdir(path)
        for file in files:
            with open(path + file)as f:
                data = json.loads(f.read())
                region = data['region']
                metro = data['metro']
                self.insert_region(file,region)
                self.insert_metro(file,metro)

    def insert_metro(self,file,metro):
        cityid = file.replace('.json','')
        cityid = int(cityid)
        sql = "insert into dp_meta(real_id,city_id,type,pid,name,create_time,update_time) values"
        values = "({},{},1,{},'{}',now(),now()),"
        num = 0
        if not metro:
            return
        for i in metro:
            id = i['id']
            value_format = values.format(id,cityid,i['parentId'],i['name'])
            sql += value_format
            num += 1
        sql = sql[:-1] + ';'
        print(f"{num} 条数据")
        # print(sql)
        self.cursor.execute(sql)
        self.connect.commit()


    def insert_region(self,file,region):
        cityid = file.replace('.json','')
        cityid = int(cityid)
        sql = "insert into dp_meta(real_id,city_id,type,pid,name,create_time,update_time) values"
        values = "({},{},0,{},'{}',now(),now()),"
        num = 0
        if not region:
            return
        for i in region:
            id = i['id']
            if id > 0 and '全部' not in i['name']:
                value_format = values.format(id,cityid,cityid,i['name'])
                sql += value_format
                num += 1
        if num == 0:
            return
        sql = sql[:-1] + ';'
        print(f"{num} 条数据")
        self.cursor.execute(sql)
        self.connect.commit()

    def get_citys_insert(self):
        with open('/home/dragon/Documents/mycodes/spider-code/test/dianping/大众点评全国城市id.txt')as f:
            content = f.read().strip()
            citys = eval(content)
            self.insert_city(citys)


    def insert_city(self,citys):
        sql = "insert ignore into dp_city(id,name,create_time) values"
        values = "({},'{}',now()),"
        num = 0
        for city in citys:
            cityId = city['cityId']
            cityName = city['cityName']
            value_format = values.format(cityId,cityName)
            sql += value_format
            num += 1
        sql = sql[:-1] + ';'
        print(f"{num} 条数据")
        self.cursor.execute(sql)
        self.connect.commit()


    def update_citys_table(self):
        path = '/home/dragon/Documents/mycodes/spider-code/test/dianping/region/'
        files = os.listdir(path)
        filenames = []
        for file in files:
            file = file.replace('.json','')
            filenames.append(int(file))
        filenames = sorted(filenames)
        print(len(filenames),filenames)
        sql = "select id from dp_city;"
        self.cursor.execute(sql)
        ids = self.cursor.fetchall()
        print(ids)
        delsql = "delete from dp_city where id={};"
        for i in ids:
            id = i[0]
            if id not in filenames:
                sql = delsql.format(id)
                self.cursor.execute(sql)
        self.connect.commit()
        print('exe ok')

    def get_dif(self):
        path = '/home/dragon/Documents/mycodes/spider-code/test/dianping/region/'
        files = os.listdir(path)
        filenames = []
        for file in files:
            file = file.replace('.json', '')
            filenames.append(int(file))
        filenames = sorted(filenames)
        sql = "select * from dp_city;"
        self.cursor.execute(sql)
        ids = self.cursor.fetchall()
        dif = []
        for i in ids:
            id = i[0]
            if id not in filenames:
               dif.append([id,i[1]])
        print(len(dif),dif)

    def insert_catgory(self,categorys):
        sql = "insert ignore into dp_category(id,pid,name,level,create_time) values"
        num = 0
        if not categorys:
            return
        for category in categorys:
            values = "({},{},'{}',2,now()),"
            id = category['id']
            pid = category['parentId']
            if pid == id:
                values = "({},{},'{}',1,now()),"
                pid = 0
            name = category['name']
            value_format = values.format(id,pid,name)
            sql += value_format
            num += 1
        sql = sql[:-1]+';'
        print(f"{num} 条数据")
        # print(sql)
        self.cursor.execute(sql)
        self.connect.commit()



    def remove_one_categroy(self,data):
        datacopy = deepcopy(data)
        newdata = []
        for d in data:
            # if d['parentId'] == 0 and '全部' not in d['name']:
            #     datacopy.remove(d)
            if '全部' in d['name'] and '全部分类' not in d['name']:
                # datacopy.remove(d)
                d['name'] = d['name'].replace('全部','')
                newdata.append(d)
                # datacopy.append(d)
        # return datacopy
        return newdata

    def removeattr(self,data):
        newdata = []
        for i in data:
            i.pop('count')
            i.pop('distance')
            i.pop('favIcon')
            i.pop('sortId')
            newdata.append(i)
        print(newdata)
        return newdata



if __name__ == '__main__':
    datamachine = DataMachine().get_categ_region_metro_insert()