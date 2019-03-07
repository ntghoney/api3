# -*- coding: utf-8 -*-
'''
@File  : newRun.py
@Date  : 2019/1/25/025 15:40
'''
from common.conDatabase import ConMysql, get_base_info
from common.log import Log
from common.handleCase import HandleCase, get_case_path
from common.sendEmail import send_email_for_all
from common.parseConfig import ParseConfig
from common.report import get_now
import string
import datetime, time
from common.report import Report
import json
import re
from config.config import *
import random
import requests
import argparse
from common.utils import MyEncoder
from common.html_report import html_body
log = Log().getLog()
pc = ParseConfig()
pat = re.compile("DIS4=(.*?);")
report = Report()  # 测试报告实例


def init():
    """
    初始化环境和数据
    :return:
    """
    # 开始测试之前先清除数据库前一次测试储存的数据
    con.truncate_data(TABLECASE)
    con.truncate_data(TABLERESULT)
    con.truncate_data(TABLEAPIINFO)


def get_env():
    """
    执行参数判定当前测试执行环境
    0：真实环境
    1：fp01
    2:fp02
    3:fp03
    默认执行fp02
    :return: environment 测试环境域名，database_info测试环境数据库连接信息
    """
    parse = argparse.ArgumentParser(description="execution environment")
    parse.add_argument("-env", type=int, default=2)
    arg = parse.parse_args()
    env = arg.env
    if env == 0:
        environment = TESTDEV0
        database_info = get_base_info(
            pc.get_info("ServerDatabase0")
        )
    elif env == 1:
        environment = TESTDEV1
        database_info = get_base_info(
            pc.get_info("ServerDatabase1")
        )
    elif env == 2:
        environment = TESTDEV2
        database_info = get_base_info(
            pc.get_info("ServerDatabase2")
        )
    else:
        environment = TESTDEV2
        database_info = get_base_info(
            pc.get_info("ServerDatabase2")
        )
        log.error("参数错误，执行fp02环境")
    return environment, database_info


test_env, server_database = get_env()
print("当前执行环境-------{}，数据库地址-------{}"
      .format(test_env, server_database["host"]))
con_server = ConMysql(server_database)  # 服务器数据库链接
con = ConMysql()  # 本地数据库连接对象


def prepare_test_data(data):
    for key in data.keys():
        if key == "sql":
            try:
                con_server.execute_sql(data[key])
            except:
                log.error("sql语句出错：%s" % data[key])
        elif key == "sh":
            try:
                os.system(data[key])
            except:
                log.error("shell文件出错")
        else:
            pass


class Http(object):
    """
    请求封装，post,get
    """

    @classmethod
    def get(cls, path, params=None, headers=None):
        res = requests.get(test_env + path, params=params, headers=headers)
        return res

    @classmethod
    def post(cls, path, params=None, headers=None):
        res = requests.post(test_env + path, data=params, headers=headers)
        return res


def header_handle(header):
    """
    处理头部信息
    :param header:
    :return:
    """
    headers = {}
    header = params_replace(header)
    if "\n" in header:
        t = header.split("\n")
        for i in t:
            if ":" in i:
                key, value = i.split(":")
                headers[key] = value
            if "：" in i:
                key, value = i.split("：")
                headers[key] = value
    else:
        if ":" in header:
            key, value = header.split(":")
            headers[key] = value
    return headers


def params_replace(p):
    """
    参数化替代
    :param p:
    :return:
    """
    r1 = re.compile("\${.*?}")  # 参数化格式
    r2 = re.compile("\${(.*?)}")  # 参数名
    if re.findall(r1, p):
        for s in re.findall(r2, p):
            if pc.get_info(PARAMETERIZE) and s in pc.get_info(PARAMETERIZE).keys():
                a = pc.get_info(PARAMETERIZE)[s]
                p = p.replace("${%s}" % s, a)
                log.info("参数化成功%s" % p)
            else:
                log.error("参数化失败,没有%s这个参数" % s)
    return p


