import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText
import requests
from lxml import etree
from redis import Redis
from hashlib import md5
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('TaiYou Monitor')


class Spider:
    def __init__(self):
        self.redis_cli = Redis()
        self.logger = logger
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Mobile Safari/537.36'
        }
        with open('urls.txt')as f:
            content = f.read().strip()
            urls = content.split('\n')
            for url in urls:
                if url:
                    self.redis_cli.sadd('taiyou',url)
        self.logger.info('开始监控')

    def request(self,url):
        try:
            response = requests.get(url,headers=self.headers)
        except:
            return ''
        tree = etree.HTML(response.text)
        patterns = tree.xpath('//div[@class="video-list"]/a[@class="videolink"]')
        new_videos = "\n\n"
        videos_list = []
        for pattern in patterns:
            href = pattern.xpath('./@href')[0]
            # if 'http://toutiao.com/preview_article/?pgc_id=6733889782235005447?app=video_article&;scheme=snssdk141%3A%2F%2Fdetail%3Fgroupid%3D6733889782235005447'
            if 'preview_article' in href:
                id = re.findall('pgc_id=(\d+)\?app=video_article',href)[0]
                href = f'http://toutiao.com/group/{id}'
            title = pattern.xpath('.//p[@class="title"]/text()')[0]
            content = "\n".join([title,href])
            uuid = md5(content.encode()).hexdigest()
            if not self.redis_cli.sismember('taiyouuuids',uuid):
                self.redis_cli.sadd('taiyouuuids',uuid)
                videos_list.append(content)
                # print(content)
        # print(videos_list)
        result = new_videos.join(videos_list)
        # print(new_videos)
        return result

    def send_email_from126(self,text):
        new_time = time.strftime("%Y-%m-%d-%H:%M:%S")
        sender = 'shixiaolongfw@126.com'  # 你发送邮箱的账号
        receivers = '208720471@qq.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

        message = MIMEText("""你好当前时间{}更新内容如下：\n\n{}""".format(new_time, text))
        message['From'] = "{}项目".format('太友短视频监控服务')
        message['To'] = f"{receivers}"
        # 标题
        subject = '视频有更新'
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect("smtp.126.com", 25)  # 25 为 SMTP 端口号
            smtpObj.login(sender, "shixiaolong22")
            smtpObj.sendmail(sender, receivers.split(','), message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print("Error: 无法发送邮件", e)


    def send_email_fromqq(self,text):

        # qszrtdadogxtbbge
        new_time = time.strftime("%Y-%m-%d-%H:%M:%S")
        sender = '654921690@qq.com'  # 你发送邮箱的账号
        receivers = '208720471@qq.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

        message = MIMEText("""你好当前时间{}更新内容如下：\n\n{}""".format(new_time, text))
        message['From'] = "{}项目".format('太友短视频监控服务')
        message['To'] = f"{receivers}"
        # 标题
        subject = '视频有更新'
        message['Subject'] = Header(subject, 'utf-8')
        try:
            # smtpObj = smtplib.SMTP()
            # smtpObj = smtplib.SMT
            # smtpObj.connect("smtp.qq.com", 465)  # 25 为 SMTP 端口号
            # smtpObj.login(sender, "747474ni")
            # smtpObj.login(sender, "vxtljavfoougbcej")
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(sender, 'qszrtdadogxtbbge')
            s.sendmail(sender, receivers.split(','), message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print("Error: 无法发送邮件", e)

    def send_email_from163(self, text):
        new_time = time.strftime("%Y-%m-%d-%H:%M:%S")
        sender = 'shixiaolongfw@163.com'  # 你发送邮箱的账号
        receivers = '208720471@qq.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

        message = MIMEText("""你好当前时间{}更新内容如下：\n\n{}""".format(new_time, text))
        message['From'] = "{}项目".format('太友短视频监控服务')
        message['To'] = f"{receivers}"
        # 标题
        subject = '视频有更新'
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect("smtp.163.com", 25)  # 25 为 SMTP 端口号
            smtpObj.login(sender, "shixiaolong22")
            smtpObj.sendmail(sender, receivers.split(','), message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print("Error: 无法发送邮件", e)

    def main(self):
        """
        每60s小时更新一次
        :return:
        """
        try:
            num = 0
            self.now = 0
            while True:
                if time.time() > self.now + 60:
                    num += 1
                    self.request_all_authors()
                    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    print('第{}次更新完,当前时间是{}'.format(num, now))
                    self.now = time.time()
        except Exception as e:
            print(e, '项目刷新失败')

    def request_all_authors(self):
        urls = self.redis_cli.smembers('taiyou')
        all_authors_videos = "\n\n"
        videos_list = []
        for url in urls:
            url = url.decode()
            new_videos = self.request(url)
            time.sleep(2)
            if new_videos.strip():
                videos_list.append(new_videos)
        result = all_authors_videos.join(videos_list)
        if result.strip():
            self.send_email_fromqq(result)
        else:
            self.logger.info('当前无更新')
            print('当前无更新')


if __name__ == '__main__':
    Spider().main()

