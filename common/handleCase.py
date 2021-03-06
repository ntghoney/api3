# -*- coding: utf-8 -*-
'''
@File  : handleCase.py
@Date  : 2019/1/15/015 18:24
'''
from common.parseExc import *
from common.log import Log
from config.config import *
import logging
import re
import os,json
from common.utils import MyEncoder

log = logging.getLogger()


# 去掉换行符
def quchu_n(str):
    str = str.replace("\n", "")
    return str


def get_case_path():
    """
    用例路径，以case_开头的.xlsx文件
    :return:
    """
    path = os.path.dirname(__file__).replace("common", "cases")
    rep = re.compile(r"^case_")
    dir_name = os.listdir(path)
    case_path = []
    for file in dir_name:
        extension = os.path.splitext(file)[1]  # 文件拓展名
        file_name = os.path.splitext(file)[0]  # 文件名
        if extension == ".xlsx" and re.findall(rep, file_name):
            case_path.append(os.path.join(path, file))
        else:
            log.info("{}不符合规则".format(file))
    return case_path


class HandleCase(object):
    def __init__(self, case_path):
        # 实例parseExc对象
        self.log = Log().getLog()
        self.pe = PaserExc(case_path, 0)

    # 总用例数
    def get_totals(self):
        return self.pe.get_nrows() - 1

    # 处理检查点中数据
    def handle_checkPoint(self, item):
        checkPints = {}
        if "\n" in item:
            point = item.split("\n")
            for i in point:
                if "=" in i:
                    key, value = i.split("=", 1)
                    if ":" in value:
                        value = value.replace(":", "：")
                    checkPints[key] = value
        else:
            key, value = item.split("=")
            if "=" in item:
                key, value = item.split("=")
                if ":" in value:
                    value = value.replace(":", "：")
            checkPints[key] = value
        return checkPints

    def hande_sql(self, sql_point):
        print(sql_point)
        sql_points = {}
        points = self.handle_sql_point(sql_point)
        for key in points.keys():
            checks = self.handle_checkPoint(points[key])
            sql_points[key] = checks
        return sql_points

    def handle_sql_point(self, sqls):
        """
        处理用例sql语句和sql检查点格式
        :param sqls:
        :return:
        """
        sqlstate = dict()
        if "\n" in sqls:
            sqls = str(sqls).split("\n")
            for i in sqls:
                if ":" in i:
                    key, value = str(i).split(":")
                elif "：" in i:
                    key, value = str(i).split("：")
                else:
                    continue
                sqlstate[key] = value
        else:
            key = ""
            value = ""
            if ":" in sqls:
                key, value = str(sqls).split(":")
            if "：" in sqls:
                key, value = str(sqls).split("：")
            if key and value:
                sqlstate[key] = value
        return sqlstate

    # 处理关联参数
    def handle_related_params(self, params):
        related_params = []
        if "\n" in str(params):
            for i in str(params).split("\n"):
                if "$" in i:
                    related_params.append(i.replace("$", ""))
        else:
            if "$" in params:
                related_params.append(params.replace("$", ""))
        return related_params

    def handle_data(self, datas):
        """
        处理用例的数据格式
        """
        global cid, apiId, describe, host, expect, method, params, checkPints, relatedApi, relatedParams
        if isinstance(datas, dict):
            cid = int(datas[CASEID])
            apiId = int(datas[APIID])
            describe = str(quchu_n(datas[CASEDESCRIBE]))
            host = str(quchu_n(datas[APIHOST]))
            expect = str(datas[EXPECT])
            method = str(datas[METHOD])
            params = str(datas[PARMAS])
            headers = str(datas[APIHEADERS])
            relatedParams = str(datas[RELEATEDPARAMS])
            sqlStatement = str(datas[SQLSTATEMENT])
            databaseExpect = str(datas[DATABASEEXPECT])
            testData = str(datas[TESTDATA])
            if expect:
                datas[EXPECT] = self.handle_checkPoint(expect)
            if sqlStatement:
                datas[SQLSTATEMENT] = self.handle_sql_point(sqlStatement)
            if databaseExpect:
                datas[DATABASEEXPECT] = self.handle_sql_point(databaseExpect)
            if relatedParams:
                datas[RELEATEDPARAMS] = self.handle_related_params(relatedParams)
            if testData:
                datas[TESTDATA] = self.handle_sql_point(testData)
            return datas
        else:
            raise Exception("参数错误，所传参数datas必须是字典")

    # 获得所有测试用例
    def get_cases(self):
        values = []
        cases = []
        result = []
        rowValues = self.pe.get_row()[1:]
        for row in rowValues:
            values.append(dict(zip(CASENAME, row)))
        # 去掉不执行的用例
        for case in values:
            if case["isExcute"] == "y" or case["isExcute"] == "Y" or case["isExcute"] == "":
                cases.append(case)
            case.pop("isExcute")
        # 转换用例字段的数据格式
        for case in cases:
            case[CASEID] = int(case[CASEID])
            case[APIID] = int(case[APIID])
            case[APIHEADERS] = case[APIHEADERS]
            case[CASEDESCRIBE] = quchu_n(str(case[CASEDESCRIBE]))
            case[APIHOST] = quchu_n(str(case[APIHOST]))
            case[PARMAS] = quchu_n(case[PARMAS])
            case[METHOD] = quchu_n(case[METHOD])
            if not case[RELATEDAPI]:
                case[RELATEDAPI]=None
            if isinstance(case[RELATEDAPI], float):
                case[RELATEDAPI] = int(case[RELATEDAPI])
            if isinstance(case[RELATEDAPI],str):
                # case[RELATEDAPI]=json.dumps(case[RELATEDAPI],cls=MyEncoder,ensure_ascii=False)
                case[RELATEDAPI] = json.loads(case[RELATEDAPI],encoding="utf8")
            case[RELEATEDPARAMS] = case[RELEATEDPARAMS]
            case[RELEATEDPARAMS] = case[RELEATEDPARAMS]
            case[EXPECT] = case[EXPECT]
            self.handle_data(case)
            result.append(case)
        return result


if __name__ == '__main__':
    cases = []
    for i in get_case_path():
        hc = HandleCase(i)
        cases.extend(hc.get_cases())
    print(cases)
