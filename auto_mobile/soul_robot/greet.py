import uiautomator2 as u2
import time
import os
import logging
from redis import Redis

redis_cli = Redis()


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Soul Monitor')


class Greet:

    def __init__(self):
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

    def test(self):
        self.d.click(0.323, 0.898)

    #
    # def open_soul(self):
    #     """
    #     打开ｓｏｕｌ广场
    #     """
    #     # start soul
    #     self.d.app_start('cn.soulapp.android')
    #     time.sleep(3)

    def greet(self,d,frame):
        frame.child(resourceId="cn.soulapp.android:id/headLayout", clickable=True).click()
        time.sleep(0.5)
        self.attent_greet(d)
        self.back_to_listpage(d)

    def just_greet(self):
        pass

    def attent_greet(self,d):
        # 关注
        d.click(0.323, 0.898)
        time.sleep(0.5)
        # 聊天
        d.click(0.565, 0.894)
        self.write_send_out(d)

    def write_send_out(self,d):

        try:
            # 发imoge
            time.sleep(1)
            d.click(0.144, 0.795)
        except:
            print('imog发不了')
        # 输入内容
        d(resourceId="cn.soulapp.android:id/et_sendmessage", clickable=True).send_keys('交朋友吗,交个朋友吧')
        # 发送
        d(resourceId="cn.soulapp.android:id/btn_send", clickable=True).click()
        logger.info('打招呼成功')

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
        # d(resourceId="com.android.systemui:id/back", clickable=True).click()
        # time.sleep(0.2)
        logger.info('回到主页')


if __name__ == '__main__':
    Greet().test()





