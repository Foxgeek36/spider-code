import itchat, time
from itchat.content import *
import requests
from lxml import etree
from redis import StrictRedis
from threading import Thread


"""
实现功能:
    1. 退订处理加回复
    2. 新消息6小时以上自动回复(首次收到立即回复)
    3. 每隔24小时推送一次当前舆论热点排行版(前五名)
    4. 支持退订,退订好友,加入黑名单以后不会再发(默认全员发送)
    
"""


# redis_cli = StrictRedis(host='192.168.1.191')
redis_cli = StrictRedis(host='192.168.43.105')


class SendNews:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }
    # itchat.auto_login(True)
    target_users = ['change', '华灯初上']

    def getUsername(self):
        users = itchat.get_friends(update=True)
        for user in users:
            if user['NickName'] in self.target_users:
                if not redis_cli.sismember('blacklist', user['NickName']):
                    print(user)
                    yield user['UserName']

    def getUsernameAll(self):
        """
        给所有人(不包含黑名单)群发
        :return:
        """
        users = itchat.get_friends(update=True)
        for user in users:
            if not redis_cli.sismember('blacklist', user['NickName']):
                yield user['UserName']

    def sendnews(self):
        """
        爬取新闻推送到微信
        :return:
        """

        url = "https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word=AI"
        for i in ['AI', '人工智能']:
            newurl = url.format(i)

            html = requests.get(newurl, headers=self.headers).text
            tree = etree.HTML(html)
            patterns = tree.xpath('//h3/a')
            allnews = ''
            for pattern in patterns:
                detailurl = pattern.xpath('./@href')[0]
                title = pattern.xpath('string(.)').strip()
                allnews += ("{}  {}\n\n".format(title, detailurl))
            for touser in self.getUsername():
                itchat.send(allnews, toUserName=touser)

    def sendweiredian(self):
        formdata = {
            "timeType": 1,
            "sort": 5,
            "labels": "",
            "province": "",
            "areaType": 1,
            "page": 1,
            "pageSize": 20,
            "city": "",
            "isLogin": False
        }

        sinaweiredianurl = 'http://www.wrd.cn/view/home/hotEvent/selectChooseListData.action'
        result = requests.post(sinaweiredianurl, data=formdata, headers=self.headers).json()['list']
        # print(result)
        num = 0
        weinews = ""
        for i in result:
            if num < 5:
                num += 1
                content = "\t".join([str(num), i['incidentTitle'], i['keyword']]) + '\n\n'
                weinews += content
        # itchat.send(weinews, toUserName='@6e6512bff85fb8b2c1f4bd14ea48d8ec7a0a74a48c7f74e6856b498a6f329584')
        title = '\t' * 17 + "今日舆情飙升榜\n\n\n"
        tuiding_content = '\n' + '\t'*10 + '如您不需此推送回复"退订"哦'
        weinews = title + weinews + tuiding_content
        for touser in self.getUsernameAll():
            itchat.send(weinews, toUserName=touser)
            print('{} 发送成功'.format(touser))

    def main(self):
        # 每隔24小时推送一次
        while True:
            now = time.strftime("%H")
            # if now == '07':
            #     self.sendnews()
            # else:
            #     self.sendweiredian()
            self.sendnews()
            self.sendweiredian()
            time.sleep(60 * 60 * 24)





@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    # print(msg.user)
    print('您有来自{}的新消息'.format(msg.user['NickName']))
    # print(msg.text)
    if '退订' in msg.text:
        redis_cli.sadd('blacklist',msg.user['NickName'])
        msg.user.send('OK')
    else:
        # 6小时以上的消息自动回复,以内不予响应
        exist = redis_cli.get(msg.user['NickName'])
        if not exist:
            msg.user.send('您好！在忙，待会回您哦 > _ <')
            redis_cli.set(msg.user['NickName'], int(time.time()))
            print('保存成功{}'.format(msg.user['NickName']))
        else:
            oldtime = int(exist.decode())
            TimeDifference = time.time() - oldtime
            if TimeDifference > 60 * 60 * 6:
                msg.user.send('您好！在忙，待会回您哦 > _ <')
                # redis_cli.set(msg.user['NickName'], time.time())
                redis_cli.set(msg.user['NickName'], int(time.time()))
                print('保存成功{}'.format(msg.user['NickName']))
            else:
                print('未满足6小时,6小时以上再回复')


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    """
    下载文件
    :param msg:
    :return:
    """
    # msg.download(msg.fileName)

    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    print('{} 给你发送到了文件 名称: {} 类型: {}'.format(msg.user['NickName'],msg.fileName,typeSymbol))
    # return '@%s@%s' % (typeSymbol, msg.fileName)

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    """
    接受好友请求
    :param msg:
    :return:
    """
    msg.user.verify()
    msg.user.send('Nice to meet you!')

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    """
    回复群@
    :param msg:
    :return:
    """
    if msg.isAt:
        msg.user.send(u'@%s\u2005I received: %s' % (
            msg.actualNickName, msg.text))

itchat.auto_login(True)

def reply_messages():
    itchat.run(True)

def send_messages():
    sendm = SendNews()
    sendm.main()


if __name__ == '__main__':
    t1 = Thread(target=reply_messages)
    t2 = Thread(target=send_messages)
    for t in [t1,t2]:
        t.start()

