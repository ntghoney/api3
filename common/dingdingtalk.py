# -*- coding: utf-8 -*-
'''
@File  : dingdingtalk.py
@Date  : 2019/3/6/006 17:15
'''
import requests, json


def send_ding(content: str, Dingtalk_access_token: str):
    """
    钉钉群发信息
    :param content:信息
    :param Dingtalk_access_token:钉钉机器人token
    :return: True 成功，False 失败
    """
    try:
        url = Dingtalk_access_token
        pagrem = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "isAtAll": True
        }
        headers = {
            'Content-Type': 'application/json'
        }
        f = requests.post(url, data=json.dumps(pagrem), headers=headers)
        if f.status_code == 200:
            return True
        else:
            return False
    except:
        return False