def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串
    :param randomlength: 指定长度，默认16
    :return:random_str str
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def get_headers():
    """
    :从配置文件中获得请求头信息
    :return:headers dict
    """
    m_headers = {}
    cookies = pc.get_info("headers")
    m_headers.update(cookies)
    return m_headers


def get_all_case():
    """
    获得所有测试用例集合
    :return:cases list
    """
    cases = []
    case_path = get_case_path()
    for path in case_path:
        hc = HandleCase(path)
        cases.extend(hc.get_cases())
    return cases


def hand_cookie(cookies):
    """
    处理cookie
    :param cookies: dict
    :return:
    """
    my_str = ""
    for key in cookies.keys():
        my_str += ("{}={};".format(key, cookies[key]))
    return my_str[:-1]


def update_message(number):
    """
    更新t_user_verify表信息
    :param number: 用户手机号，从apiParams中获取
    :return:
    """
    result = con_server.query_one(
        "select * from t_user_verify where number ={}"
            .format(number)
    )
    # 十分钟前的时间
    timedelta = datetime.datetime.now() - datetime.timedelta(minutes=10)
    if not result:
        con_server.insert_data("t_user_verify",
                               number=number,
                               call_sid=generate_random_str(32),
                               verify="4883",
                               date_created=get_now().strftime(FORMORT),
                               status=1)
        return
    if result["date_created"] < timedelta:
        sql = "update t_user_verify set date_created='{}'where number={}". \
            format(get_now().strftime(FORMORT), number)
        con_server.update_data(sql)
    if result["status"] == 0:
        con_server.update_data(
            "update t_user_verify set status=1 where number={}"
                .format(number)
        )


def get_all_related_apiinfo(case, relatedApi):
    """
    获得当前执行用例的api以及与该api相关的api信息集合
    获得的接口信息会反转，最后关联的接口在最前，用例执行的接口在最后
    :param case_api_id:当前执行用例时的apiId
    :param relatedApi:关联接口的apiId
    :return:关联接口信息 list
    """
    if relatedApi == "self":
        return relatedApi
    all_related_apiinfo = []
    # 将当前用例执行的接口保存到接口信息集合
    all_related_apiinfo.append(case)
    while True:
        if isinstance(relatedApi,dict):
            all_related_apiinfo.append(relatedApi)
            all_related_apiinfo.reverse()
            break
        if relatedApi is not None:
            relatedApiInfo = con.query_one(
                "select * from {} where apiId={}"
                    .format(TABLEAPIINFO, relatedApi)
            )
            if relatedApiInfo:
                relatedApi = relatedApiInfo[RELATEDAPI]
                all_related_apiinfo.append(relatedApiInfo)
                all_related_apiinfo.reverse()
            else:
                log.error(
                    "接口{}所关联的接口{}在用例中没有选择执行".format(case, relatedApi)
                )
                return "ERRRR:接口{}所关联的接口{}在用例中没有选择执行" \
                    .format(case, relatedApi)
        else:
            break
    return all_related_apiinfo


def request_api(host, my_params, my_headers, request_method):
    """
    接口请求
    """
    if request_method == "post":
        res = Http.post(host, params=my_params, headers=my_headers)
    elif request_method == "get":
        res = Http.get(host, params=my_params, headers=my_headers)
    else:
        log.error("ERRRR:暂不支持{}这种请求方式".format(method))
        return "ERRRR：暂不支持{}这种请求方式".format(method)
        # 如果调用创建用户或登录接口，将headers信息写入配置文件
    if "login.mobile" in host or "create_user" in host and res is not None:
        # 将cookie转换为字符串写入配置文件
        cookies = hand_cookie(res.cookies.get_dict())
        pc.wirte_info(HEADERS, "cookie", cookies)
        log.info("headers信息写入配置文件成功--->{}".format(cookies))
    return res


