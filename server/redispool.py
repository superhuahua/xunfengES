import sys
import os
import redis
from Config import RedisConfig

def getPoolBR():
    try:
        poolBR = redis.ConnectionPool(host=RedisConfig.HOST, port=RedisConfig.PORT, password=RedisConfig.PASSWORD, db=RedisConfig.BR)
        return redis.Redis(connection_pool=poolBR)
    except Exception as e:
        print 'redis connect error'
        return 'None'

def getStrictRedis():
    try:
        r = redis.StrictRedis(host=RedisConfig.HOST, port=RedisConfig.PORT, password=RedisConfig.PASSWORD, db=RedisConfig.BR)
        return r
    except Exception as e:
        print 'redis connect error'
        return 'None'
