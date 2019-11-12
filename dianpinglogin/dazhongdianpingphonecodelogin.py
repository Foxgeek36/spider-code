import zlib
import base64
import time
import json
import requests
import pyp

class GetToken:
    def __init__(self,user,password):
        """
        :param user: 你的电话号
        :param password: 你的密码
        """
        self.password = password
        self.user = user

    def BirthToken(self):
        """
        生成加密的token
        :return:
        """
        userdata = '"riskChannel=202&user={}"'.format(self.user).encode()
        sign = base64.b64encode(zlib.compress(userdata)).decode('utf-8')
        now = int(time.time()*1000)
        ip = {
                "rId":"100049",
                "ver":"1.0.6",
                "ts":now,
                "cts":now+906489,#保证比ts大
                "brVD":[290, 375],
                "brR":[
                    [1366, 768],
                    [1366, 728], 24, 24
                ],
                "bI":["https://account.dianping.com/account/iframeLogin?callback=EasyLogin_frame_callback0&wide=false&protocol=https:&redir=http%3A%2F%2Fwww.dianping.com", "https://account.dianping.com/login?redir=http://www.dianping.com"],
                "mT":["220,156", "220,156", "220,157", "219,158", "219,159", "219,161", "219,162", "217,163", "217,165", "215,166", "214,167", "214,169", "213,169", "213,171", "212,172", "211,173", "211,175", "210,177", "210,179", "210,182", "210,184", "210,185", "210,186", "210,188", "210,189", "210,191", "209,193", "208,196", "208,199", "208,200"],
                "kT":["3,INPUT", "2,INPUT", "9,INPUT", "9,INPUT", "8,INPUT", "9,INPUT", "1,INPUT", "2,INPUT", "6,INPUT", "7,INPUT", "1,INPUT", "\\b,INPUT", "\\b,INPUT", "\\b,INPUT", "\\b,INPUT", "6,INPUT", "3,INPUT", "1,INPUT"],
                "aT":["220,156,BUTTON", "100,163,INPUT", "99,160,INPUT", "181,113,INPUT", "275,20,DIV"],
                "tT":[],
                "aM":"",
                "sign":sign
            }
        info = json.dumps(ip, separators=(',', ':')).encode('utf-8')
        token = base64.b64encode(zlib.compress(info)).decode('utf-8')
        token = token.replace('+',' ')
        print(token)
        return token

    def GetPhonecode(self):
        """
        调用发送手机验证码的接口
        :return:
        """
        # 拿到加密参数
        _token = self.BirthToken()
        url = "https://account.dianping.com/account/ajax/checkRisk"
        headers = {'Referer':"https://account.dianping.com/account/iframeLogin?callback=EasyLogin_frame_callback0&wide=false&protocol=https:&redir=http%3A%2F%2Fwww.dianping.com",
                   'Accept-Encoding':'gzip, deflate, br',
                   'Content-type':'application/x-www-form-urlencoded',
                   'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
                   }
        formdata = {
            'riskChannel':'202',
            'user':self.user,
            '_token':_token
        }
        response = requests.post(url,data=formdata,headers=headers)
        print(response.text)
        # 请求发验证码的接口
        headers.update({'X-Requested-With':'XMLHttpRequest'})
        formdata = {'mobileNo':self.user,
                    'uuid':response.json()['msg']['uuid'],
                    'type':'304',
                    'countrycode':'86'
                    }
        url = 'https://account.dianping.com/account/ajax/mobileVerifySend'
        response = requests.post(url,data=formdata,headers=headers)
        print(response.text)


