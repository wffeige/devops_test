import urllib
import urllib2


data={
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
data = urllib.urlencode(data)

# requrl = "http://192.168.81.16/cgi-bin/python_test/test.py"
requrl = "http://172.16.1.147:9200/201708-openstack_log/_search?pretty"

req = urllib2.Request(url = requrl,data =data)
print req

res_data = urllib2.urlopen(req)
res = res_data.read()
print res

