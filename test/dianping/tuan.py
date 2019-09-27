import requests

headers = {
"charset":"utf-8",
"Accept-Encoding":"gzip",
"referer":"https://servicewechat.com/wx734c1ad7b3562129/138/page-frame.html",
"wechatversion":"7.0.6",
"sdkversion":"2.8.3",
"channelversion":"7.0.6",
"minaname":"dianping-wxapp",
"minaversion":"4.20.0",
"channel":"weixin",
"content-type":"application/json",
"platformversion":"9",
"platform":"Android",
"User-Agent":"Mozilla/5.0 (Linux; Android 9; MI 8 Build/PKQ1.180729.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.132 Mobile Safari/537.36 MicroMessenger/7.0.6.1500(0x2700063D) Process/appbrand0 NetType/WIFI Language/zh_CN",


"Host":"m.dianping.com",
"Connection":"Keep-Alive"
}


headers={
"Charset":"utf-8",
"Accept-Encoding":"gzip",
"Referer":"https://servicewechat.com/wx734c1ad7b3562129/138/page-frame.html",
"Wechatversion":"7.0.6",

"Sdkversion":"2.8.3",
"Channelversion":"7.0.6",
"Minaname":"dianping-wxapp",
"Minaversion":"4.20.0",


"Channel":"weixin",
"Content-Type":"application/json",
"Platformversion":"9",
"Platform":"Android",
"User-Agent":"Mozilla/5.0 (Linux; Android 9; MI 8 Build/PKQ1.180729.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.132 Mobile Safari/537.36 MicroMessenger/7.0.6.1500(0x2700063D) Process/appbrand0 NetType/WIFI Language/zh_CN",
"Host":"m.dianping.com",
"Connection":"Keep-Alive",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Accept-Language":"en",
}

headers = {

"User-Agent":"Mozilla/5.0 (Linux; Android 9; MI 8 Build/PKQ1.180729.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.132 Mobile Safari/537.36 MicroMessenger/7.0.6.1500(0x2700063D) Process/appbrand0 NetType/WIFI Language/zh_CN",
"Accept-Encoding":"gzip",
"Accept":"*/*",
"Connection":"Keep-Alive",
"Charset":"utf-8",
"Referer":"https://servicewechat.com/wx734c1ad7b3562129/138/page-frame.html",
"Wechatversion":"7.0.6",
"Sdkversion":"2.8.3",
"channelversion":"7.0.6",
"minaname":"dianping-wxapp",
"minaversion":"4.20.0",
"channel":"weixin",
"content-type":"application/json",
"platformversion":"9",
"platform":"Android",
"Host":"m.dianping.com",

}

# url = 'https://m.dianping.com/wxmapi/shop/shoptuan?shopUuid=93361578&cityId=1'
url = 'https://m.dianping.com/wxmapi/shop/shoptuan?shopUuid=17453003&cityId=4'
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}
res = requests.get(url,headers=headers,proxies=proxies,verify=False)
print(res.status_code,res.text)



# headers = {
# "charset":"utf-8",
# "Accept-Encoding":"gzip",
# "referer":"https://servicewechat.com/wx734c1ad7b3562129/138/page-frame.html",
# "ismicromessenger":"true",
# "phone-brand":"Xiaomi",
# # "dpid":"WmKA7H5mHhme8T4PvJf7KMiQgI8yEWpmzZxsKi-L5Ls",
# "channel":"weixin",
# "appversion":"4.20.0",
# "platform":"Android",
# # "token":"00e2749061b3538bb85cce2e7e8700ccc900eba389e830c69fd2652dc014c47ab314a04e7bca54659a91a632369abc6160436d73d4c126b115a866f922a59277",
# "network-type":"wifi",
# "phone-model":"MI 8",
# "appname":"dianping-wxapp",
# "content-type":"application/json",
# "platformversion":"9",
# "micromsgversion":"7.0.6",
# "User-Agent":"Mozilla/5.0 (Linux; Android 9; MI 8 Build/PKQ1.180729.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.132 Mobile Safari/537.36 MicroMessenger/7.0.6.1500(0x2700063D) Process/appbrand0 NetType/WIFI Language/zh_CN",
# "Host":"mapi.dianping.com",
# "Connection":"Keep-Alive"
# }
#
# url = 'https://mapi.dianping.com/mapi/wechat/shop.bin?shopUuid=93361578'
#
# res = requests.get(url,headers=headers)
# print(res.text)
#
