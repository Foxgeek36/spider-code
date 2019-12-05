import uiautomator2 as u2
import time
import os
import logging
from redis import Redis

redis_cli = Redis(host='118.31.66.50')


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Soul Monitor')


class Greet:

    def __init__(self,content):
        """
        初始化鏈接指定的设备
        :param deviceid: 设备 device  ID
        """
        while True:
            try:
                self.d = u2.connect_usb('2244261a')
                break
            except:
                # 初始化uiautomator2 否则有可能连不上
                os.system('python -m uiautomator2 init')
        self.num = 0
        # 给最新的动态点赞
        self.lastest = False
        self.selectt_city = False
        self.content = content
        self.attent = False

    def test(self):
        self.d.click(0.323, 0.898)

    def greet(self,d,frame):
        frame.child(resourceId="cn.soulapp.android:id/headLayout", clickable=True).click(timeout=1)
        time.sleep(0.5)
        # 存在点进去之后弹框的情况
        try:
            if self.attent:
                self.just_greet(d)
            else:
                self.attent_greet(d)
        except:
            pass
        self.back_to_listpage(d)

    def just_greet(self,d):
        d.click(0.726, 0.9)
        self.write_send_out(d)

    def attent_greet(self,d):
        # 关注
        d.click(0.323, 0.898)
        time.sleep(0.5)
        # 聊天
        d.click(0.565, 0.894)
        self.write_send_out(d)

    def write_send_out(self,d):
        time.sleep(1)
        nick_name = self.black_list(d)
        if redis_cli.sismember('soul:nicknames', nick_name):
            return
        try:
            # 发imoge
            d.click(0.144, 0.795)
        except:
            print('imog发不了')
        # 输入内容
        d(resourceId="cn.soulapp.android:id/et_sendmessage", clickable=True).send_keys(self.content)
        # 发送
        d(resourceId="cn.soulapp.android:id/btn_send", clickable=True).click(timeout=1)
        logger.info('打招呼成功')
        redis_cli.sadd('soul:nicknames',nick_name)
        logger.info(f'昵称{nick_name} 已拉黑')

    def back_to_listpage(self,d):
        # 撤销键盘
        time.sleep(0.5)
        d.press("back")
        time.sleep(0.5)
        # 回到用户主页
        d.press("back")
        time.sleep(0.8)
        # 回到广场列表页
        d.press("back")
        d.app_start('cn.soulapp.android')
        time.sleep(1)
        logger.info('回到主页')

    def black_list(self,d):
        # 将打过招呼的人拉黑
        nick_name = d(resourceId="cn.soulapp.android:id/title").get_text(timeout=1)
        return nick_name




if __name__ == '__main__':
    Greet('ddd').test()





