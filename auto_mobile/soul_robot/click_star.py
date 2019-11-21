import uiautomator2 as u2
import time
import os
import logging
from redis import Redis
from greet import Greet
redis_cli = Redis()


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Soul Monitor')


class TianGou:
    """
    soul click star
    适配分辨率，如果不同需要该参数
    displayHeight: 2029,
    displayWidth: 1080,
    """

    def __init__(self,type,deviceid):
        """
        初始化鏈接指定的设备
        :param deviceid: 设备 device  ID
        """
        while True:
            try:
                if type == 'usb':
                    self.d = u2.connect_usb(deviceid)
                else:
                    os.system('python3 -m uiautomator2 init')
                    os.system(f'adb connect {deviceid}')
                    logger.info('初始化')
                    self.d = u2.connect_wifi(deviceid)
                break
            except:
                # 初始化uiautomator2 否则有可能连不上
                os.system('python3 -m uiautomator2 init')
        self.num = 0
        # 给最新的动态点赞
        self.lastest = False
        self.selectt_city = False

    def open_soul(self):
        """
        打开ｓｏｕｌ广场
        """
        # start soul
        self.d.app_start('cn.soulapp.android')
        time.sleep(3)
        self.change_model()

    def change_model(self):
        """
        切换帖子列表的模式
        """
        if self.lastest:
            self.d(resourceId="cn.soulapp.android:id/tv_tab", text="最新").click()
            logger.info('切换到最新帖子模式')
        # 搜索文本内容包含上海的，提高效率（一定要有上海的搜索记录才行）
        if self.selectt_city:
            logger.info('切换到上海')
            try:
                self.d(resourceId="cn.soulapp.android:id/searchLayout").click()
            except:
                self.d(resourceId="cn.soulapp.android:id/ivSearch").click()
            time.sleep(0.5)
            self.d.xpath('//*[@resource-id="cn.soulapp.android:id/toolbar_search"]/android.widget.RelativeLayout[1]').set_text('上海')
            # self.d(resourceId="cn.soulapp.android:id/text_search_record",text="上海").click()
            self.d.press('enter')

    def _click(self):
        # 不确定１号框架可以点击还是２号框架可以点击，测试发现每次最多只有一个可点击
        for i in range(1, 3):
            # 定位框架
            frame = self.d(resourceId="cn.soulapp.android:id/item_post_all", className="android.view.ViewGroup",
                           instance=i)
            try:
                center = frame.center()
            except:
                # logger.error(f'{i},无法获取中心位置')
                continue
            # 可能图标还没漏出来
            if center[1] > 1200:
                # logger.warning(f'{i},中心位置大于1200')
                continue
            # 可能没有文字
            try:
                name = frame.child(resourceId="cn.soulapp.android:id/expandable_text").get_text()
            except:
                name = str(time.time())
            if redis_cli.sismember('soul', name):
                logger.info(f'存在该用户')
                continue
            # 判断小心心有没有暴露出来
            try:
                star_distance = frame.child(resourceId="cn.soulapp.android:id/iv_like", clickable=True).center()
                if star_distance[1] > 1800:
                    continue
            except:
                pass
            frame.child(resourceId="cn.soulapp.android:id/iv_like", clickable=True).click_exists(timeout=1)
            self.num += 1
            logger.info(f'{self.num},点击完成,{name}')
            Greet().greet(self.d,frame)
            redis_cli.sadd('soul', name)


    def doit(self):
        """
        swipe + click stars点击完成
        """
        # 否则滑动失效
        time.sleep(0.5)
        self.d.swipe(500, 1500, 500, 1300)
        while True:
            # 如果不加等待,在滑动后元素无法识别
            time.sleep(0.5)
            self._click()
            self.d.swipe(500, 1500, 500, 1300)

    def run_spider(self):
        """
        """
        self.open_soul()
        self.doit()


if __name__ == '__main__':
    """
    存在将star 点错的问题
    """
    tiangou = TianGou('usb','2244261a')
    # tiangou = TianGou('ip','10.170.111.7')
    tiangou.run_spider()