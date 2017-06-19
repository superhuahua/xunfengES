#coding:utf8
import sys
import os
import time
import thread

from verify import portCheck
sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/../../")
from server.es import Es
from celerynode.api import api_hostScan

if __name__ == "__main__":
    es = Es()  
    thread.start_new_thread(portCheck,(es, "test")) 
    try:
        ac_data = []
        while True:
            now_time = time.localtime()
            now_hour = now_time.tm_hour
            now_day = now_time.tm_mday
            now_date = str(now_time.tm_year) + str(now_time.tm_mon) + str(now_day)
            cy_day, ac_hour = es.get_scan_config()["scanPeriod"].split('|') #读取周期配置
            if now_hour == int(ac_hour) and now_day % int(cy_day) == 0 and now_date not in ac_data:
                ac_data.append(now_date)
                scanHosts = es.get_scan_config()["scanHosts"]
                scanPorts = es.get_scan_config()["scanPorts"]
                print (scanHosts, scanPorts)
                api_hostScan(hostsList=scanHosts, ports=scanPorts)
            time.sleep(60)
    except Exception, e:
        print e