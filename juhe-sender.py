#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO: 优化定时器
# TODO: API错误码识别
# TODO: 引入Logging
import uuid
import datetime
import random
import json
import urllib
import time
from urllib import urlencode
from azure.servicebus import ServiceBusService


def main():
    appkey = "24000e5c1b5338a94f68ce841d975f8a" # juhe-api 

    # Azure service
    sbs = ServiceBusService(service_namespace='brucewaynetolltooth', shared_access_key_name='RootManageSharedAccessKey', shared_access_key_value='m6mWS29LUMIh2ZH9gh4KjmoNPiXBxeMCaq6eMxojBDc=')

    while True:
        print("Query starts...")
        page_quantity_query = 10 # 请求页数
        for page in range(1,page_quantity_query):
            api_result = request4(appkey, "GET", page) # 香港股市列表
            s = json.dumps(api_result)
            sbs.send_event('entrysignals', s)
        time.sleep(60) # 1000次每日限额，每1分钟请求10次，100分钟用完


#沪深股市
def request1(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/finance/stock/hs"
    params = {
        "gid" : "sh601009", #股票编号，上海股市以sh开头，深圳股市以sz开头如：sh601009
        "key" : appkey, #APP Key
 
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
 
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            return res["result"]
           
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
            return None
    else:
        print "request api error"
        return None
 
#香港股市
def request2(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/finance/stock/hk"
    params = {
        "num" : "00001", #股票代码，如：00001 为“长江实业”股票代码
        "key" : appkey, #APP Key
 
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
 
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            return res["result"]
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
            return
    else:
        print "request api error"
        return
 
#美国股市
def request3(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/finance/stock/usa"
    params = {
        "gid" : "aapl", #股票代码，如：aapl 为“苹果公司”的股票代码
        "key" : appkey, #APP Key
 
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
 
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            return res["result"]
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
            return None
    else:
        print "request api error"
        return None
 
#香港股市列表
def request4(appkey, m="GET", page=1):
    """
    成功请求api返回json格式为以下result键值：
    {
        "error_code": 0,
        "reason": "SUCCESSED!",
        "result": {
            "totalCount": "273", /*总条数*/
            "page": "2", /*当前页数*/
            "num": "20", /*显示条数*/
            "data": [
                {
                    "symbol": "00066", /*代码*/
                    "name": "港铁公司",/*名称*/
                    "engname": "MTR CORPORATION",/*英文名*/
                    "lasttrade": "35.900",/*最新价*/
                    "prevclose": "36.100",/*昨收*/
                    "open": "35.900",/*今开*/
                    "high": "35.900",/*最高*/
                    "low": "35.900",/*最低*/
                    "volume": "178000",/*成交量*/
                    "amount": "6389923",/*成交额*/
                    "ticktime": "2015-07-02 09:20:00",/*时间*/
                    "buy": "35.800",/*买入*/
                    "sell": "35.900",/*卖出*/
                    "high_52week": "40.000",/*52周最高*/
                    "low_52week": "29.250",/*52周最低*/
                    "stocks_sum": "5839612547",/*总股本*/
                    "pricechange": "-0.200",/*涨跌额*/
                    "changepercent": "-0.5540166"/*涨跌幅*/
                },
    ...}]
    """
    url = "http://web.juhe.cn:8080/finance/stock/hkall"
    params = {
        "key" : appkey, #您申请的APPKEY
        "page" : page, #第几页,每页20条数据,默认第1页
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
 
    content = f.read()
    res = json.loads(content)
    #return res
    
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            print res["result"]
            return res["result"]
        else:
            return None
    else:
        print "request api error"
        return None
 
#美国股市列表
def request5(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/finance/stock/usaall"
    params = {
        "key" : appkey, #您申请的APPKEY
        "page" : "", #第几页,每页20条数据,默认第1页，
        "type": 4 # 每页80条数据
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
 
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            return res["result"]
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
            return None
    else:
        print "request api error"
        return None
 
#深圳股市列表
def request6(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/finance/stock/szall"
    params = {
        "key" : appkey, #您申请的APPKEY
        "page" : "", #第几页(每页20条数据),默认第1页
 
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
 
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            return res["result"]
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
            return None
    else:
        print "request api error"
        return None
 
#沪股列表
def request7(appkey, m="GET"):
    url = "http://web.juhe.cn:8080/finance/stock/shall"
    params = {
        "key" : appkey, #您申请的APPKEY
        "page" : "", #第几页,每页20条数据,默认第1页
 
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)
 
    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            return res["result"]
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
            return None
    else:
        print "request api error"
        return None
 
 
if __name__ == '__main__':
    main()