def new_excute_case(case):
    related_params = case[RELEATEDPARAMS]
    related_api = case[RELATEDAPI]
    case_id = case[CASEID]
    params = case[PARMAS]
    sqlexpect = case[DATABASEEXPECT]
    apiId = case[APIID]
    apiId = case[APIID]
    host = case[APIHOST]
    method = case[METHOD]
    testData = case[TESTDATA]
    headers = ""
    # 如果接口中有参数为phone，可能这个接口需要验证码，
    # 则调用updata_message初始化t_user_verify表
    if testData:
        prepare_test_data(testData)
    if params:
        params = params_replace(params)  # 参数化参数
        case[PARMAS] = params
        if "phone" in json.loads(params, encoding="utf8").keys():
            update_message(params["phone"])
    if not case:
        log.error("没有可执行的用例")
        return
    # 如果调用创建用户接口，不需要headers信息
    if case[APIHEADERS]:
        headers = header_handle(case[APIHEADERS])
    else:
        if "create_user" in host or "login.mobile" in host:
            headers = None
        else:
            headers = get_headers()
    log.info("此次接口请求的header信息为--->{}".format(headers))
    # 获得关联接口信息
    allRelatedApi = get_all_related_apiinfo(case, related_api)
    # 判断用例执行的接口所关联的接口是否执行
    if isinstance(allRelatedApi, str):
        return allRelatedApi
    for api in allRelatedApi:
        related_api_host = api[APIHOST]
        related_api_params = api[PARMAS]
        related_api_method = api[METHOD]
        related_api_relatedparams = api.get(RELEATEDPARAMS)
        if api[APIHEADERS]:
            related_api_headers = header_handle(api[APIHEADERS])
        else:
            if "create_user" in host or "login.mobile" in host:
                related_api_headers = None
            else:
                related_api_headers = get_headers()
        if isinstance(related_api_relatedparams, str):
            related_api_relatedparams = related_api_relatedparams.replace(" ", "").split(",")
        log.info("正在执行关联接口:{}".format(related_api_host))
        res = request_api(related_api_host,
                          related_api_params,
                          related_api_headers,
                          related_api_method
                          )
        if res.status_code == 405:
            return res

        if not isinstance(res, str):
            try:
                respJson = res.json()
            except:
                log.error("接口调用出错{}".format(res))
                respJson = {}
            if related_api_relatedparams and respJson:
                for i in related_api_relatedparams:
                    if i == HEADERS:
                        pc.wirte_info(PARAMETERIZE, HEADERS,
                                      {"cookie": hand_cookie(res.cookies)})
                    if "." in i:
                        temp_resp = respJson
                        for j in i.split("."):
                            if j in temp_resp.keys():
                                temp_resp = temp_resp[j]
                        pc.wirte_info(PARAMETERIZE, i, str(temp_resp))
                    if i in respJson.keys():
                        pc.wirte_info(PARAMETERIZE, i, str(respJson[i]))
        if api.get(APIID) == case[APIID]:
            # 单条用例执行完毕后，清空params
            # pc.remote_section(PARAMETERIZE)
            return res


