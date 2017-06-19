# coding:utf-8
# Redis配置 
class RedisConfig(object):
    HOST = "localhost"
    PORT = 6379
    PASSWORD = ""
    BR = 1
    HOSTSCANKEY = "hostScan"
    VULTASKKEY = "vulTask"

# Celery配置
class CeleryConfig(RedisConfig):
    BROKER_URL = "redis://:{0}@{1}:{2}/{3}".format(RedisConfig.PASSWORD, RedisConfig.HOST, RedisConfig.PORT, RedisConfig.BR)
    CELERY_TASK_SERIALIZER = "json"
    CELERY_TIMEZONE = "Asia/Shanghai"
