#coding: utf8
import json
import os
import sys
import re
import uuid
from datetime import datetime
from urllib import unquote, urlopen, urlretrieve, quote
from flask import request, render_template, session, jsonify
from flask import redirect, url_for, make_response
from werkzeug.utils import secure_filename

from vulscan import vulScan
from common import cleanPostData
from lib.Login import logincheck
from es import Es

from Index import app

sys.path.append(os.path.split(os.path.realpath(__file__))[0]+"/../")
from celerynode.api import api_hostScan, api_vulPoc, api_vulScript
from redispool import getStrictRedis

es = Es()
FILE_PATH = os.path.split(os.path.realpath(__file__))[0] + '/vulscan/vuldb/'

#返回es中扫描配置
@app.route('/taskconfig/all', methods=['get','post'])
def AllConfig():
    defaultConfig = es.get_scan_config()
    scanHosts = defaultConfig["scanHosts"].split(",")
    if request.json is None:
        return jsonify({
            "scanHosts":scanHosts,
            "scanPeriod": defaultConfig["scanPeriod"],
            "scanThreads":defaultConfig["scanThreads"], 
            "scanCMS":defaultConfig["scanCMS"],
            "scanPorts":defaultConfig["scanPorts"]
        })
    else:
        scanHosts = cleanPostData(request.json.get('scanHosts'))
        scanPeriod = cleanPostData(request.json.get('scanPeriod'))
        scanPorts = cleanPostData(request.json.get('scanPorts'))
        es.update_scan_config("scanHosts", scanHosts)
        es.update_scan_config("scanPeriod", scanPeriod)
        es.update_scan_config("scanPorts", scanPorts)
        return jsonify({"message":"ok"})

#返回搜索结果
@app.route('/vultask/search', methods=['post'])
@logincheck
def VulTaskSearch():
    value = cleanPostData(request.json.get('searchValue'))
    try:
        searchGroup = []
        for item in value.split(";"):
            (n, v) = item.split(":")
            searchGroup.append({"match" : { n: v } })
        rg = es.get_assets_doc(searchGroup)
        searchResult = []
        if rg:
            count = 0
            for v in rg:
                searchResult.append(v["_source"])
                count += 1
        return jsonify({"searchResult":searchResult, "count":count})
    except:
        pass

#返回所有脚本
@app.route('/vultask/getplugins', methods=['get'])
@logincheck
def VulTaskGetPlugins():
    all_plugins = [x for x in es.get_all_plugins()]
    try:
        return jsonify({"vulPlugins": all_plugins})
    except:
        pass

@app.route('/login', methods=['get','post'])
def Login():
    return render_template('login.html')

@app.route('/loginUp', methods=['post'])
def LoginUp():
    username = request.json.get('username')
    password = request.json.get('password')

    if username == app.config.get('USERNAME') and password == app.config.get('PASSWORD'):
        session['login'] = 'loginsuccess'
        return jsonify({"message":"ok"})
    else:
        return jsonify({"message":"error"})

@app.route('/loginOut', methods=['post'])
@logincheck
def loginOut():
    session['login'] = ''
    return jsonify({"message":"ok"})

@app.route('/')
@logincheck
def Index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404

@app.route('/setHostScan', methods=['post'])
@logincheck
def setHostScan():
    defaultConfig = es.get_scan_config()
    value = cleanPostData(request.json.get("scan_hosts"))
    hostsList, ports = (value, defaultConfig["scanPorts"])
    if api_hostScan(hostsList=hostsList, ports=ports):
        return jsonify({"message":"ok"})
    else:
        return jsonify({"message":"error"})

@app.route('/setVulScan', methods=['POST'])
@logincheck
def setVulScan():
    #get vultaskName,vultaskPlugin
    try:
        tid = uuid.uuid1()
        netloc = request.json.get('vul_task_netloc')
        name = request.json.get('vul_task_name')
        plugin_ids = request.json.get('vul_task_plugin_id')
        passDic = ["admin","root"]
        queue = "master"
        #vul class param:task_id, task_netloc, task_plugin, passDic, task_queue
        for plugin_id in plugin_ids:
            vulScan.vulscan(tid, name, netloc, plugin_id, passDic)
        return jsonify({"message":"ok"})
    except Exception as e:
        pass

@app.route('/uploadPlugins', methods=['POST'])
@logincheck
def uploadPlugins():
    f = request.files['file']
    file_name = ''
    try:
        if f:
            fname = secure_filename(f.filename)
            if fname.split('.')[-1] == 'py':
                path = FILE_PATH + fname
                if os.path.exists(FILE_PATH + fname):
                    fname = fname.split('.')[0] + '_' + str(datetime.now().second) + '.py'
                    path = FILE_PATH + fname
                f.save(path)
                if os.path.exists(path):
                    file_name = fname.split('.')[0]
                    # redis publish
                    with open(path) as pf:
                        r = getStrictRedis()
                        r.publish('updateplugins', json.dumps({"filename":file_name+".py", "content":pf.read()}))
                    # update esplugins
                    vulScan.updatePlugins(file_name)
        return jsonify({"message":"ok"})
    except Exception as e:
        pass
