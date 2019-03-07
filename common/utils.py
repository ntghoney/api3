# -*- coding: utf-8 -*-
'''
@File  : utils.py
@Date  : 2019/3/6/006 14:27
'''
import json
import decimal


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(MyEncoder, self).default(o)
