from redis import Redis
redis_cli = Redis('127.0.0.1',6379)
added = redis_cli.sadd('test', 'id')
print(type(added))
