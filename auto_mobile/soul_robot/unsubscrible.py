import uiautomator2 as u2
import time
import os
import logging
from redis import Redis

redis_cli = Redis(host='118.31.66.50')


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Soul Monitor')


class Unsubscribe:
    """
    存在向下滑动无法加载的问题，增大单次滑动距离和增加滑动的频率可以解决
    存在取关误操作的现象，目前无解决方案
    """

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

    def unsubscribe_main(self):
        # start soul
        self.d.app_start('cn.soulapp.android')
        time.sleep(3)
        # 切到聊天页
        self.d.xpath('//*[@resource-id="cn.soulapp.android:id/lotMsg"]').click()
        time.sleep(0.5)
        # 切到关注页
        self.d.xpath('//*[@resource-id="cn.soulapp.android:id/ic_user_follow"]').click()
        time.sleep(0.5)
        # 切到我的关注
        self.d.xpath('//*[@text="我关注的"]').click()
        time.sleep(0.2)
        self.d.swipe(500, 1500, 500, 1000)
        while True:
            self.unscribe_list()



    def unscribe_list(self):
        """
        取关当前页
        """
        self.now_list_existence = False
        # 取关当前可视列表
        for i in range(0,7):
            result = self.unscribe_one(i)
            if result:
                break
        # 当前列表没有需要取关的，向下滑动
        if not self.now_list_existence:
            self.d.swipe(500, 1500, 500, 1000)
            time.sleep(0.2)




    def unscribe_one(self,i):
        """
        取关一个用户
        :param i: 列表页序号
        """
        name = self.d(resourceId="cn.soulapp.android:id/follow_sign", instance=i).get_text()
        existence = redis_cli.sismember('soul:white_list', name)
        if not existence:
            # 取关后 列表会自动上移
            self.d(resourceId="cn.soulapp.android:id/icon_follow", instance=i).click()
            logger.info(f'{name} 取关成功')
            time.sleep(0.8)
            self.now_list_existence = True
            return True
        else:
            self.d.swipe(500, 1500, 500, 1100)

    def get_my_fans_to_redis(self):
        """
        将粉丝加入白名单
        :return:
        """
        self.d.xpath('//*[@text="关注我的"]').click()
        while True:
            # 跳出循环，结束
            break_status = False
            for i in range(0,8):
                name = self.d(resourceId="cn.soulapp.android:id/follow_sign", instance=i).get_text()
                if i == 7:
                    if redis_cli.sismember('soul:white_list',name):
                        break_status = True
                        break
                redis_cli.sadd('soul:white_list',name)
                logger.info(f'我的粉丝 {name} 已经加入白名单')
            if break_status:
                logger.warning('粉丝白名单加入完毕')
                break
            self.d.swipe(500, 1500, 500, 1000)
            time.sleep(0.2)


if __name__ == '__main__':
    Unsubscribe().unsubscribe_main()

