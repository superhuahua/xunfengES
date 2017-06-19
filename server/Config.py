#coding: utf8

class ServerConfig(object):
    USERNAME = "test"
    PASSWORD = "test"

class RedisConfig(object):
    HOST = "localhost"
    PORT = 6379
    PASSWORD = ""
    BR = 1
    HOSTSCANKEY = "hostScan"
    VULTASKKEY = "vulTask"

class ElasticConfig(object):
    HOST = "localhost"
    PORT = "9200"
    USERNAME = ""
    PASSWORD = ""
    INDEX_CONFIG = {"index":"xfconfig", "type":"logs"}
    INDEX_ASSETS = {"index":"assets",  "type":"logs"}
    INDEX_VULTASKS = {"index":"vulscan",  "type":"data"}