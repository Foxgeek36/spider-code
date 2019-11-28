# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta
import time

import dateparser
from dateparser import parse


_TODAY = datetime.now()
_TOMORROW = time.mktime((_TODAY + timedelta(days=1)).timetuple())
_ONE_MONTH_AGO = time.mktime((_TODAY - timedelta(days=60)).timetuple())


def is_candidate_column(url=None, title=None):
    """
    通过url 和 title 结合判断，该链接是否是分栏链接
    :param url:
    :param title:
    :return:
    """
    if isinstance(url, str):
        if 'content' in url and 'detail' in url:
            return False

        article_patterns = [r'.*?content_\d+.*', r'.*?/nw\..*?' ]

        for pattern in article_patterns:
            p = re.compile(pattern, re.I)
            rslt = re.search(p, url)
            if rslt:
                return False

        if isinstance(title, str):
            _title = title.replace('第', '', 1)
            _title = _title.replace('期', '', 1)
            rslt = parse(_title)
            if isinstance(rslt, datetime):
                try:
                    time_temp = time.mktime(rslt.timetuple())
                except:
                    time_temp = 0
                if _ONE_MONTH_AGO <= time_temp <= _TOMORROW:
                    return True


        if isinstance(title, str):
            if len(title) > 35:
                return False
            patterns_title = [r'.*?第.*?版.*?',
                              r'\w{1,10}版.*?',
                              r'.*?下一版.*?',
                              r'[A-Z][0-9]?[0-9]?：.*',
                              r'^\d{1,2}:.{1,10}',
                              r'^[A-D]\d{1,2}.{1,10}',
                              r'\[A\d{1,2}\].{1,10}',
                              r'.*?/uniflows/html/\d{4}/\d{2}/\d{2}/\d{2}/\d{2}\.htm',
                              ]
            for pattern in patterns_title:
                p = re.compile(pattern, re.I)
                rslt = re.search(p, title)
                if rslt:
                    return True



def is_article_url(url=None, title=None,nod_name=None):
    """
    判断链接是否是文章url
    :param url: 需要识别的url
    :param title: 辅助性判断行元素
    :param nod_name: 标签名字，如果是area直接返回True
    """
    if nod_name == 'area_node':
        return True
    # 和小好商量过滤字符长度小于5的url
    if title == None or len(title) >= 50 or len(title) < 10:
        return False

    if isinstance(url, str):
        # sub, sub_part, domain, domain_part, tail, tail_part, suffix = temp

        patterns = [r'.*?content_\d+.*', r'.*?/nw\..*?', r'.*?content\d+_\d+.*']

        for pattern in patterns:
            p = re.compile(pattern, re.I)
            rslt = re.search(p, url)
            if rslt:
                return True
        for i in ['content','articel','article','newsid','news','News','NEWS','id','show']:
            if i in url:
                return True
        return True
