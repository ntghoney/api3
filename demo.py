# -*- coding: utf-8 -*-
'''
@File  : demo.py
@Date  : 2019/1/15/015 16:18
'''
from configparser import ConfigParser
import os
import json
import pytest_html

import requests

headers = {
    "cookie": 'DIS4=f3002ea4638a4b8b902b4da0a9c882b8; Expires=Wed, 22-Jan-2020 03:11:05 GMT; Max-Age=31536000; Path=/, lu=26; Expires=Wed, 22-Jan-2020 03:11:05 GMT; Max-Age=31536000; Path=/, ln=1; Expires=Wed, 22-Jan-2020 03:11:05 GMT; Max-Age=31536000; Path=/',
    # "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16B92 version=2.0.2018101201 bid=com.he.ar",
    # "Accept":"application/json"
    }
url_login = "http://fp02.ops.gaoshou.me/s4/login.mobile"
url_dash = "http://fp02.ops.gaoshou.me/s4/dashboard"
url_creat= "http://fp01.ops.gaoshou.me/s5/create_user"
url_bind= "http://fp02.ops.gaoshou.me/s4/bindMobile"
url_bind_oc = "http://fp01.ops.gaoshou.me/a/5.0/bindMobile.occupied"
url5_detail = "http://fp01.ops.gaoshou.me/s4/users.accounts.getDetail"
header12={'cookie': 'DIS4=09b7b75b7cdc4390a3640dac0abfd5f5'}
data11 = {'Accept': '*/*', 'Content-Type': 'applicatio3'
                                           'n/json;charset=utf-8',
          'cookie': 'DIS4=7fcf2a98b39c4e79907c5b35d880456e; Expires=Thu, 20-Feb-2020 03:16:51 GMT; Max-Age=31536000; Path=/'}
data = {"phone": "18711794029", "code": "4883"}

# s=requests.post(url_creat)
# print(s.headers)
h = {
    'cookie': 'DIS4=5600488029db45ed87c46bbb870c7f93'
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
w={'payload': {'level_info': {'next_level_more_coin': {'a': {'b': {'c': {'d': {'e': '0'}}}}}}}}
s={"a":1}
print(s.keys())




