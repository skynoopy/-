from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
bp = Blueprint('create_uhost_modus', __name__)




import hashlib
import urllib
from urllib.parse import urlparse
from urllib.parse import urlencode
import requests
import threading
import  sqlite3
import json


def _verfy_ac(param, publickey, private):
    pp = dict(param, **publickey)
    # print(pp)
    items = list(pp.items())
    items.sort()
    # # 将参数串排序
    params_data = "";
    httpurl = "";
    transfered = "";
    transfer = "";
    # header = 'https://api.ucloud.cn/?'
    for key, value in items:
        params_data = params_data + str(key) + str(value)
        # print(params_data)
        if str(key) == 'PublicKey':
            transfer = {str(key): str(value)}
            # print(transfer)

            continue
        else:
            transfered = urlencode(transfer)
            httpurl = httpurl + str(key) + '=' + str(value) + '&'

    params_data = params_data + private

    sign = hashlib.sha1()
    sign.update(params_data.encode("utf8"))
    signature = sign.hexdigest()
    # print(signature)
    # httpurl = header + httpurl + transfered +  '&Signature=' + signature
    httpurl = httpurl + transfered + '&Signature=' + signature
    # print (signature)
    # print(httpurl)
    return httpurl


requesturl = {
    "Action": "CreateUHostInstance",
    # "PublicKey":"d+OjKD0rgaqxZWwaa9Nev4pQeAlhsiht4B9EgYDBGn5IbmvN",
    "ProjectId": "org-sjdken",
    "Region": "cn-bj2",
    "Zone": "cn-bj2-03",
    "ImageId": "uimage-3n0bue",
    "Password": "V2VuQmEwNjMwIUAj",

    "Disks.0.IsBoot": "True",
    "Disks.0.Type": "LOCAL_NORMAL",
    "Disks.0.Size": "20G",
    "Disks.1.IsBoot": "False",
    "Disks.1.Type": "LOCAL_NORMAL",
    "Disks.1.Size": "500G",

    "LoginMode": "Password",
    "Name": "ucloud-api-test",
    "ChargeType": "Dynamic",
    "UHostType": "N2",
    "CPU": 2,
    "Memory": 4096,
    "VPCId": "uvnet-w4ciux",
    "SubnetId": "subnet-5dc25p",
    "Tag":"fudao",
    # "AlarmTemplateId": "",
    "Remark": "wenba"
}

# 公钥
publickey = {'PublicKey': 'd+OjKD0rgaqxZWwaa9Nev4pQeAlhsiht4B9EgYDBGn5IbmvN'}
# #私钥
private = 'd186ba62dad44a55ee8e4da1a873c51aee64737e'
http_url = 'https://api.ucloud.cn/?'
base_url = _verfy_ac(requesturl, publickey, private)

# r = requests.get(url=http_url, params=base_url)
# print(r.url)
# print(r.text)


conn = sqlite3.connect('/Users/gz0101000646/flaskk/instance/pages.db')
c = conn.cursor()

def create_uhost():
    for i in range(1, 2):
        r = requests.get(url=http_url, params=base_url)
        #
        r_tag = json.loads(r.text)
        #r_tag = {"RetCode":0,"Action":"CreateUHostInstanceResponse","UHostIds":["uhost-m0cbnaaq"],"IPs":["192.168.11.46"]}

        print (type(r_tag))

        r_tag_value = r_tag['RetCode']
        print(r_tag_value)

        #提交api返回值入库
        stus = c.execute(

            "insert  into create_host  (r_tag_value) values ('%d')" %(r_tag_value)
        )
        conn.commit()

kk = create_uhost()

def creat_uhost_num(num):

    threads = []
    for i in range(1, num + 1):
        t1 = threading.Thread(target=create_uhost())
        threads.append(t1)

    for t in threads:
        t.start()


@bp.route('/create_effective/', methods=['POST','GET'])
def create_effective():



    recv_data = request.get_data()
    print(recv_data)

    #传递需要创建主机数量 默认创建一台
    creat_uhost_num(1)

    #获取api 值
    tag_value = c.execute(

        'select r_tag_value from create_host order by id desc limit 1'
    ).fetchone()[0]
    print(tag_value)



#     #获取Api返回值，如果返回0 则将返回成功信息给js，否则异然
    if tag_value != 0:
       tag = 1
       tag_s = json.dumps(tag)
       return  tag_s
    else:
       tag = 0
       tag_s = json.dumps(tag)
       return tag_s








