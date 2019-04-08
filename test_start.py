# !/uer/bin/env python3
# coding=utf-8
import unittest
import requests
import json
import datetime
from parameterized import parameterized_class
from module.collage_string import CollageStr
from base.runner import TestRunner
from base.my_exception import *
from base.log import LOGGER
from analysis.comparison_results import differences
from module.get_variable import get_var, push_var
from module.get_msg_from_db import get_msg_from_db

# debug data
par = [{'case_no': 1, 'case_name': '短信', 'url': 'https://test-acs.czb365.com/services/v3/begin/sendMsg',
        'method': 'post', 'port': None, 'data': {'phone': '$phone'}, 'checkpoint': {'text': {'code': 200}}},
       {'case_no': 1, 'case_name': '登录', 'url': 'https://test-acs.czb365.com/services/v3/begin/loginAppV4',
        'method': 'post', 'port': None, 'data': {'phone': '%phone', 'code': '&get_msg_from_db(%phone)'},
        'checkpoint': {'text': {'code': 200, 'token': '$&token'}}}
       ]

"""
   $：表示从配置文件中取值
   %：代表从全局变量中取值
   &：表示运行系统方法
"""

TEMPORARY_VARIABLE = {}


# cases = LoadCase().get_all_data_set()


@parameterized_class(par)
class Test(unittest.TestCase, TestRunner):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_run(self):
        LOGGER.info('No: {} {}'.format(self.case_no, self.case_name))
        if self.method == 'get':
            # get方法还没调好
            data = CollageStr(self.data).sign_str(self.data['phone'])

            res = requests.get(self.url, data, verify=True)
            LOGGER.info('response: {}'.format(res.text))
            if res.status_code != requests.codes.ok:
                dict_res = json.dumps(res.text)
                if self.checkpoint:
                    for po in self.checkpoint.keys():
                        for var in self.checkpoint[po].keys():
                            if po == 'text':
                                differences(self.checkpoint[po][var], dict_res)
                else:
                    LOGGER.warning("[-]用例: {}, 请求地址: {}, 请求参数: {}, 响应body: {}"
                                   .format(self.case_no, self.url, res.status_code, res.text))
            else:
                LOGGER.info("[+]用例: {}, 请求地址: {}, 参数: {} , 响应: {}".format(self.case_no, self.url, self.data, res.text))
        elif self.method == 'post':
            # 取前置条件所需的变量
            for d in self.data:
                # 变量中有系统方法的
                if '&' in str(self.data[d]):
                    func_str = self.data[d].replace('&', '')
                    func = func_str.split('(')[0]
                    # 带参方法
                    if '%' in func_str:
                        var = func_str.split('%')[-1].replace(')', '')
                        value = TEMPORARY_VARIABLE[var]
                        result = eval(func)(value)
                        if result:
                            self.data[d] = result
                        else:
                            raise RuntimeException("{}({})方法运行时，未取到结果！".format(func, value))
                    if '$' in func_str:
                        var = func_str.split('$')[-1].replace(')', '')
                        value = get_var(var)
                        result = eval(func)(value)
                        if result:
                            self.data[d] = result
                        else:
                            raise RuntimeException("{}({})方法运行时，未取到结果！".format(func, value))

                if '%' in str(self.data[d]):
                    self.data[d] = TEMPORARY_VARIABLE[d]

                if '$' in str(self.data[d]):
                    k = self.data[d].split('$')[-1].replace(')', '')
                    result = get_var(k)
                    self.data[d] = result
                    TEMPORARY_VARIABLE[d] = result

            data = CollageStr(self.data).sign_str(self.data['phone'])
            LOGGER.info('\n*************************\n全局变量：{}\n*************************'.format(TEMPORARY_VARIABLE))

            LOGGER.info('***** request: {}'.format(self.data))
            start_time = datetime.datetime.now()
            res = requests.post(self.url, data, verify=True)
            end_time = datetime.datetime.now() - start_time
            LOGGER.info('***** response: {}, 响应时间: {} 秒!'.format(res.text, end_time))

            dict_res = json.loads(res.text)
            if res.status_code == requests.codes.ok:
                if self.checkpoint:
                    for po in self.checkpoint.keys():
                        for var in self.checkpoint[po].keys():
                            # 取后置参数所需变量
                            if '$&' in str(self.checkpoint[po][var]):
                                TEMPORARY_VARIABLE[var] = dict_res['result'][var]
                                push_var(var, self.data['phone'], dict_res['result'][var])
                                continue
                            if po == 'text':
                                self.assertIn(self.checkpoint[po][var], dict_res.values(), '预期不符～')
                            elif po == 'result':
                                self.assertIn(self.checkpoint[po][var], dict_res[po], '预期不符～')

                else:
                    LOGGER.warning("[-]用例: {}, 请求地址: {}, 请求参数: {}, 响应body: {}"
                                   .format(self.case_no, self.url, res.status_code, res.text))
            else:
                LOGGER.info("[+]用例: {}, 请求地址: {}, 参数: {} , 响应: {}".format(self.case_no, self.url, self.data, res.text))
        else:
            raise MethodException("方法错误，不支持{}方法!".format(self.method))


if __name__ == '__main__':
    run = TestRunner('./', 'xxx接口测试', '测试环境', 'Medivh')
    run.debug()