def excute_case(case):
    """
    执行用例的方法
    :param case: 单条用例
    :return: 接口执行结果，Response
    """
    global caseId, apiId, apiHost, params, method, headers, relatedApi, relatedParams
    allRelatedApi = []  # 所有关联api的信息
    res = {}
    relatedApi = case[RELATEDAPI]
    if not case:
        log.error("没有可执行的用例")
        return
    if CASEID in case.keys():
        caseId = case[CASEID]
    if APIID in case.keys():
        apiId = case[APIID]
    host = case[APIHOST]

    # 判断接口参数是否有参数化
    if "$" in case[PARMAS]:
        params = case[PARMAS]
    else:
        if PARMAS in case.keys() and case[PARMAS]:
            params = json.loads(case[PARMAS], encoding="utf8")
            # 如果接口中有参数为phone，可能这个接口需要验证码，
            # 则调用updata_message初始化t_user_verify表
            if "phone" in params.keys():
                update_message(params["phone"])
        else:
            params = ""
    if METHOD in case.keys():
        method = case[METHOD]
    # 如果调用创建用户接口，不需要headers信息
    if case[APIHEADERS]:
        headers = header_handle(case[APIHEADERS])
    else:
        if "create_user" in host or "login.mobile" in host:
            headers = None
        else:
            headers = get_headers()

    log.info("此次接口请求的header信息为--->{}".format(headers))
    # 获得关联接口信息
    allRelatedApi = get_all_related_apiinfo(caseId, relatedApi)
    # 判断用例执行的接口所关联的接口是否执行
    if isinstance(allRelatedApi, str):
        return allRelatedApi
    # 如果len(allRelatedApi)>1,说明该接口没有关联接口
    if len(allRelatedApi) > 1:

        for i in range(len(allRelatedApi)):
            if i < len(allRelatedApi) - 1:
                a = allRelatedApi[i]  # 当前执行接口
                b = allRelatedApi[i + 1]  # 下一个接口
            else:
                a = allRelatedApi[i]
                b = allRelatedApi[i]
                # 如果调用创建用户接口，不需要headers信息
            if case[APIHEADERS]:
                headers = header_handle(a[APIHEADERS])
            else:
                if "create_user" in host or "login.mobile" in host:
                    headers = None
                else:
                    headers = get_headers()

            apiHeaders = headers
            apiHost = a[APIHOST]
            apiParams = a[PARMAS]
            apiMethod = a[METHOD]
            relatedApiId = a[RELATEDAPI]
            # 当前接口执行结果其实是为了下一个接口的关联参数
            relatedParams = b[RELEATEDPARAMS]
            # 判断是否有多个关联参数，如果有，返回参数集合
            if relatedParams and ";" in relatedParams:
                relatedParams = relatedParams.split(";")
            if 0 != i and apiParams:
                apiParams = string.Template(apiParams)
                apiParams = apiParams.substitute(vars())
                apiParams = json.loads(apiParams, encoding="utf8")
            log.info("正在执行关联接口:{}".format(apiHost))
            res = request_api(apiHost, apiParams, apiHeaders, apiMethod)
            if not isinstance(res, str):
                try:
                    respJson = res.json()
                except:
                    log.error("接口调用出错{}".format(res))
                    respJson = {}
                # 判断relatedParams的数据类型，可能为list和str
                if relatedParams is not None and respJson:
                    if isinstance(relatedParams, str):
                        if relatedParams == HEADERS:
                            apiHeaders = {"cookie": hand_cookie(res.cookies)}
                        else:
                            var = locals()
                            var[relatedParams] = respJson[relatedParams]
                    elif isinstance(relatedParams, list):
                        for j in relatedParams:
                            if isinstance(j, str):
                                var = locals()
                                var[j] = respJson[j]
                            elif isinstance(j, list):
                                var = locals()
                                var[j[1]] = respJson[j[0]][j[1]]
                            else:
                                log.error("参数错误")
                if apiHost == host:
                    return res, apiParams
    else:
        res = request_api(host, params, headers, method)
    return res


# 测试报告模板

def get_report_data(caseID, caseDesciribe, apiHost,method,
                    apiParams, expect, fact, time="",
                    isPass=PASS, reason="",
                    databaseResult="", databaseExpect=""):
    result = {}
    result[METHOD]=method
    result[CASEID] = caseID
    # result[APIID] = apiId
    result[CASEDESCRIBE] = caseDesciribe
    result[APIHOST] = apiHost
    result[PARMAS] = apiParams
    result[EXPECT] = expect
    result[FACT] = fact
    result[DATABASERESUTL] = databaseResult
    result[DATABASEEXPECT] = databaseExpect
    result[ISPASS] = isPass
    result[TIME] = time
    result[REASON] = reason
    return result


