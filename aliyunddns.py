from datetime import datetime
import schedule
import time
from requests import get
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordInfoRequest import DescribeDomainRecordInfoRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from json import loads

client = AcsClient('AccessKey ID','AccessKey Secret', 'cn-hangzhou')
recordId = 'recordId'


def ylog(m):
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(t+':'+m)
	
def operate():
    url = 'http://www.3322.org/dyndns/getip'
    res = get(url)
    ylog('当前ip：' + res.text.strip())
    return res.text.strip()


def getParsingRecords():
    request = DescribeDomainRecordInfoRequest()
    request.set_accept_format('json')
    request.set_RecordId(recordId)
    response = client.do_action_with_exception(request)
    obj = loads(str(response, encoding='utf-8'))
    ylog('当前解析ip：' + obj['Value'])
    return obj['Value']


def editParsingRecords(ip):
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')
    request.set_RecordId(recordId)
    request.set_RR("k")
    request.set_Type("A")
    request.set_Value(ip)
    response = client.do_action_with_exception(request)
    ylog(str(response, encoding='utf-8'))


def func():
    try:
        # 当前ip
        locip = operate()
        # 当前解析ip
        netip = getParsingRecords()
        if locip != netip:
            editParsingRecords(locip)
        else:
            ylog('ip相同')
    except Exception as ex:
        print("出现如下异常%s"%ex)
    else:
        pass


def tasklist():
    ylog("开始...")
    # 先执行一次
    func()
    #清空任务
    schedule.clear()
    #创建
    schedule.every(10).minutes.do(func)
    while True:
        schedule.run_pending()
        time.sleep(1)


tasklist()