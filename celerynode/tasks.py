#coding:utf-8
import os
import sys
import nmap
import json
import md5
import socket
import urllib2
import re
from celery import Celery

from redispool import *
from common import get_id_md5, get_code, set_request
from Config import CeleryConfig, RedisConfig
reload(sys)
sys.setdefaultencoding('utf8')

sys.path.append(os.path.split(os.path.realpath(__file__))[0] + '/vuldb')

app = Celery('tasks')
app.config_from_object(CeleryConfig)

@app.task
def hostScan(host, ports, arguments, queue):
    """
    host - 单台主机: 127.0.0.1
    ports - 多个端口: 21,22,135,137,445,3389
    arguments - 扫描参数: -Pn -sV
    """
    try:
        nm = nmap.PortScanner()
        nm.scan(hosts=host, ports=ports, arguments=arguments)

        if "tcp" in nm[host].all_protocols():
            for port in nm[host]["tcp"].keys():
                if nm[host]["tcp"][port]["state"] == "open":
                    #nm[host]["tcp"][port]["extrainfo"] match codes
                    pattern = re.compile('(php)|(aspx?)|(jsp)|(python)', re.I)
                    match = pattern.search(nm[host]["tcp"][port]["extrainfo"])
                    if match:
                        codes = match.group().lower()
                    else:
                        codes = ""
                    result = {
                        "id": get_id_md5(host, port),
                        "tags": "hostScan",
                        "host": host,
                        "port": port,
                        "product": nm[host]["tcp"][port]["product"],
                        "state": nm[host]["tcp"][port]["state"],
                        "version": nm[host]["tcp"][port]["version"],
                        "server": nm[host]["tcp"][port]["name"],
                        "codes": codes,
                        "extrainfo": nm[host]["tcp"][port]["extrainfo"],
                        "reason": nm[host]["tcp"][port]["reason"],
                        "cpe": nm[host]["tcp"][port]["cpe"],
                        "queue": queue
                    }
                    getPoolBR().lpush(RedisConfig.HOSTSCANKEY, json.dumps(result))
    except Exception as e:
        pass

@app.task
def hostVerify(host, port, queue):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((host, port))
        return True
    except Exception as e:
        result = {
            "id": get_id_md5(host, port),
            "tags": "hostScan",
            "host": host,
            "port": port,
            "product": None,
            "state": "closed",
            "version": None,
            "name": None,
            "extrainfo": None,
            "reason": None,
            "cpe": None,
            "queue": queue
        }
        getPoolBR().lpush(RedisConfig.HOSTSCANKEY, json.dumps(result))
        return False

@app.task
def vulPocCheck(task_id, task_name, netloc, pluginInfo, queue):
    netloc = [netloc["host"],netloc["port"]]
    poc_request = set_request(netloc, pluginInfo)
    try:
        res = urllib2.urlopen(poc_request, timeout=5)
        res_html = res.read(204800)
        header = res.headers
    except urllib2.HTTPError as e:
        header = e.headers
        res_html = e.read(204800)
    except Exception as e:
        return
    try:
        html_code = get_code(header, res_html).strip()
        if html_code and len(html_code) < 12:
            res_html = res_html.decode(html_code).encode('utf-8')
    except Exception as e:
        pass

    an_type = pluginInfo['analyzing']
    vul_tag = pluginInfo['tag']
    analyzingdata = pluginInfo['analyzingdata']

    vul_scan_result = {
        "tags": "vulTask",
        "task_id": task_id,
        "task_name": task_name,
        "host": netloc[0],
        "port": netloc[1],
        "queue": queue,
        "isvul": False
    }

    if an_type == 'keyword':
        if analyzingdata.encode("utf-8") in res_html:
            vul_scan_result["isvul"] = '存在漏洞'
    elif an_type == 'regex':
        if re.search(analyzingdata, res_html, re.I):
            vul_scan_result["isvul"] = '存在漏洞'
    elif an_type == 'md5':
        md5 = hashlib.md5()
        md5.update(res_html)
        if md5.hexdigest() == analyzingdata:
            vul_scan_result["isvul"] = '存在漏洞'
    else:
        vul_scan_result["isvul"] = None
    getPoolBR().lpush(RedisConfig.VULTASKKEY, json.dumps(vul_scan_result))

@app.task
def vulScriptCheck(task_id, task_name, netloc, pfileName, passDic, queue):
    netloc = [netloc["host"],netloc["port"]]
    timeout = 20
    plugin_res = __import__(pfileName)
    setattr(plugin_res, "PASSWORD_DIC", passDic)  # 给插件声明密码字典
    try:
        result = plugin_res.check(netloc[0], int(netloc[1]),timeout)
        vul_scan_result = {
            "tags": "vulTask",
            "task_id": task_id,
            "task_name": task_name,
            "host": netloc[0],
            "port": netloc[1],
            "pfileName": pfileName,
            "queue": queue,
            "isvul": result
        }
        getPoolBR().lpush(RedisConfig.VULTASKKEY, json.dumps(vul_scan_result))
    except Exception as e:
        pass
