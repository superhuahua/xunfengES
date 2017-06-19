#coding:utf8
import re

def checkip(ip):  
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')  
    if p.match(ip):  
        return True  
    else:  
        return False

def cleanPostData(data):
    data = data.replace(" ","") # 去掉空格
    data = data.split("\n") # 去掉换行
    while "" in data:
        data.remove("")
    return ",".join(data)


