import re
from copy import deepcopy
from lxml import etree
from datetime import datetime

"""
TO DO
如果正文中存在超链接文本,存在被剔除的风险
"""

class HtmlContentExtract:

    def __init__(self,htmltext):
        """
        :param htmltext:html文本
        抽取正文的 文章详情 发布日期
        :return
        """
        tree = etree.HTML(htmltext)
        scripts = tree.xpath('//script/text()')
        contents = tree.xpath('//*/text() | //br/following::text()[1]')

        # 剔除超链接文本
        for pattern in tree.xpath('//*'):
            if pattern.xpath('./@href'):
               text = pattern.xpath('./text()')
               if text:
                   contents.remove(text[0])
        # 剔除script 文本
        for i in scripts:
            try:
                contents.remove(i)
            except:
                pass
        self.text = contents

    def countwrap(self):
        """
        统计不同段落间的换行数，值为当前元素与下个元素的距离
        给文本从上到下，编号，排序
        根据不同段落间的换行数（间距）和排序位置 确定段落性质
        该算法会漏掉最后一个文本的计数（文本之间丢弃），

        需注意字典的键有可能重复
        :return {'data': {1: ['铜山区人民政府', 10], 2: ['铜山区人民政府', 5], 3: ['高级搜索', 9], 4: ['首页', 1], 5: ['走进铜山', 1], 6: ['信息公开', 1], 7: ['公共服务', 1], 8: ['政民互动', 1], 9: ['新闻中心', 1], 10: ['专题专栏', 1], 11: ['铜山论坛', 4], 12: ['铜山发布', 0], 13: ['扫描二维码', 1], 14: ['��', 0], 15: ['铜山区预决算公开平台', 6], 16: ['当前位置', 0], 17: ['：', 0], 18: ['首页', 0], 19: [' > ', 0], 20: ['新闻中心', 0], 21: [' > ', 0], 22: ['本地新闻', 0], 23: [' > ', 0], 24: ['政务要闻', 3], 25: ['高建民检查安全生产工作', 1], 26: ['发布日期：2019-07-02\xa0作者：常成龙\xa0\xa0\xa0\xa0 点击：', 0], 27: [' \xa0\xa0\xa0\xa0字体： [ ', 0], 28: ['大', 1], 29: ['中', 1], 30: ['小', 0], 31: [' ]  ', 2], 32: ['\xa0\xa0\xa0 6月29日下午，区长高建民率公安局、住建局、城管局、生态环境局等相关单位检查安全生产工作。高建民一行实地查看了美的雍翠园建筑工地、汉王瑞祥烟花爆竹仓库、刘集镇徐州海飞箱桥制造有限公司等地，详细了解企业的安全生产工作规程、消防设施配备以及重点区域重点环节安全生产制度措施落实情况。高建民要求，要时刻绷紧安全生产这根弦，加强日常运行的安全管理，严格落实安全生产各项制度措施，严防各类安全事故发生。企业要切实担负起主体责任，把安全生产牢牢扛在肩上、记在心上、抓在手上、落实在行动上，为企业稳定、健康发展提供坚强的安全保障。各有关部门和单位要明确职责，认真落实监管职责，切实把各项安全生产措施做得更扎实，把各类安全隐患排查治理得更到位。', 4], 33: ['分享到：', 3], 34: ['关闭页面', 0], 35: ['|', 0], 36: ['打印', 0], 37: ['|', 0], 38: ['收藏', 6], 39: ['联系我们', 0], 40: [' | ', 0], 41: ['站点地图', 0], 42: [' | ', 0], 43: ['收藏本站', 1], 44: [' 主办单位：中共铜山区委 铜山区人民政府\xa0\xa0\xa0承办单位：中共铜山区委宣传部\xa0\xa0\xa0版权所有：徐州市铜山区人民政府办公室\n            ', 0], 45: ['备案序号：', 0], 46: ['苏ICP备09062975号-1', 0]}, 'ElementCount': 46}

        """

        # 对\n 进行计数
        num = 0
        # 文本与\n之间的状态,0代表上一个元素为空
        start = 0
        end = 0
        # 记录元素的位置
        position = 0

        # 缓存当前比对区间第一个文本
        NowElement = None
        # json保存统计结果
        result_json = {'data': {}}
        for i in self.text:
            # if '市客服中心工作人员说，钱包里有一张会员卡，他们通过会员卡关' not in i:
            #     continue
            realcontent = i.replace('\n', '').strip()
            if start == 0:
                if len(realcontent) > 5:
                    start = 1
                    # 将原始元素（文本）赋值给变量
                    NowElement = i
                    position += 1
                # else:
                #     num += 1
            else:
                # 中间空置计数
                if not realcontent:
                    num += 1
                # 下一个有文本，end = 1
                else:
                    end = 1
                    # 一个统计区间结束
                    if start and end:
                        result_json['data'][position] = {'NowElement': NowElement, 'num': num}
                        # 复位
                        num = 0
                        # 复位
                        # 将下一个比对区间的第一文本替换为上一个比对区间的后一个文本
                        NowElement = i
                        position += 1
        if position not in result_json:
            result_json['data'][position] = {'NowElement': NowElement, 'num': num}
        return result_json


    def combination(self):
        """
        将相邻的元素且间距为0 且字符长度大于5的组合
        :return:
        """

        data = self.countwrap()
        datacopy = deepcopy(data['data'])
        CombinNum = {}
        # 记录换行书为0 的序号
        nownum = 0
        firstnum = None
        # 每组的最后一个num为0的元素，记录其序号
        lastnum = 0
        for ele in data['data']:

            # 在换行等于0并且是相邻元素的时候，放入一个列表
            if data['data'][ele]['num'] == 0:
                # 整个json的第一组的第一个元素
                if nownum == 0:
                    firstnum = ele

                    CombinNum[firstnum] = [data['data'][ele]['NowElement']]
                    # 将字典中该条数据剔除
                    datacopy.pop(ele)
                    # 将当前序号赋值给零时计数器 nownum
                    nownum = ele
                # 判断是否相邻,相邻的就放入一个列表
                elif ele - nownum == 1:
                    CombinNum[firstnum].append(data['data'][ele]['NowElement'])
                    datacopy.pop(ele)
                    # 将当前序号赋值给零时计数器 nownum
                    nownum = ele
                    lastnum = ele
                # 如果是当前的一组比对完，经过几个噪音，到下一组第一个的时候，从新开辟一个新的key
                else:
                    # nownum = 0
                    firstnum = ele
                    CombinNum[firstnum] = [data['data'][ele]['NowElement']]
                    datacopy.pop(ele)
                    # 将当前序号赋值给零时计数器 nownum
                    nownum = ele
            # 每组最后一个元素即使num不是0，依旧应该添加到一组中，因为上一个元素和它中间换行数是0
            else:
                if (ele > 1) and (ele - nownum == 1):
                    # 记录每组最后一个元素与下一个元素的换行数
                    CombinNum[firstnum].append(data['data'][ele]['NowElement'] + "--{}".format(data['data'][ele]['num']))
                    datacopy.pop(ele)
        # 如果是孤立的一个元素 并且不包含时间，就剔除
        pattern = re.compile(r'(20\d{2}[_,/,\-,年]\d{1,2}[/,_,\-,月]\d{0,2})(\s{1}\d{2}:\d{2}:\d{2}){0,1}')
        CombinNumCopy = deepcopy(CombinNum)
        for element in CombinNum:
            if len(CombinNum[element]) == 1 and not re.findall(pattern,CombinNum[element][0]):
                CombinNumCopy.pop(element)
        LastCombinNum = deepcopy(CombinNumCopy)
        for element in CombinNumCopy:
            try:
                newcontent = ''.join(CombinNumCopy[element]).split('--')
                LastCombinNum[element] = {'NowElement': newcontent[0], 'num': int(newcontent[1])}
            # 兼容最后一组最后一个元素 num 为0的情况
            except:
                LastCombinNum[element] = {'NowElement': ''.join(CombinNumCopy[element]), 'num': 0}

        datacopy.update(LastCombinNum)
        return datacopy

    def exclude(self):
        """
        剔除长度小于5的垃圾文本
        剔除中文占比小于50%,英文占比大于50%的文本
        剔除离散的文本（长度小于10，并且前后的换行数大于3）
        :return(list):[(1, {'NowElement': '《广东省地方志工作条例》解读-吴川市人民政府门户网站', 'num': 26}), (11, {'NowElement': '您现在所在的位置：吴川市人民政府门户网站', 'num': 0})]
        """
        data = self.combination()
        datacopy = deepcopy(data)
        # 上一个元素的num值
        upelement = 0
        #上一个元素的index
        upindex = 0
        for i in data:
            # 其他文本长度的计算也剔除空格的影响
            content_statistics = data[i]['NowElement'].strip()

            # 剔除长度小于5的垃圾文本
            if len(content_statistics) < 5:
                datacopy.pop(i)
                # 在剔除该元素之后把该元素的换行添加到上一个元素上
                if upindex != 0:
                    datacopy[upindex]['num'] = datacopy[upindex]['num'] + data[i]['num']
                continue

            # 剔除中文占比小于50 %, 英文占比大于50 % 的文本或者数字占比小于50%
            zh = re.findall(r'[\u4E00-\u9FA5]', content_statistics)
            en = re.findall('[a-zA-Z]', content_statistics)
            num = re.findall('[0-9]+', content_statistics)
            num = ''.join(num)
            if ((len(zh)/len(content_statistics)) < 0.5) and (((len(en)/len(content_statistics)) > 0.35) or ((len(num)/len(content_statistics)) < 0.2)):
                datacopy.pop(i)
                # 在剔除该元素之后把该元素的换行添加到上一个元素上
                if upindex != 0:
                    datacopy[upindex]['num'] = datacopy[upindex]['num'] + data[i]['num']
                continue

            # 剔除离散的文本（长度小于10，并且前后的换行数大于3）
            if len(content_statistics) < 10:
                # 第一个元素
                if upelement == 0:
                    datacopy.pop(i)
                    continue
                else:
                    if (upelement > 3) and (data[i]['num'] > 3):
                        datacopy.pop(i)
                        upelement = data[i]['num']
                        # 在剔除该元素之后把该元素的换行添加到上一个元素上
                        if upindex != 0:
                            datacopy[upindex]['num'] = datacopy[upindex]['num'] + data[i]['num']
                        continue

            # 只有当当前文本是正常值的时候才修改
            upindex = i
        # 按key排序
        s = sorted(datacopy.items(), key=lambda x: x[0])
        return s

    def longest_center_content(self,data):
        """

        各种最长中心原则确定核心文本位置
        取最长文本,并且最长文本处于中心位置,否则为空
        :return: 核心文本的位置
        """
        #提取核心文本,通过最长文本段定位文章核心位置,通过与核心位置进行悬挂高度对比,过滤非正文文本
        # 取出最长文本,及其在列表的index
        longest_content = ''
        index = None
        for serial in data:
            article_content = serial[1]['NowElement']
            if len(article_content.strip()) > len(longest_content.strip()):
                longest_content = article_content
                index = data.index(serial)
        # 拿到列表中最大的index值 与核心文本index进行比较,核心文本应该在页面中间位置,否则该页面为空:
        max_index = len(data)
        # 当 文本列表长度小于4的时候取到的核心文本,默认就是核心位置(中间)
        if max_index > 3:
            if (index/max_index) < 1/3 or (index/max_index) > 4/5:
                status = 0
            else:
                status = 1
        else:
            status = 1
        # status 代表ok,核心文本符合中心最长的标准
        return status , index

    def center(self,data):
        """
        直接取中心文本为核心文本
        :return:
        """
        datacopy = deepcopy(data)
        index = int(len(data)/2)
        if index < 3:
            return 1 , index
        else:
            # 从两边剪枝 减掉悬挂距离大于2的元素,碰到小于2的结束
            for i in data[:index]:
                num = i[1]['num']
                if num > 2:
                    datacopy.remove(i)
                else:
                    break
            # 翻转列表从后往前
            for i in list(reversed(data[index:])):
                num = i[1]['num']
                if num > 2:
                    datacopy.remove(i)
                else:
                    break
            newindex = int(len(datacopy)/2)
            return 1 , newindex

    def MainBody(self,data,index):
        """
        拼接列表中所有的文本，中介加入换行
        :return:
        """

        # print(longest_content)
        # 判断最长文本上一个段落和下一个段落悬挂距离,大于阀值,剔除
        # 从中心往两边推,当某个段落悬挂距离突然大于正常值,以此为节点,剔除文章两端垃圾数据
        # 拿到上面切割点
        upindex = 0
        print(data[index],data)
        for serial in list(reversed(data[:index])):
            if serial[1]['num'] > 1:
                upindex = data.index(serial)
                break

        # 拿到下面切割点,需从核心文本开始,它的num值就是距离下一个文本的悬挂距离 ,赋值None ,当下面条件不成立的时候取到列表最后
        downindex = None
        for serial in data[index:]:
            if serial[1]['num'] > 1:
                # 之所以要+1,是为了剔除悬挂的下方 ,如果serial是最后一个元素,那么downindex会越界,需要处理
                downindex = data.index(serial)+1
                if downindex > data.index(data[-1]):
                    downindex = None
                break

        # 切除垃圾文本后的正文
        if upindex > 0:
            data = data[upindex+1:downindex]
        else:
            # 0号元素的文本就是核心文本
            data = data[upindex:downindex]
        # # 对于第一行类似标题的问题过滤
        # if data[0][1]['num'] > 1:
        #     data.pop(0)

        # 过滤文章开头的发布时间等垃圾信息
        if '来源' in data[0][1]['NowElement']:
            if data[0][1]['num'] > 1 and len(data) > 1:
                data.pop(0)
            elif len(data[0][1]['NowElement']) < 60 and data[0][1]['num'] > 0:
                data.pop(0)
        # 换行
        content = ''
        # 不换行
        content2 = ''
        for i in data:
            if i[1]['num'] > 0:
                huanhang = '\n' * i[1]['num']
            else:
                huanhang = ''
            content += (i[1]['NowElement'] + huanhang)
            content2 += i[1]['NowElement']
        # 对正文长度小于100的进行过滤 ,依据经验确实存在就一句话的新闻比如:"也许是受台风外围影响，7月20日傍晚，从玄武湖眺望南京城市上空有一种别样的美。",但是此类新闻毫无价值,故长度定位100
        if len(content2) < 100:
            return None
        return content.strip()


    def main_body_longest(self):
        data = self.exclude()
        longest_content = ''
        longest_index = 0
        for serial in data:
            article_content = serial[1]['NowElement']
            if len(article_content.strip()) > len(longest_content.strip()):
                longest_content = article_content
                longest_index = data.index(serial)
        # print(longest_content)
        # 判断最长文本上一个段落和下一个段落悬挂距离,大于阀值,剔除
        # 从中心往两边推,当某个段落悬挂距离突然大于正常值,以此为节点,剔除文章两端垃圾数据
        # 拿到上面切割点
        upindex = 0
        for serial in list(reversed(data[:longest_index])):
            if serial[1]['num'] > 1:
                upindex = data.index(serial)
                break

        # 拿到下面切割点,需从核心文本开始,它的num值就是距离下一个文本的悬挂距离 ,赋值None ,当下面条件不成立的时候取到列表最后
        downindex = None
        for serial in data[longest_index:]:
            if serial[1]['num'] > 1:
                # 之所以要+1,是为了剔除悬挂的下方 ,如果serial是最后一个元素,那么downindex会越界,需要处理
                downindex = data.index(serial)+1
                if downindex > data.index(data[-1]):
                    downindex = None
                break

        # 切除垃圾文本后的正文
        if upindex > 0:
            data = data[upindex+1:downindex]
        else:
            # 0号元素的文本就是核心文本
            data = data[upindex:downindex]
        # 过滤文章开头的发布时间等垃圾信息
        if '来源' in data[0][1]['NowElement']:
            if data[0][1]['num'] > 1 and len(data) > 1:
                data.pop(0)
            elif len(data[0][1]['NowElement']) < 60 and data[0][1]['num'] > 0:
                data.pop(0)


        # 换行
        content = ''
        # 不换行
        content2 = ''
        for i in data:
            if i[1]['num'] > 0:
                huanhang = '\n' * i[1]['num']
            else:
                huanhang = ''
            content += (i[1]['NowElement'] + huanhang)
            content2 += i[1]['NowElement']
        # 对正文长度小于100的进行过滤 ,依据经验确实存在就一句话的新闻比如:"也许是受台风外围影响，7月20日傍晚，从玄武湖眺望南京城市上空有一种别样的美。",但是此类新闻毫无价值,故长度定位100
        if len(content2) < 100:
            return None
        return content.strip()

    def artical_content_lc(self):
        """
        根据最长中心原则确定的核心文本提取的文章详情
        :return:
        """
        data = self.exclude()
        status,index = self.longest_center_content(data)
        if status:
            artical = self.MainBody(data,index)
            return artical
        else:
            return None

    def artical_content_c(self):
        """
        根据中心位置确定核心文本
        :return:
        """
        data = self.exclude()
        status,index = self.center(data)
        if status:
            artical = self.MainBody(data,index)
            return artical
        else:
            return None

    def artical_center(self):
        """
        直接从两边剪枝,提取中间所有文本
        :return:
        """
        data = self.exclude()
        datacopy = deepcopy(data)
        # 从两边剪枝 减掉悬挂距离大于2的元素,碰到小于2的结束
        for i in data:
            num = i[1]['num']
            if num > 10:
                datacopy.remove(i)
            else:
                break
        # 翻转列表从后往前,当前num值大于2,剔除上一个
        last_element = None
        for i in list(reversed(data)):
            num = i[1]['num']
            if num > 10:
                if last_element:
                    try:
                        datacopy.remove(last_element)
                    except:
                        print('yishan  {}'.format(last_element))
            else:
                break
            last_element = i

        #切割点index列表:
        index_cuts = []

        for i in datacopy:
            num = i[1]['num']
            if num > 10:
                index_cuts.append(datacopy.index(i))
        index_cuts.insert(0,0)
        allparagraph_content = []
        split_dic = {}
        for head in index_cuts[:-1]:
            tail = index_cuts[index_cuts.index(head) + 1]
            if head == 0:
                paragraph = datacopy[head:tail + 1]
            paragraph = datacopy[head+1:tail+1]
            paragraph_content = ''
            for i in paragraph:
                paragraph_content += i[1]['NowElement']
            allparagraph_content.append(paragraph_content)
            split_dic[paragraph_content] = paragraph
        longest_paragraph = split_dic[max(allparagraph_content,key=len)]
        # 换行
        content = ''
        # 不换行
        content2 = ''
        for i in longest_paragraph:
            if i[1]['num'] > 0:
                huanhang = '\n' * i[1]['num']
            else:
                huanhang = ''
            content += (i[1]['NowElement'] + huanhang)
            content2 += i[1]['NowElement']
        # 对正文长度小于100的进行过滤 ,依据经验确实存在就一句话的新闻比如:"也许是受台风外围影响，7月20日傍晚，从玄武湖眺望南京城市上空有一种别样的美。",但是此类新闻毫无价值,故长度定位100
        if len(content2) < 100:
            return None
        return content.strip()


    def timepaser(self):
        """
        提取详情页的时间并且解析
        :param content:
        :return:
        """
        data = self.combination()
        content = ''
        for i in data:
            content += data[i]['NowElement']
        # 必须精确到日最少，再少就不考虑了
        pattern = re.compile(r'(20\d{2}[_,/,\-,年]\d{1,2}[/,_,\-,月]\d{1,2})(\s{1}\d{2}:\d{2}(:\d{2}){0,1}){0,1}')
        # 拿到文章中提取的时间[('2017-05-08', '', ''), ('2009年10月', '', ''), ('2012年2月', '', ''), ('2012年7月', '', ''), ('2012年10月23', '', '')]
        # print(content)
        date_match = re.findall(pattern,content)
        # print(date_match)
        # 将元组转化为字符串
        date_list = []
        for date_tuple in date_match:
            date_list.append(''.join(date_tuple))
        # print(date_list)
        if len(date_list) == 0:
            return None
        elif len(date_list) == 1:
            date_str = date_list[0]
        else:
            # 剔除往年的日期,不包含今年和去年的
            nowyear = datetime.today().year
            new_date_list = deepcopy(date_list)
            for i in new_date_list:
                if (str(nowyear) not in i) and (str(nowyear-1) not in i):
                    date_list.remove(i)
            # 当列表中时间长度不同时：列表从前往后迭代，两两对比不同的时间的长度，返回最大的
            lastdate = None
            date_str = None
            for i in date_list:
                if lastdate:
                    if i != lastdate:
                        if len(i) > len(lastdate):
                            date_str = i
                        else:
                            date_str = lastdate
                        break
                lastdate = i
            # 如果列表内所有字符串长度相同那么返回index 0
            if not date_str:
                date_str = date_list[0]
        return date_str

