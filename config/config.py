# -*- coding: utf-8 -*-
'''
@File  : config.py.py
@Date  : 2019/1/15/015 17:28
'''
import os, platform

# 测试环境域名
# TESTDEV1 = "http://fp02.ops.gaoshou.me"
# TESTDEV2 = "http://fp02.ops.gaoshou.me"
# TESTDEV = "http://www.baidu.com"
TESTDEV0 = "http://fp02.ops.gaoshou.me"
TESTDEV1 = "http://fp01.ops.gaoshou.me"
TESTDEV2 = "http://fp02.ops.gaoshou.me"

# 用例字段名
CASENAME = ["caseId", "apiId", "caseDescribe", "apiHost", "apiParams", "apiHeaders", "method", "relatedApi",
            "relatedParams", "expect", "sqlStatement", "databaseExpect", "isExcute"]
if platform.system() == "Windows":
    # 用例存放路径
    CASEPATH = os.path.dirname(__file__).replace("common", "cases") + "\exmple.xlsx"
else:
    CASEPATH = os.path.dirname(__file__).replace("common", "cases") + "/case_user.xlsx"

TABLECASE = "testcase"
TABLERESULT = "testresult"
TABLEAPIINFO = "apiinfo"

CASEID = "caseId"
APIID = "apiId"
CASEDESCRIBE = "caseDescribe"
APIHOST = "apiHost"
PARMAS = "apiParams"
METHOD = "method"
APIHEADERS="apiHeaders"
HEADERS = "headers"
RELATEDAPI = "relatedApi"
RELEATEDPARAMS = "relatedParams"
FACT = "fact"
EXPECT = "expect"
SQLSTATEMENT = "sqlStatement"
DATABASERESUTL = "databaseResult"
DATABASEEXPECT = "databaseExpect"
ISPASS = "ispass"
TIME = "time"
FORMORT = "%Y/%m/%d %H:%M:%S"

PASS = "pass"
FAIL = "fail"
BLOCK = "block"
REASON = "reason"

# 邮件接受人邮箱
RECEIVERS = ["740207942@qq.com", "2395027402@qq.com","ning.tonggang@qianka.com"]

"""
cookie key
"""

"""
用户当前登录状态
    前端
        用来区分用户登录状态

    后端
        当用户登录时，自动设置cookie值 ln=1
        当用户登出时
            API接口401时，自动设置cookie值为空，并立即过期
            index.py时，自动设置cookie值为空，并立即过期
"""
COOKIE_LOGIN_STATUS = 'ln'
COOKIE_LOGIN_STATUS_VALUE_IS_LOGIN = '1'
COOKIE_LOGIN_STATUS_VALUE_IS_LOGOUT = ''

NEW_COOKIE_REFERER_KEY = 'qk_referer'  # 渠道 id（新的）
COOKIE_LAST_USER_ID = 'lu'  # 最近一次登录的 user id
COOKIE_MASTER_ID = 'mu'  # 师父 id
COOKIE_SHOUTU_RULE = 'rule'  # 收徒规则
COOKIE_SESSION_V4 = 'DIS4'  # 4.0 登录状态下的 session id
COOKIE_SESSION_V3 = 'DIS'  # 3.0 的 session id
COOKIE_SESSION_UNAUTHED = 'DIS4L'  # 未登录状态下的 session id, 4.0 的退出用户
COOKIE_WEBCLIP = 'webclip'  # 通过钱咖入口进入钱咖
COOKIE_DIABLO_REV = 'diabloRev'
COOKIE_TLS_STATUS = 'QK_TLS_STATUS'
# 是否安装过证书标志位, 这个 cookie 实际是种在 苹果的设置应用的 webview 中的
COOKIE_PROFILE_SERVICE_INSTALLED = 'profile_service_installed'
COOKIE_QK_GUID_APPSTORE = 'qk_guid_appstore'  # 首次安装 appstore 版钥匙的标记
# lite版token，用以绑定用户设备信息及lppa
COOKIE_LITE_TOKEN = 'lite_token'
NEW_JUTA_BILUID = 'juta_bilu_id'  # 聚塔必撸用户id（新的）
# 记录用户是否第一次打开荣誉咖跳转试玩任务列表页
COOKIE_USER_REDIRECT_LIST = 'user_redirct_subtask_list'
