## Base xunfeng

## Python 2.7.5+

* 低版本python貌似celery会报错

* pip install elasticsearch (elasticsearch-5.4.0,不然help.scan会报错)

## nmap

* 安装最新版本nmap(节点、server)

* sudo pip install python-nmap

## Server (flask 、 react + atnd)
    
* 初始化es配置: python esinit.py 

* 启动服务端: sudo python run.py

* 启动周期验证: sudo python monitor/index.py 

## Celery node

* sudo pip install redis celery celery[redis]

* 部署开启即可

* 建议使用supervisor管理

* 启动worker定义队列和worker名称：celery worker -A celerynode.tasks -E -n node1 -Q master -c 5 &>/dev/null &

* 启动订阅redis,接收更新插件: python subscribe.py 

## Flower

* 监控celery队列，查看tasks运行情况

* sudo pip install flower

* 启动flower：flower --broker=redis://:Password@localhost:6379/0 --basic_auth=test:123456 --address=127.0.0.1 --port=5555

* 不带认证启动：flower --broker=redis://localhost:6379/0 --address=127.0.0.1 --port=5555

## logstash
<pre>
input{
    redis {
        host => "localhost"
        data_type => "list"
        key => "hostScan"
        db => 1
    }
    redis {
        host => "localhost"
        data_type => "list"
        key => "vulTask"
        db => 1
    }
}
filter{}
output{
    if [tags] == "hostScan" {
        elasticsearch {
            hosts => ["localhost"]
            index => "assets"
            document_id => "%{id}"
        }       
    }

    if [tags] == "vulTask" {
        elasticsearch {
            hosts => ["localhost"]
            index => "vultask"
        }
    }
}
</pre>

## 前端

* flower查看task状态

* kibana配置视图，面板

* 懒得重新打包前端, 可自行修改index.js中localhost:5555、localhost:5601

## 文件结构说明

    celerynode
    |
    |-- vuldb 漏洞扫描脚本库
    |
    |-- api.py 提供server调用tasks
    |
    |-- tasks.py 芹菜任务列表
    |
    |-- common.py 公用函数库
    |
    |-- subscribe.py 接收更新插件
    |
    |-- Config.py 芹菜配置
    
    server
    |
    |-- lib 
    |
    |-- static 静态文件
    |
    |-- templates html页面
    |
    |-- vul 漏洞扫描引擎
        |
        |-- vuldb 漏洞扫描脚本库
        |
        |-- vulScan.py 漏洞扫描脚本引擎
    |
    |-- monitor 周期验证引擎
        |
        |-- index.py 周期nmap扫描
        |
        |-- verify.py 周期探测port
    |
    |-- Config.py 服务端配置
    |
    |-- Routes.py 处理web请求
    |
    |-- run.py 启动flask
    |
    |-- esinit.py 初始化es配置

## 后续功能

* 主机扫描cidr

* 插件password字典

* 服务识别