if __name__ == '__main__':
    # gettoken = GetToken('17621989923','password')
    # gettoken.GetPhonecode()
    # s = 'eJxNTttugkAQ/Zd57QZmgWWBxAdLm1RbtFJKjcYHRLsQy6UsKdWm/94xsYnJJOcy5yTnB7rJDgKOiA5n8LXvIABuoOECg17TR0h0ubQ8XzqSQX7t+ehKwWDbpXcQrLknbGbbYnN2YjLW3LeQcfRww6655dCdUxMKQdH3bWCawzAYuzKr27JWRt5Upi6a1pSWLThKpDFAjSqhBuHhgtkF+38d0XrK6lLVxPbT7+RFO/rzPY50kr4e0Y5OD7P50/3H7HT0wjBWq7dHla5uFsvxtK5inVWF2la3h2a8fM7n4WI0gt8/X8FQHQ=='
    # s = 'eJxNTttugkAQ/Zd57QZmgWWBxAdLm1RbtFJKjcYHRLsQy6UsKdWm/94xsYnJJOcy5yTnB7rJDgKOiA5n8LXvIABuoOECg17TR0h0ubQ8XzqSQX7t+ehKwWDbpXcQrLknbGbbYnN2YjLW3LeQcfRww6655dCdUxMKQdH3bWCawzAYuzKr27JWRt5Upi6a1pSWLThKpDFAjSqhBuHhgtkF+38d0XrK6lLVxPbT7+RFO/rzPY50kr4e0Y5OD7P50/3H7HT0wjBWq7dHla5uFsvxtK5inVWF2la3h2a8fM7n4WI0gt8/X8FQHQ=='
    # s = 'eJxVT9lugkAU/Zd5lcjMwDAzvinighXUAEaNDwoKVBbLImLTf++QtEmb3OTce5bk3E9QzAMwQBBCFUngcSnAAKA+7GtAAlUpFEKhhqjGENKwBPz/nMaZBM6FNwaDA2JEkRSFHDtmI4gD4hhKCDJ4lP7uWBXTuebCBKKqug9kuWmafhCfsnuchX0/T+Uyyu8yxQpBkEJRBohE6nQJhrmk4I6johKGvJNunSTw9IPV770UDwlrGYeZ2C5mY7Vvhh22Q3dtTWR/q7sjNQoNsqiVaz6LbNM5G665S7FzzZqARkmNLquQF5lvYq4vtil1x8Wk3KlqEsCK7xaTZ4xiXhpV5OwXPTjVd+ydrVWzTALTeqqe/iJeHqG9YmQOd2zLG47arf+8lWtWs/119fCH3itYJclUnxHTTO3rsMkUai/L9uFMWY9PQ3LTca1xd/+cb275x4rAy9gZga9vNod/Uw=='
    # wechat api
    s = 'eJxdi9lugkAUht9lbiEROjCISS9cQKm4sAii8QJwWET2sUCbvntxuWianPzLl/98g0o5gxHLMDQgdR94gUEs4lmO50Ua+P+Y0DOvsmZgdIQipBFEpzvQ+35kmSFLswInnui/+Y3r775S+hEoXD9xQ1wPauxWfjQoHuUa1+QhgAZPEmdn3D4V9M+p2T/3nrzcfTl5eR2HGRgB/NFZl0RSw8vYbz1KzVUsfe3g2XFwqK83YR5NkRGgs4KCWF0WW9iUjI8CiLczTLHpvqrI0pBKXELt0MqmTBy1MRYeNHU7sYVkbwSRzwssyvQhujq31YEURVzIQrfaTZyDxplGzTV1fE3lyXxhWiV2xssolObebZOrjZ7nnb2K7JZqc8LAwM7SriUet2umrRx9puIlYJRuqItakcaNOffnVGcQShG2/np1zRqKrN9qy6y0d/DzC7wjibY='
    # sign
    # s = 'eJyVjkELgjAcxb+LoLeEzU3dYYegRNOgohC6Sf6dI6fiLKpP3wq0c6f3ePDe+1mXrrtKSEqeq3QZxFTFtYLwSHb3TRWkW7kXSfhc5716nR86lYuMZtppipF7yMUBYZQ4TSs4wsilmFBGHTVqeYAKhgEGbuOoLwRooyWMhWx+xot03fWnmyxtb4UwCxFhvm9jf0Iy8R9QpmiwTGcG+ySt+I7PcNMlnw+tN2sVTrQ=d'
    b = base64.b64decode(s)
    z = zlib.decompress(b)
    print(z)
    print(z.decode())



