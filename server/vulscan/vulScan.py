# coding:utf-8
import os
import sys
import urllib2
import time
import datetime
import hashlib
import json
import re
import uuid

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/../../")
from celerynode.api import api_vulPoc, api_vulScript
from server.es import Es

PASSWORD_DIC = []
PLUGIN_DB = {}
TASK_DATE_DIC = {}
WHITE_LIST = []

es = Es()

class vulscan():
    def __init__(self, task_id, task_name, task_netloc, task_plugin_id, passDic):
        self.task_id = task_id
        self.task_name = task_name
        self.task_netloc = task_netloc
        self.task_plugin_id = task_plugin_id
        self.passDic = passDic
        self.start()

    def start(self):
        self.get_plugin_info()
        if self.get_plugin_info:
            if '.json' in self.plugin_info['filename']:
                try:
                    self.load_json_plugin()
                    self.poc_check()
                except Exception as e:
                    return None
            else:
                try:
                    self.script_check()
                except Exception as e:
                    return None

    def get_plugin_info(self):
        info = es.get_plugins_doc("_id", self.task_plugin_id) 
        self.plugin_info = info
        
    def load_json_plugin(self):
        json_plugin = open(sys.path[0] + '/vulscan/vuldb/' + self.plugin_info['filename']).read()
        self.plugin_info['plugin'] = json.loads(json_plugin)['plugin']

    def poc_check(self):
        task_id = self.task_id
        task_name = self.task_name
        netloc = self.task_netloc
        pluginInfo = self.plugin_info['plugin']
        api_vulPoc(task_id=task_id, task_name=task_name, netloc=netloc, pluginInfo=pluginInfo)

    def script_check(self):
        task_id = self.task_id
        task_name = self.task_name
        netloc = self.task_netloc
        pfileName = self.plugin_info['filename']
        passDic = self.passDic
        api_vulScript(task_id=task_id, task_name=task_name, netloc=netloc, pfileName=pfileName, passDic=passDic)

def updatePlugins(plugin_name):
    try:
        time_ = datetime.datetime.now()
        res_tmp = __import__('server.vulscan.vuldb.'+plugin_name, globals(), locals(), ["get_plugin_info"], -1)
        plugin_info = res_tmp.get_plugin_info()
        plugin_info['add_time'] = time_
        plugin_info['filename'] = plugin_name
        es.insert_plugins_doc(plugin_info)
    except Exception as e:
        pass
         
def init():
    es.init_plugins() # 创建es插件库
    script_plugin = []
    json_plugin = []
    file_list = os.listdir(sys.path[0] + '/vulscan/vuldb/')
    time_ = datetime.datetime.now()

    for filename in file_list:
        try:
            if filename.split('.')[1] == 'py':
                script_plugin.append(filename.split('.')[0])
            if filename.split('.')[1] == 'json':
                json_plugin.append(filename)
        except:
            pass
    for plugin_name in script_plugin:
        try:
            res_tmp = __import__('server.vulscan.vuldb.'+plugin_name, globals(), locals(), ["get_plugin_info"], -1)
            plugin_info = res_tmp.get_plugin_info()
            plugin_info['add_time'] = time_
            plugin_info['filename'] = plugin_name
            es.insert_plugins_doc(plugin_info)
        except Exception as e:
            pass

    for plugin_name in json_plugin:
        try:
            json_text = open(sys.path[0] + '/vulscan/vuldb/' + plugin_name, 'r').read()
            plugin_info = json.loads(json_text)
            plugin_info['add_time'] = time_
            plugin_info['filename'] = plugin_name
            del plugin_info['plugin']
            es.insert_plugins_doc(plugin_info)
            jcount+=1
        except:
            pass