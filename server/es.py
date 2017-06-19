from elasticsearch import Elasticsearch
from elasticsearch import helpers
from Config import ElasticConfig

SCANCONFIG = {
    "scanHosts": "",
    "scanPeriod": "1|6",
    "scanThreads":"20", 
    "scanCMS":"",
    "scanPorts":"21,22,23,25,53,80,110,139,143,389,443,445,465,873,993,995,1080,1311,1723,1433,1521,3000,3001,3002,3306,3389,3690,4000,5432,5900,6379,7001,8000,8001,8080,8081,8888,9200,9300,9080,9090,9999,11211,27017"
}

class Es():
    def __init__(self):
        USERNAME = ElasticConfig.USERNAME
        PASSWORD = ElasticConfig.PASSWORD
        HOST = ElasticConfig.HOST
        PORT = ElasticConfig.PORT
        if USERNAME == "" and PASSWORD == "":
            CONN = "http://"+HOST+":"+PORT
        else:
            CONN = "http://"+USERNAME+":"+PASSWORD+"@"+HOST+":"+PORT
        self.es = Elasticsearch([CONN])
        self.confIndex = ElasticConfig.INDEX_CONFIG["index"]
        self.confType = ElasticConfig.INDEX_CONFIG["type"]
        self.assetIndex = ElasticConfig.INDEX_ASSETS["index"]
        self.assetType = ElasticConfig.INDEX_ASSETS["type"]

    def init_scan_config(self):
        doc = SCANCONFIG
        if self.es.exists(index=self.confIndex, doc_type=self.confType, id="1"):
            self.es.delete(index=self.confIndex, doc_type=self.confType, id="1")
        self.es.create(index=self.confIndex, doc_type=self.confType, id="1", body=doc)

    def get_scan_config(self):
        config = self.es.search(index=self.confIndex, doc_type=self.confType, body={
        "query":{
            "term" : { "_id" : "1" }
        }
    }, request_timeout=5)["hits"]["hits"]
        if len(config) == 0:
            return False
        else:
            return config[0]["_source"]

    def update_scan_config(self, name, value):
        self.es.update(index=self.confIndex, doc_type=self.confType, id="1", body={
            "doc":{
                name: value.strip()
            }    
        })
        return True

    #vulscan 
    def init_plugins(self):
        if self.es.indices.exists(ElasticConfig.INDEX_VULTASKS["index"]):
            self.es.indices.delete(ElasticConfig.INDEX_VULTASKS["index"])
        self.es.indices.create(ElasticConfig.INDEX_VULTASKS["index"])

    #vulscan
    def get_plugins_doc(self, name, value):
        v = self.es.search(index=ElasticConfig.INDEX_VULTASKS["index"], doc_type=ElasticConfig.INDEX_VULTASKS["type"], body={
            "query":{"term" : {  name : value}}
            }, request_timeout=5)["hits"]["hits"]
        
        if len(v) == 0:
            return False
        else:
            return v[0]["_source"]

    #vulscan
    def insert_plugins_doc(self, doc):
        self.es.index(index=ElasticConfig.INDEX_VULTASKS["index"], doc_type=ElasticConfig.INDEX_VULTASKS["type"], body=doc)
        return True

    #return data <type 'generator'>
    def get_all_plugins(self):
        index = ElasticConfig.INDEX_VULTASKS["index"]
        doc_type = ElasticConfig.INDEX_VULTASKS["type"]
        scroll = "2m"
        size = 30
        body = {"query" : {"match_all": {}}}
        data = helpers.scan(client=self.es, query=body, index=index, doc_type=doc_type, scroll=scroll, size=size)
        return data

    #search assets
    def get_assets_doc(self, searchGroup):
        index = self.assetIndex
        doc_type = self.assetType
        scroll = "5m"
        size = 100
        body = {"query":{"bool": {"must": searchGroup}}}
        data = helpers.scan(client=self.es, query=body, index=index, doc_type=doc_type, scroll=scroll, size=size)
        return data

if __name__ == '__main__':
    esconn = Es()
    count = 0
    searchGroup = {"match":{"port":"80"}}
    r = esconn.get_assets_doc(searchGroup)
    for v in r:
        print v
        count += 1
    print "-"*20
    print count