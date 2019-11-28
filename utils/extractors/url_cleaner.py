# -*- coding: utf-8 -*-
import re
from datetime import datetime

from tld import get_tld

_BANNED_SUBDOMAIN = {
    'bbs', 'bbs1', 'club', 'blog', 'weibo', 'v', 'forum',
    'pic', 'photo', 'video', 'tv', 'live', 'mail', 'lottery',
    'baike', 'search', 'help', 'login', 'map', 'foxue', 'download',
    'japanese', 'email', 'epay', 'vipmail', 'vip', 'caipiao', 'pay',
    'open', 'reg', 'sitemap', 'baoxian', 'astro', 'price',
}

_BANNED_SUFFIX = {
    # images
    'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
    'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg', 'gif',

    # audio
    'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

    # video
    '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
    'm4a', 'm4v', 'flv',

    # office suites
    'xls', 'xlsx', 'ppt', 'pptx', 'pps', 'doc', 'docx', 'odt', 'ods', 'odg',
    'odp',

    # other
    'css', 'pdf', 'exe', 'bin', 'rss', 'zip', 'rar','json'

    # mobile
    'apk', 'dmg',
}

_BANNED_TITLES = [
    '登录', '注册', '联系我们', '版权所有', '隐私保护', 'DedeCMS提示信息',
    '.jpg', '关于我们', '为您服务', '意见反馈', '隐私政策', '订阅', '全文检索',
    '客户服务', '不良信息举报', '招聘信息', '加入我们', '联系方法', '报纸检索',
    '网站地图', '返回顶部', '[详细]', '查看评论', '常见问题解答', '客户端',
    '客服中心', '网站导航', '股吧', '分类信息', '页面找不到', '版权声明', '在线订报',
    '使用帮助', '过往期刊', '联系方式', '回到首页', '返回首页', '人才招聘', '广告价目',
    '返回主页', '站内检索', '投稿', '加为收藏', '旧版入口', '离线浏览', '旧版点击进入',
    '内部邮箱', '广告服务', '上一期', '下一期', '返回头版', '返回首页', '网站首页', '返回首版',
    'PDF', '责任编辑','本版编辑', '信息服务许可证'
]


_BANNED_TAILS = ['video', 'download', 'login', 'radio',
                 'photo', 'price', 'search', 'privacy',
                 'productlist', 'tibet']

_EXPIRED_YEAR_IN_URL = [str(datetime.now().year - i) for i in range(1, 21)]

def get_domain(url):
    """
    拿到域名
    """
    if not isinstance(url, str):
        return
    url = url.lower()
    if not url.startswith('http'):
        return
    try:
        try:
            try:
                domain = re.findall('//(.+?):\d+/', url)[0]
            except:
                domain = re.findall('//(.+?)/', url)[0]
        except:
            try:
                domain = re.findall('//(.+?):\d+', url)[0]
            except:
                domain = re.findall('//(.+)', url)[0]
    except:
        print('垃圾链接     {}'.format(url))
        domain = None
    return domain



def is_vaild_url(url,title=None):
    """
    判断url是否合法，包括对各种垃圾链接的过滤
    结合已经总结的垃圾链接所包含的特征集
    """
    if not isinstance(url, str):
        # print(1)
        return
    url = url.strip().lower()
    if not url.startswith('http'):
        # print(2)
        return

    if any('\u4e00' <= char <= '\u9fff' for char in url):
        # print(4)
        return

    if isinstance(title, str):
        title = re.sub(r'\s+', ' ', title)
        title = title.strip()
        if title == '广告' or title == '无标题':
            # print(5)
            return
        if len(title) < 8:
            return
        result = re.search('2\d{3}年\d{1,2}月\d{1,2}日(\d/\d){0,1}', title)
        # 过滤类似2019年5月18日2/4这样的标题
        if result and len(title) < 20:
            return
        if title:
            for kw in _BANNED_TITLES:
                if kw in title:
                    return
        # 通过url后缀判断url有效性
        suffix = url.split('.')[-1]
        if '&redirect=' in url:
            return
        if suffix in _BANNED_SUFFIX:
            return

        # 非中文标题过滤
        zh = re.findall(r'[\u4E00-\u9FA5]', title)
        en = re.findall('[a-zA-Z]', title)
        num = re.findall('[0-9]+', title)
        num = ''.join(num)
        if (len(zh) / len(title)) < 0.5:
            return

    return True
