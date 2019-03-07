# -*- coding: utf-8 -*-
'''
@File  : demo.py
@Date  : 2019/1/15/015 16:18
'''
from configparser import ConfigParser
import os
import json
import pytest_html
import hashlib

import requests

headers = {
    # "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A456 Safari/602.1",
    #
    "cookie":"DIS4=6461c3a4e5b14aa2af2ac2a8b50d2f4a",
    "User-Agent":"dogProj/2018101601 CFNetwork/811.4.18 Darwin/16.5.0",
    }
def make_sign(session_id, timestamp, plain_data):
    s = "/s5k/key.bootstrapa"\
         + "+X-QK-APPV=iPhone11,6|1570.120000|shadow.hirat.online|1.0.1"\
         + "+X-QK-AUTH=A9E5672E-92CF-4262-9AE8-32EC025B4782|f81f2d6c-40cf-4b75-bda3-63d4ead1df88|"\
         + "+X-QK-CDID=D2szej8SQavz6V+lQlLlhNsgn4rLJgKcXOxtWzdkI6VigXe5"\
         + "+X-QK-DIS=%s"\
         + "+X-QK-EXTENSION=12.2|1|1517bfd3f7ea41c4abc"\
         + "+X-QK-PUSH-STATE=1+X-QK-SCHEME=shadow.hirat.online"\
         + "+X-QK-TAG=<cc517135 7b7eef5d 24260b81 ba59e436 e9207875 cebabb76 c60acd01 4ecacf93>"\
         + "+X-QK-TIME=%s"\
         + "+X-QK-TOKEN=e39f7faf3b60d7790089fadfe24ea6b3"

    s = s % (session_id, timestamp)

    m = hashlib.md5()
    m.update(s.encode())
    # m.update(plain_data)

    return m.hexdigest().upper()
import time
# g=make_sign("DIS4=6461c3a4e5b14aa2af2ac2a8b50d2f4a",int(time.time()),"")
# print(g)
headers1={
    "cookie": "DIS4=6461c3a4e5b14aa2af2ac2a8b50d2f4a",
    "Referer":"http://fp01.ops.gaoshou.me/v4/tasks/lite",
    "Access-Control-Allow-Headers":"X-Qk-Auth, *",
    "User-Agent":"dogProj/2018101601 CFNetwork/811.4.18 Darwin/16.5.0",
    "X-QK-API-KEY":"c26007f41f472932454ea80deabd612c",
    "X-QK-APPV":"iPhone11,6|1570.120000|shadow.hirat.online|1.0.1",
    "X-QK-AUTH":"A9E5672E-92CF-4262-9AE8-32EC025B4782|f81f2d6c-40cf-4b75-bda3-63d4ead1df88|",
    # "X-QK-CDID":"D2szej8SQavz6V+lQlLlhNsgn4rLJgKcXOxtWzdkI6VigXe5",
    # "X-QK-DIS":"2cb350cd68c946e38ef17462d4137d94",
    # "X-QK-DSID":"25153182298",
    # "X-QK-EXTENSION":"12.2|1|1517bfd3f7ea41c4abc",
    # "X-QK-PUSH-STATE":"shadow.hirat.online",
    # "X-QK-SCHEME":"shadow.hirat.online",
    # "X-QK-SIGN":"11544D977DDFBB77382AACF90D6DD4A5",
    # "X-QK-TAG":"<cc517135 7b7eef5d 24260b81 ba59e436 e9207875 cebabb76 c60acd01 4ecacf93>",
    "X-QK-TIME":"1551406837",
    # "X-QK-TOKEN":"e39f7faf3b60d7790089fadfe24ea6b3"
}
def make_sign_with_headers():
    h="/s5k/key.bootstrapc26007f41f472932454ea80deabd612cX-QK-APPV=iPhone11,6|1570.120000|shadow.hirat.online|1.0.1" \
      "+X-QK-AUTH=A9E5672E-92CF-4262-9AE8-32EC025B4782|f81f2d6c-40cf-4b75-bda3-63d4ead1df88|" \
      "+X-QK-API-KEY=c26007f41f472932454ea80deabd612c"
    m=hashlib.md5()
    m.update(h.encode())
    return m.hexdigest().upper()
