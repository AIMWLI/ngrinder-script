# -*- coding:utf-8 -*-

from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from java.util import Date
from HTTPClient import NVPair, Cookie, CookieModule
from net.grinder.util import GrinderUtils
from net.grinder.plugin.http import HTTPRequest
from net.grinder.plugin.http import HTTPPluginControl
import time,uuid,random,string
import json

control = HTTPPluginControl.getConnectionDefaults()

control.timeout = 60000

test1 = Test(1, "zhengzhaoshibie")
request1 = HTTPRequest()
headers = [] # Array of NVPair
headers.append(NVPair("Content-Type", "application/json"))
# ✿ 压测前，人工智能提供最新签名
headers.append(NVPair("sign", "93828b500cd2646b14944fa9b22e23ab78749e5543ef44b19619e167f0cd2943"))
json_body = {}

class TestRunner:
    def __init__(self):
        test1.record(TestRunner.__call__)
        grinder.statistics.delayReports=True
        pass

    def before(self):
        global json_body
        request1.setHeaders(headers)
        json_body=json.load(open("./resources/license-body.json",'r'))
        # ✿ 压测前，人工智能提供最新签名时间戳
        json_body["timestamp"] = 1720076995444
    #grinder.logger.info(str(json_body))

    # test method
    def __call__(self):
        self.before()
        result = request1.POST("http://10.201.62.152:8889/detection/api/ocr/license", json.dumps(json_body))
        if result.getStatusCode() == 200 :
            if json.loads(result.getText())["code"] != 1:
                grinder.logger.warn(result.getText())
                raise
            #grinder.logger.info(str(json.loads(result.getText())["code"] == 1 ))
            return
        elif result.getStatusCode() in (301, 302) :
            grinder.logger.warn("Warning. The response may not be correct. The response code was %d." %  result.getStatusCode())
            return
        else:
            raise