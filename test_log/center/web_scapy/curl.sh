curl -XPOST 'http://172.16.1.147:9200/201708-openstack_log/_search?pretty' -d '


 {
          "query": {
            "filtered": {
              "query": { "match_all": {} },
              "filter": {
                "range": {
                  "logdate": {
                    "gte": "2017-08-24 05:30:38.916",
                    "lte": "2017-08-24 05:30:39.916"
                            }
                            }
                         }
                        }
                    }
                }
'