def test(exp, fact, result):
    r = re.compile(r"\[(.*?)]")
    if "ERRRR" in fact:
        result[ISPASS] = FAIL
        result[REASON] = fact
        result[TIME] = get_now().strftime(FORMORT)
        return
    if isinstance(fact, tuple):
        result[PARMAS] = json.dumps(fact[-1], ensure_ascii=False)
        fact = fact[0]
    else:
        try:
            res = fact.json()
        except:
            if "err_code" in exp.keys():
                if str(exp["err_code"]) != str(fact.status_code):
                    result[FACT] = fact.text
                    result[ISPASS] = FAIL
                    result[TIME] = get_now().strftime(FORMORT)
                    reason = "{}的值预期为：{}，实际为：{}" \
                        .format("err_code", exp["err_code"], fact.status_code)
                    result[REASON] = reason
                else:
                    # 判断是否有检查点判断失败，如果有，ispass值仍然为fail
                    if result[ISPASS].__eq__(FAIL):
                        result[ISPASS] = FAIL
                    else:
                        result[FACT] = fact.text
                        result[ISPASS] = PASS
                    result[TIME] = get_now().strftime(FORMORT)
            return
        if not exp:
            result[ISPASS] = BLOCK
            result[FACT] = fact.text
            result[EXPECT] = " "
            result[TIME] = get_now().strftime(FORMORT)
            result[REASON] = "检查点未设置或用例检查点格式错误"
            return
        keys = exp.keys()
        for key in keys:
            values = exp[key].split(",")
            items = key.split(".")
            temp_res = res
            for item in items:
                if item not in temp_res.keys():
                    result[FACT] = fact.text
                    result[ISPASS] = FAIL
                    result[TIME] = get_now().strftime(FORMORT)
                    result[REASON] = "实际结果中没有{}这个字段," \
                                     "检查用例是否错误或接口返回结果错误".format(item)
                    return
                temp_res = temp_res[item]
            for value in values:
                t = []
                if re.findall(r, value):
                    value = re.findall(r, value)
                    for i in value:
                        k, v = i.split("=")
                        for j in temp_res:
                            if k not in j.keys():
                                result[FACT] = fact.text
                                result[ISPASS] = FAIL
                                result[TIME] = get_now().strftime(FORMORT)
                                result[REASON] = "实际结果中没有{}这个字段," \
                                                 "检查用例是否错误或接口返回结果错误".format(k)
                                return
                            t.append(j[k])
                        try:
                            v = int(v)
                        except:
                            v = v
                        if v not in t:
                            result[FACT] = fact.text
                            result[ISPASS] = FAIL
                            result[TIME] = get_now().strftime(FORMORT)
                            reason = "{}字段预期的值不在返回结果集中，预期{}={}，实际{}=[{}]" \
                                .format(k, k, v, k, t)
                            result[REASON] = reason
                else:
                    if str(temp_res) != str(value):
                        result[FACT] = fact.text
                        result[ISPASS] = FAIL
                        result[TIME] = get_now().strftime(FORMORT)
                        reason = "{}字段预期为{}，实际为{}]".format(key, temp_res, value)
                        result[REASON] = reason
                    else:
                        # 判断是否有检查点判断失败，如果有，ispass值仍然为fail
                        if result[ISPASS].__eq__(FAIL):
                            result[ISPASS] = FAIL
                        else:
                            result[FACT] = fact.text
                            result[ISPASS] = PASS
                        result[TIME] = get_now().strftime(FORMORT)


