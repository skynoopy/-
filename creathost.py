
# coding=UTF-8

from flask import Flask,request
app = Flask(__name__)


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
    # 将参数串排序
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

def requesturl(hostname, cpu, mem, disk):
    requrl = {
        "Action": "CreateUHostInstance",
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
        "Disks.1.Size": disk + "G",

        "LoginMode": "Password",
        "Name": hostname,
        "ChargeType": "Dynamic",
        "UHostType": "N2",
        "CPU": cpu,
        "Memory": mem,
        "VPCId": "uvnet-w4ciux",
        "SubnetId": "subnet-5dc25p",
        "Tag":"fudao",
        "Remark": "wenba"
    }
    print(requrl)

    # 公钥
    publickey = {'PublicKey': 'd+OjKD0rgaqxZWwaa9Nev4pQeAlhsiht4B9EgYDBGn5IbmvN'}
    #私钥
    private = 'd186ba62dad44a55ee8e4da1a873c51aee64737e'
    http_url = 'https://api.ucloud.cn/?'
    base_url = _verfy_ac(requrl, publickey, private)


    r = requests.get(url=http_url, params=base_url)
    v = r.text






#dingtalk notic
def dingtalk():
    headers = {'content-type': 'application/json'}
    web_url = 'https://oapi.dingtalk.com/robot/send?access_token=ace2f9d401307aa116fe162ff7946e19c893761eab4115d597792fffd0e1a1e2'
    parse = {"msgtype": "text", "text": {"content": "主机创建成功了 %s " %('孟海亮') }}
    r = requests.post(web_url,  data=json.dumps(parse), headers=headers)
    print(r.text)

@app.route('/hello/<name>')
def hello(name):
     kk = requesturl(name)
     # dd = dingtalk()
     # return "300"

@app.route('/create_host/', methods=['GET','POST'])
def create_host():
    if request.method == 'POST':
        hostname = request.form.get('hostname')
        cpu = int(request.form.get('cpu', 2))
        mem = int(request.form.get('mem', 4096))
        disk = str(request.form.get('disk', '500'))

        value = len(str(mem))
        if value == 1:mem = mem * 1024

        requesturl(hostname, cpu, mem, disk)
        return "hostname:{},cpu:{},mem:{},disk:{}".format(hostname, cpu, mem, disk)
        dt = dingtalk()
        return "200"

    else:
        hostname = request.args.get('hostname')
        cpu = int(request.args.get('cpu',2))
        mem = int(request.args.get('mem',4096))
        disk = request.args.get('disk', "500G")

        value = len(str(mem))
        if value == 1:mem = mem * 1024

        requesturl(hostname, cpu, mem, disk)
        return "hostname:{},cpu:{},mem:{},disk:{}".format(hostname, cpu, mem, disk)
        dt = dingtalk()
        return "200"


if __name__ == "__main__":
    app.run(host='0.0.0.0')