# headers1.setdefault("X-QK-SIGN",g)
url_login = "http://fp02.ops.gaoshou.me/s4/login.mobile"
url_dash = "http://fp01.ops.gaoshou.me/s4/dashboard"
url_creat= "http://fp01.ops.gaoshou.me/s5/create_user"
url_bind= "http://fp02.ops.gaoshou.me/s4/bindMobile"
url_bind_oc = "http://fp01.ops.gaoshou.me/a/5.0/bindMobile.occupied"
url5_detail = "http://fp01.ops.gaoshou.me/s4/users.accounts.getDetail"
url_task="http://fp01.ops.gaoshou.me/s4/lite.subtask.list"
url_task_newbie="http://fp01.ops.gaoshou.me/s4/subtask.list.newbie"
url_key_bind="http://fp04.ops.gaoshou.me/s5k/key.bind"
url_lite="http://fp04.ops.gaoshou.me/v4/tasks/lite"
url_lppa="http://fp04.ops.gaoshou.me/s5k/key.lppa"
url_bootstrp="http://fp01.ops.gaoshou.me/s5k/key.bootstrap"
url_claim="http://fp01.ops.gaoshou.me/s5/reward.coin.claim.today"

header12={'cookie': 'DIS4=09b7b75b7cdc4390a3640dac0abfd5f5'}
data11 = {'Accept': '*/*', 'Content-Type': 'applicatio3'
                                           'n/json;charset=utf-8',
          'cookie': 'DIS4=7fcf2a98b39c4e79907c5b35d880456e; Expires=Thu, 20-Feb-2020 03:16:51 GMT; Max-Age=31536000; Path=/'}
data = {"phone": "18711794029", "code": "4883"}

# s=requests.post(url_creat)
# print(s.headers)
h = {
    'cookie': 'DIS4=f97c6ec81c37429d81d24b826eb2dfd7;user_redirct_subtask_list=1'
}

h3 = {
    'cookie': 'DIS4=c289c376b3b14bf182116069bdee559d; Expires=Thu, 20-Feb-2020 07:05:38 GMT; Max-Age=31536000; Path=/, lu=51229754; Expires=Thu, 20-Feb-2020 07:05:38 GMT; Max-Age=31536000; Path=/, ln=1; Expires=Thu, 20-Feb-2020 07:05:38 GMT; Max-Age=31536000; Path=/'}
