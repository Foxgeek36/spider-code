import requests
# 账号登录登录
login_url = 'http://api.xinheyz.com/api/do.php?action=loginIn&name=shixiaolong&password=nishijiba22'
token = 'a79a9b08d442a8ff3a07140b80a7f525'
# 获取手机号
getphone_url = f'http://api.xinheyz.com/api/do.php?action=getPhone&sid=1838&token={token}'
# 通过手机号获取验证码，３ｓ刷一次　６０次都刷不到就把手机号拉黑
getMessage_url = f'http://api.xinheyz.com/api/do.php?action=getMessage&sid=1838&phone={}&token={token}&author=shixiaolong'
# 拉黑手机好
addBlacklist = f'http://api.xinheyz.com/api/do.php?action=addBlacklist&sid=1838&phone={}&token={token}'


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
r = requests.get(getphone_url)
print(r.text)
