import os
import sys
import time

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/../../")
from server.Config import ElasticConfig
from celerynode.api import api_hostVerify

def portCheck(es, test):
    while True:
        data = es.getAllData()
        for item in data:
            host = item["_source"]["host"]
            port = item["_source"]["port"]
            queue = item["_source"]["queue"]
            api_hostVerify(host, port, queue)
    time.sleep(1800)