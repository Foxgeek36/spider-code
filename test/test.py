from redis import Redis
redis_cli = Redis()

# cookies = redis_cli.hget('elem_cookies', 1)
# print(cookies)
#
# redis_cli.hset('kk',1,{1:2})


import requests
url = 'https://h5.ele.me/restapi/shopping/v3/restaurants?latitude=31.272856&longitude=121.528798&offset=0&limit=30'
headers = {

# ":authority":"h5.ele.me",
"cache-control":"max-age=0",
"dnt":"1",
"upgrade-insecure-requests":"1",
"user-agent":"Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36",
"sec-fetch-mode":"navigate",
"sec-fetch-user":"?1",
"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"sec-fetch-site":"none",
"accept-encoding":"gzip, deflate, br",
"accept-language":"zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7",
# "cookie":"_utrace=39f59f46c00c1426b061ee8e6c4a1377_2019-10-17; ut_ubt_ssid=5lbntve4fdzmjamzs7awsrjmbyvd06b5_2019-10-17; perf_ssid=bwkkkqpat2jc4ur3pqdjquebpdcsmxnx_2019-10-17; ubt_ssid=4guwydbi3b820plxfmqdn5liddgmspx4_2019-10-17; cna=HwkvFqENtSICAbSn5aIEoDLV; track_id=1571301599|67025959f4b96cd72d97e5ca621bb9ccf1a21df2e7fe932bf9|199dd45f42c41d4c79ecf3c6dd27abf6; USERID=884699394; UTUSER=884699394; SID=iY2uM0G4oQJMWN2uXl2xNc2ro4YV7KYa3wPQ; ZDS=1.0|1571301599|lWwcTSSWEsRmmWQ4K4B+kLw3R4At1aouDU9QvaFPnhSmu/i1g4lmX2EuNAjtBLU+ixxEGhXFWCtdrTBWOJX70A==; _bl_uid=wIkwU106u5kgn8esXmp86F9at2LI; tzyy=550ca0716d20a77147b2bc93c03e1f16; isg=BK-vfpUOLo6ilyq_hgypwn1CPsqz_m4XIxrNhcE8Sp4lEM0SySRvxGCClmaLbNvu; pizza73686f7070696e67=1MkK5-oAczE99P7yXnEoaM43pG5XLIDxpORG3HrPk5GzrYSoCF0OlZS_aULEU65q",

}


cookies = {'SID': 'nF27dfFzEiuJutPB4oFHtDB81z0fXo2yAFkg', 'USERID': '884699394', 'UTUSER': '884699394', 'ZDS': '1.0|1571306095|lWwcTSSWEsRmmWQ4K4B+kD6ib8hfSWXCnjrzTjBrK1D5Mky66LXDNBpjo5hVFpZO7Yeygepe83QzkkI2ixFbmg==','track_id': '1571306095|3931143fc1b9afda6f68a6dd9676c9e9d07882240ffd3167ea|9a3d2b64bc58f15fc273df5e6e49f7ea'}


r = requests.get(url,headers=headers,cookies=cookies)
print(r.status_code,r.text)
