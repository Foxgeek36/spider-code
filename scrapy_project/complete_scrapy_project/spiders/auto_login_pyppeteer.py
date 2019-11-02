import time
import asyncio
import pyppeteer


class LoginDianPing:
    """
    类异步
    """
    pyppeteer.DEBUG = True
    page = None

    async def _injection_js(self):
        """注入js 绕过驱动识别
        """
        await self.page.evaluate('''() =>{

                   Object.defineProperties(navigator,{
                     webdriver:{
                       get: () => false
                     }
                   })
                }''')

    async def _init(self):
        """初始化浏览器
        """
        browser = await pyppeteer.launch({'headless': False,
                                          'args': [
                                              '--window-size={1300},{600}'
                                              '--disable-extensions',
                                              '--hide-scrollbars',
                                              '--disable-bundled-ppapi-flash',
                                              '--mute-audio',
                                              '--no-sandbox',
                                              '--disable-setuid-sandbox',
                                              '--disable-gpu',
                                          ],
                                          'dumpio': True,
                                          })
        self.page = await browser.newPage()
        # 设置浏览器头部
        await self.page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                     '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
        # 设置浏览器大小
        await self.page.setViewport({'width': 1200, 'height': 600})


    async def mouse_slider(self):
        """滑动滑块
        """
        await asyncio.sleep(3)
        try:
            await self.page.hover('#yodaBox')
            # 鼠标按下按钮
            await self.page.mouse.down()
            # 移动鼠标
            await self.page.mouse.move(2000, 0, {'steps': 30})
            # 松开鼠标
            await self.page.mouse.up()
            await asyncio.sleep(2)
        except Exception as e:
            print(e, '      :错误')
            return None


    async def main(self):
        """登陆
        """
        # 初始化浏览器
        await self._init()
        # await self.page.goto('https://verify.meituan.com/v2/web/general_page?action=spiderindefence&requestCode=957aacb9810e4466bac2be893facac0e&platform=1000&adaptor=auto&succCallbackUrl=https%3A%2F%2Foptimus-mtsi.meituan.com%2Foptimus%2FverifyResult%3ForiginUrl%3Dhttp%253A%252F%252Fwww.dianping.com%252Fshop%252F20916623&theme=dianping')
        await self.page.goto('https://hotels.ctrip.com/hotel/36148460.html')

        # 注入js
        await self._injection_js()
        time.sleep(1000)
        # 获取滑块元素
        slider = await self.page.querySelector('#yodaBox')
        if slider:
            print('有滑块')
            # 移动滑块
            await self.mouse_slider()
        else:
            print('没滑块')


if __name__ == '__main__':
    login = LoginDianPing()
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(login.main())
    loop.run_until_complete(task)

