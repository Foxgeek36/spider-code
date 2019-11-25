from redis import Redis
redis_cli = Redis(host='118.31.66.50')

# name = '仙娜人事复星锦绣路站,要吃红烧肉闵行,服装店重庆带来上海,主播虹桥,静安性感小摩托,住周浦嘉定卖包,你好'
# names = name.split(',')
# for n in names:
#     print(n)
#     redis_cli.sadd('soul:white_list',n)

for i in redis_cli.smembers('soul:white_list'):
    print(i.decode())