#coding: utf8
from Config import ElasticConfig
from es import Es
from vulscan import vulScan

if __name__ == '__main__':
    es = Es()
    #初始化周期扫描配置
    es.init_scan_config()
    #初始化vultask脚本
    vulScan.init()
    print 'es初始化完成'