# coding:utf-8
import time
import json
import os
import sys
from redispool import getStrictRedis
reload(sys)
sys.setdefaultencoding('utf-8') 

FILE_PATH = os.path.split(os.path.realpath(__file__))[0] + '/vuldb/'

if __name__ == '__main__':
    r = getStrictRedis()
    p = r.pubsub()
    p.subscribe("updateplugins")
    while True:
        try:
            message = p.get_message()
            if message:
                m = json.loads(message["data"])
                filename = m["filename"]
                content = m["content"]
                f = open(FILE_PATH + filename, "w")
                f.write(content)
                f.close()
            time.sleep(10)      
        except Exception as e:
            pass
