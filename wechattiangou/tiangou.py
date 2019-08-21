import uiautomator2 as u2
import time
import os


class TianGou:
    """
    wechat greasiness dog
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


    def test1(self):
        """
        不给自己点赞
        :return:
        """
        # 定位框架
        frame = self.d(resourceId="com.tencent.mm:id/eu8", className="android.widget.LinearLayout", instance=1)
        # 拿到昵称
        text = frame.child(resourceId="com.tencent.mm:id/b9i").get_text()
        # 不给自己点赞
        # if text != 'change':
        frame.child(resourceId="com.tencent.mm:id/eop", description=u"评论", className="android.widget.ImageView").click_exists(timeout=1)


    def test2(self):
        """
        不给广告点赞
        :return:
        """
        # 定位框架
        frame = self.d(resourceId="com.tencent.mm:id/eu8", className="android.widget.LinearLayout", instance=1)
        # 广告
        status = frame.child(resourceId="com.tencent.mm:id/enc").exists(timeout=1)
        if status:

            text = frame.child(resourceId="com.tencent.mm:id/enc").get_text()
            print(text)

    def test3(self):
        """
        jiesuo
        :return:
        """

        self.d.swipe_points([(0.235, 0.456), (0.503, 0.449), (0.509, 0.601), (0.777, 0.603), (0.771, 0.763), (0.222, 0.75)], 0.2)

    def open_wechat(self):
        """
        打开微信朋友圈
        :return:
        """
        # start wechat
        self.d.app_start('com.tencent.mm')
        # select friends zone
        self.d(resourceId="com.tencent.mm:id/sh", className="android.widget.ImageView", instance=2).click()
        # open friends zone
        self.d(className="android.widget.LinearLayout", instance=7).click()

    def skip(self,frame):
        """
        跳过自己和广告
        """
        # 拿到昵称
        text = frame.child(resourceId="com.tencent.mm:id/b9i").get_text()
        status = frame.child(resourceId="com.tencent.mm:id/enc").exists(timeout=1)
        # 不给自己点赞
        if text == 'change':
            return True
        # 广告
        elif status:
            return True
        else:
            return False

    def swipe(self):
        """
        swipe + click stars
        """
        # 否则滑动失效
        time.sleep(1)
        self.d.swipe(500, 2000, 500, 1500)
        while True:
            # 如果不加等待,在滑动后元素无法识别
            time.sleep(1)
            for i in range(1,2):
                try:
                    # 定位框架
                    frame = self.d(resourceId="com.tencent.mm:id/eu8", className="android.widget.LinearLayout",
                                   instance=i)

                    # 跳过不需要点赞的
                    if self.skip(frame):
                        print("Needn't click star")
                        continue

                    frame.child(resourceId="com.tencent.mm:id/eop", description=u"评论",
                                className="android.widget.ImageView").click_exists(timeout=1)
                    # 是要识别未被点赞过得,否则就取消了
                    zan = self.d(resourceId="com.tencent.mm:id/eoc")
                    text = zan.get_text()
                    if text == '赞':
                        zan.click()
                        print('click star successfully')
                    else:
                        print('already star no click')
                        # raise Exception('已经点赞过了')
                except:
                    break
            #当前可见的页无需要点赞的继续往下滑动
            time.sleep(1)
            # d(scrollable=True).scroll(steps=2)
            # 上滑
            self.d.swipe(500, 2000, 500, 1200)
            # 往下滑
            # d.swipe(500, 500, 500, 1500)
            # time.sleep(1)
            # d.swipe(500, 2000, 500, 1500)

    def run_spider(self):
        """
        微信朋友圈自动点赞,舔狗程序
        """
        self.open_wechat()
        self.swipe()


if __name__ == '__main__':
    tiangou = TianGou('2244261a')
    tiangou.run_spider()