def checkDatabase(databaseExpect, databaseResult, result, fact):
    """
    数据库验证
    :param databaseExpect: 数据库期望
    :param databaseResult: sql执行结果
    :param result: 报告模板
    :param fact: 接口返回实际结果
    :return:
    """
    if databaseExpect:
        result[DATABASEEXPECT] = json.dumps(databaseExpect, ensure_ascii=False)
    else:
        result[DATABASEEXPECT] = " "
    if not databaseResult:
        result[DATABASERESUTL] = " "
    if databaseExpect and databaseResult:
        for key, values in databaseExpect.items():
            value = values.split(",") or values.split("，")
            for i in value:
                k, v = i.split("=")
                if k is None or v is None:
                    result[FACT] = fact.text
                    result[ISPASS] = BLOCK
                    result[TIME] = get_now().strftime(FORMORT)
                    result[REASON] = "用例sql语句书写错误"
                    return
                if k == "len":
                    if str(len(databaseResult[key])) != v:
                        result[FACT] = fact.text
                        result[ISPASS] = FAIL
                        result[TIME] = get_now().strftime(FORMORT)
                        result[REASON] = "数据库{}检查点检查失败，预期返回{}条数据，实际返回{}条数据" \
                            .format(k, v, len(databaseResult[key]))
                    continue
                if k not in databaseResult[key][0].keys():
                    result[FACT] = fact.text
                    result[ISPASS] = BLOCK
                    result[TIME] = get_now().strftime(FORMORT)
                    result[REASON] = "用例sql语句书写错误或数据库返回错误，{}不在数据库返回字段中" \
                        .format(k)
                    return
                if str(databaseResult[key][0][k]) != v:
                    result[FACT] = fact.text
                    result[ISPASS] = FAIL
                    result[TIME] = get_now().strftime(FORMORT)
                    result[REASON] = "数据库{}.{}检查点检查失败，预期为:{}，实际为:{}" \
                        .format(key, k, v, databaseResult[key][0][k])
                    return

    # if databaseExpect and databaseResult:
    #     for key in databaseResult.keys():
    #         if result[ISPASS] == "pass":
    #             if key not in databaseExpect.keys():
    #                 result[ISPASS] = BLOCK
    #                 result[FACT] = fact.text
    #                 result[TIME] = get_now().strftime(FORMORT)
    #                 result[REASON] = "数据库{}检查点未设置".format(key)
    #                 return
    #             if databaseResult[key] is None:
    #                 result[FACT] = fact.text
    #                 result[ISPASS] = BLOCK
    #                 result[TIME] = get_now().strftime(FORMORT)
    #                 result[REASON] = "用例sql语句书写错误"
    #                 return
    #             if int(databaseExpect[key]) == databaseResult[key]:
    #                 result[FACT] = fact.text
    #                 result[ISPASS] = PASS
    #                 result[TIME] = get_now().strftime(FORMORT)
    #             else:
    #                 result[FACT] = fact.text
    #                 result[ISPASS] = FAIL
    #                 result[TIME] = get_now().strftime(FORMORT)
    #                 result[REASON] = "数据库{}检查点检查失败，预期返回{}条数据，实际返回{}条数据" \
    #                     .format(key, databaseExpect[key], databaseResult[key])


