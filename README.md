# Base xunfeng

## 安装环境依赖

    * Python 2.7.5+ 

    * Nmap

    * ELK（elasticsearch、logstash、kibana）

    * Redis

## 部署流程

### 下载xfes

`git clone https://github.com/superhuahua/xunfengES.git`

### 安装python的nmap插件（服务端、节点）

`sudo pip install python-nmap`

### Server (服务端)

```
pip install elasticsearch==5.4.0 //安装python的es插件

cd xunfengES/server
python esinit.py  //初始化es配置
python run.py //启动服务端
sudo python monitor/index.py //启动周期验证,无资产数据时报错,可忽略报错
```

### Celery node（节点）

```
sudo pip install redis celery celery[redis] //安装redis，celery模块
cd xunfengES
celery worker -A celerynode.tasks -E -n node1 -Q master -c 5  //启动celery
python subscribe.py //启动订阅redis，接收更新插件
```

### Flower

```
sudo pip instal flower

flower --broker=redis://:Password@localhost:6379/1 --basic_auth=test:123456 --address=127.0.0.1 --port=5555 //启动flower

flower --broker=redis://localhost:6379/0 --address=127.0.0.1 --port=5555 //不带认证启动

```

### redis

```
wget http://download.redis.io/releases/redis-3.2.8.tar.gz
tar xzf redis-3.2.8.tar.gz
cd redis-3.2.8
make
```

修改`/etc/redis.conf`为

```
bind 0.0.0.0
```

启动redis：`src/redis-server /etc/redis.conf`

### Elasticsearch
下载ES: <https://www.elastic.co/downloads/elasticsearch>

解压之后以普通用户运行: `bin/elasticsearch`

### Logstash
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

以上文件保存为`/etc/logstash.conf`

下载logstash:

<https://www.elastic.co/downloads/logstash>

启动logstash: `bin/logstash -f /etc/logstash.conf`


### Kibana

下载: <https://www.elastic.co/downloads/kibana>

运行: `bin/kibana`

### 前端

* flower查看task状态

* kibana配置视图，面板

* 懒得重新打包前端, 可自行修改index.js中localhost:5555、localhost:5601

### 文件结构说明

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