h2 = {'cookie': 'DIS4=b81a55bdd0cf4f008a4896eae39e57f0'}
h5={'cookie': 'DIS4=479ebf2457744c8897147039ca5fbce6; Expires=Thu, 20-Feb-2020 07:12:49 GMT; Max-Age=31536000; Path=/, DIS4=479ebf2457744c8897147039ca5fbce6; Expires=Thu, 20-Feb-2020 07:12:49 GMT; Max-Age=31536000; Path=/, lu=51229750; Expires=Thu, 20-Feb-2020 07:12:49 GMT; Max-Age=31536000; Path=/, mu=; Expires=Thu, 01-Jan-1970 00:00:00 GMT; Path=/, ln=1; Expires=Thu, 20-Feb-2020 07:12:49 GMT; Max-Age=31536000; Path=/'}
# h4=requests.post(url_bind,data=data,headers=h3)
# print(h4.json())
# from newRun import hand_cookie
# h1=requests.post(url_login,data=data)
# print(h1.headers["Set-Cookie"])
# print(h1.text)
# cookies=h1.cookies.get_dict()
# print(cookies)
# print(hand_cookie(cookies))
# s=requests.get(url_task,headers={})
# print(s.text)
# Hm_lpvt_484788504bd0bc163a54b110d0dc003c=1551263345; Hm_lvt_484788504bd0bc163a54b110d0dc003c=1551148020,1551160396,1551160457,1551263345; DIS4=2cb350cd68c946e38ef17462d4137d94; _umdata=G2BE4F5BD84715801F4E9A9EB04C1B64D728E2E; lite_token=f57de35df633269251a22d31b48c7c35; ln=1; lu=51229796; _uab_collina=155107910363212885338268; MCU=4bbd3cbcffa74572bbe2387a5e13fb7a; user_first_vist_rongyuka=1
from requests.cookies import RequestsCookieJar
cookie_jar=RequestsCookieJar()
cookie_jar.set("DIS4","DIS4=f62cf68677854828858610326acff69d")
# cookie_jar.set("user_first_vist_rongyuka","1")
# cookie_jar.set("Hm_lpvt_484788504bd0bc163a54b110d0dc003c","1551317706")
# cookie_jar.set("Hm_lvt_484788504bd0bc163a54b110d0dc003c","1551160396,1551160457,1551263345,1551317706")
# cookie_jar.set("_umdata","G2BE4F5BD84715801F4E9A9EB04C1B64D728E2E")
# cookie_jar.set("lite_token","f57de35df633269251a22d31b48c7c35")
# cookie_jar.set("_uab_collina","155107910363212885338268")
# cookie_jar.set("MCU","4bbd3cbcffa74572bbe2387a5e13fb7a")
# cookie_jar.set("user_first_vist_rongyuka","1")
# cookie_jar.set("ln","1")
# cookie_jar.set("lu","51229796")
# cookie_jar.set("DIS4","2cb350cd68c946e38ef17462d4137d94")
# s=requests.post(url_creat,cookies=cookie_jar)
# print(s.headers)
# print(s.cookies["DIS4"])
# print(s.text)
# r=requests.get(url_task,headers=headers)
# print(r.headers)
# print(r.headers["Set-Cookie"])
# print(r.cookies["user_first_vist_rongyuka"])
# print(r.text)
# a=requests.get("http://fp04.ops.gaoshou.me/s4/lite.subtask.list",headers={"cookie":"DIS4=2cb350cd68c946e38ef17462d4137d94"})
# print(a.text)
# b=requests.get(url_lite,headers=headers)
# print(b.text)

js={
    "bssid": "94:f6:65:17:77:3c",
    "carrier": "\\U4e2d\\U56fd\\U79fb\\U52a8",
    "device_id": 0,
    "is_jail_broken": 0,
    "local_ip": "172.16.1.83",
    "local_time": "1531384254.235346",
    "push": 1,
    "ssid": "QK1",
    "installed_apps": [
      {
        "bundle_id": "com.apple.Passbook",
        "bundle_version": "1.0",
        "dsid": 0,
        "item_id": 0,
        "purchase_date": "1487036321.00",
        "redownload": 0
      }
    ],
    "installed_apps_ios11": [
      {
        "bundle_id": "com.apple.Passbook",
        "bundle_version": "1.0",
        "dsid": 0,
        "item_id": 0,
        "purchase_date": "1487036321.00",
        "redownload": 0
      }
    ]
}
from common.crypto import Crypto
# crypto=Crypto()
# d=crypto.encrypt(js,10)
# print(d)
# a=requests.post(url_lppa,data=js,headers=headers)
# print(a.text)
# a=requests.get(url_key_bind,headers=headers1)
# print(a.headers)
# print(a.text)
#
# s=requests.get(url_dash, headers=headers1)
# print(s.text)
# b=requests.get(url_task,headers=headers)
# print(b.text)
# g=requests.get(url_bootstrp,headers=headers1)
# print(g.text)
# requests.post(url_creat)

# sign=make_sign_with_headers()
# print(sign)
# headers1.setdefault("X-QK-SIGN",sign)
# g=requests.get(url_bootstrp,headers=headers1)
# print(g.text)
# test_h={"cookie":"DIS4=7b5c030b6e68409f856c44b5a7c0b1cc"}
# t=requests.post(url_claim,headers=test_h)
# print(t.text)
# t=requests.get(url_dash,headers=headers)
# print(t.text)
# print(t.elapsed.total_seconds())
from requests import exceptions
# ggg={
#     "url":"/s5/reward.coin.claim.today",
#     "method":"post",
#     "params":"",
#     "headers":"",
# }
# print(ggg.get("a"))

a=r"E:\project\ApiTest\report\20190307接口自动化测试报告.xls"
import os
s,b=os.path.splitext(a)
print(b)