def runAll():
    """
    运行所有用例
    :return:
    """
    init()  # 初始化
    resultSet = []  # 执行结果集
    cases = get_all_case()  # 测试用例集
    start_time = time.time()
    if not cases:
        log.error("用例为空，无匹配格式的.xlsx文件或文件中暂无用例数据")
        return
    log.info("共获取{}条用例".format(len(cases)))
    for case in cases:
        # 将用例存入数据库临时保存,testData不入库保存
        con.insert_data(TABLECASE, **case)
        # 将接口数据插入数据库apiInfo表中暂时保存
        apiInfo = {
            APIID: int(case[APIID]),
            APIHOST: case[APIHOST],
            PARMAS: case[PARMAS],
            METHOD: case[METHOD],
            APIHEADERS: case[APIHEADERS],
            RELATEDAPI: case[RELATEDAPI],
            RELEATEDPARAMS: case[RELEATEDPARAMS]
        }
        # 如果数据库中不存在apiId的接口，则插入
        if not con.query_all(
                "select * from {}  where apiId={}"
                        .format(TABLEAPIINFO, apiInfo[APIID])):
            con.insert_data(TABLEAPIINFO, **apiInfo)

    for case in cases:
        log.info("正在执行caseId={}的用例".format(case[CASEID]))
        databaseExpect = case[DATABASEEXPECT]
        sqlStatement = case[SQLSTATEMENT]
        sqlResult = {}
        # 执行用例
        res = new_excute_case(case)
        # sql语句参数化
        if sqlStatement:
            for key in sqlStatement.keys():
                result = con_server.query_all(
                    params_replace(sqlStatement[key])
                )
                if result is not None:
                    sqlResult[key] = result
                else:
                    sqlResult[key] = None
        else:
            sqlResult = {}
        # 报告模板
        result = get_report_data(
            caseID=case[CASEID],
            caseDesciribe=case[CASEDESCRIBE],
            apiHost=case[APIHOST],
            method=case[METHOD],
            apiParams=case[PARMAS],
            expect=json.dumps(case[EXPECT], ensure_ascii=False),
            fact=res,
            databaseExpect=json.dumps(databaseExpect, ensure_ascii=False, cls=MyEncoder),
            databaseResult=json.dumps(sqlResult, ensure_ascii=False, cls=MyEncoder)
        )
        # 检查点验证
        test(fact=res, exp=case[EXPECT], result=result)
        # 数据库验证
        checkDatabase(databaseExpect=databaseExpect,
                      databaseResult=sqlResult,
                      result=result,
                      fact=res)

        # 将执行结果写入数据库临时保存
        con.insert_data(TABLERESULT, **result)
        resultSet.append(result)
    end_time = time.time()
    time_consum = end_time - start_time  # 测试耗时
    case_count = con.query_all(
        "SELECT caseId FROM {}".format(TABLERESULT)
    )  # 执行用例
    fail_case = con.query_all(
        "SELECT caseId "
        "FROM {} WHERE ispass='{}'".format(TABLERESULT, FAIL)
    )  # 执行失败的用例
    block_case = con.query_all(
        "SELECT caseId FROM {} WHERE ispass='{}'".format(TABLERESULT, BLOCK)
    )  # 执行阻塞的用例
    success_case = con.query_all(
        "SELECT caseId FROM {} WHERE ispass='{}'".format(TABLERESULT, PASS)
    )  # 执行成功的用例
    if case_count is None:
        case_count = 0
    else:
        case_count = len(case_count)
    if fail_case is None:
        fail_case = 0
    else:
        fail_case = len(fail_case)
    if block_case is None:
        block_case = 0
    else:
        block_case = len(block_case)
    if success_case is None:
        success_case = 0
    else:
        success_case = len(success_case)
    result_info = "本次测试执行完毕，本次测试环境为：{}，" \
                  "共耗时{}秒，共执行用例：{}条，" \
                  "成功：{}条，失败：{}条，阻塞：{}条" \
        .format(test_env[7:11], float("%.2f" % time_consum),
                case_count, success_case,
                fail_case, block_case)
    log.info(result_info)
    # 将测试结果写入测试报告
    report.set_result_info(result_info)
    print(resultSet)
    exc_path, part_name = report.get_report(resultSet)

    #生成html报告
    html_title="%s接口自动化测试报告"%(get_now().strftime("%Y/%m/%d"))
    html_path=html_body(
        total=case_count,
        starttime=time.strftime(FORMORT,time.localtime(start_time)),
        endtime=time.strftime(FORMORT,time.localtime(end_time)),
        during=time_consum,
        passd=success_case,
        fail=fail_case,
        block=block_case,
        titles=html_title,
        details=resultSet
    )
    con.close()
    con_server.close()
    # 测试完成发送邮件
    send_email_for_all(
        msg=result_info,
        part_path=[exc_path,html_path])


if __name__ == '__main__':
    log.debug("******************************************START******************************************")
    runAll()
    log.debug("******************************************END******************************************")
