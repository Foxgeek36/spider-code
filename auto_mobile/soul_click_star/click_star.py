import uiautomator2 as u2
import time
import os
from redis import Redis
redis_cli = Redis()




class TianGou:
    """
    soul click star
    """

    def __init__(self,deviceid):
        """
        初始化鏈接指定的设备
        :param deviceid: 设备 device  ID
        """
        while True:
            try:
                self.d = u2.connect_usb(deviceid)
                break
            except:
                # 初始化uiautomator2 否则有可能连不上
                os.system('python -m uiautomator2 init')
        self.num = 0

    def open_soul(self):
        """
        打开ｓｏｕｌ广场
        """
        # start soul
        self.d.app_start('cn.soulapp.android')
        time.sleep(3)


    def doit(self):
        """
        swipe + click stars
        """
        # 否则滑动失效
        time.sleep(0.5)
        self.d.swipe(500, 1500, 500, 1300)
        while True:
            # 如果不加等待,在滑动后元素无法识别
            time.sleep(0.5)
            for i in range(1,3):
                # try:
                # 定位框架
                frame = self.d(resourceId="cn.soulapp.android:id/item_post_all", className="android.view.ViewGroup",
                               instance=i)
                try:
                    center = frame.center()
                except:
                    print(f'{i},无法获取中心位置')
                    continue
                # 可能图标还没漏出来
                if center[1] > 1250:
                    print(f'{i},中心位置大于1250')
                    continue
                # 可能没有文字
                try:
                    name = frame.child(resourceId="cn.soulapp.android:id/expandable_text").get_text()
                except:
                    name = str(time.time())
                if redis_cli.sismember('soul',name):
                    print(f'存在该用户    {name}')
                    continue
                frame.child(resourceId="cn.soulapp.android:id/iv_like",clickable=True).click_exists(timeout=1)
                self.num += 1
                print(f'{self.num},点击完成')
                redis_cli.sadd('soul',name)
            self.d.swipe(500, 1500, 500, 1300)

    def run_spider(self):
        """
        微信朋友圈自动点赞,舔狗程序
        """
        self.open_soul()
        self.doit()


if __name__ == '__main__':
    """
    存在滑动实效的问题
    """
    tiangou = TianGou('2244261a')
    tiangou.run_spider()