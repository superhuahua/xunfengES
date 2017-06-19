import urllib2

from tasks import hostScan, hostVerify, vulPocCheck, vulScriptCheck
from common import get_ip_list

def api_hostScan(hostsList, ports, arguments='-Pn -sV', queue="master"):
    """
    hosts: 192.168.1.1-192.168.1.128,192.168.1.129-192.168.1.130
    arguments: -Pn -sV
    """
    hostsList = hostsList.split(",")
    for hostsQ in hostsList:
        if hostsQ.find("|") != -1:
            hosts, queue = hostsQ.split("|")
        else:
            hosts, queue = (hostsQ, "master")
        ipList = get_ip_list(hosts)
        for v in ipList:
            hostScan.apply_async(args=[v, ports, arguments, queue], queue=queue)
    return True

def api_hostVerify(host, port, queue="master"):
    """
        host: 192.168.1.1
        port: 80
    """
    hostVerify.apply_async(args=[host, port, queue], queue=queue)
    return True

def api_vulPoc(task_id, task_name, netloc, pluginInfo):
    # .json payload
    # for v in netlocList
    for item_netloc in netloc:
        vulPocCheck.apply_async(args=[task_id, task_name, item_netloc, pluginInfo, item_netloc["queue"]], queue=item_netloc["queue"])

def api_vulScript(task_id, task_name, netloc, pfileName, passDic):
    #.py scripts
    # for v in netlocList
    for item_netloc in netloc:
        vulScriptCheck.apply_async(args=[task_id, task_name, item_netloc, pfileName, passDic, item_netloc["queue"]], queue=item_netloc["queue"])