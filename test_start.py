# !/uer/bin/env python3

import unittest
import requests
import json
from parameterized import parameterized_class

from base.runner import TestRunner, LOGGER
from base.my_exception import *
from configElement import conf_load
# from analysis.comparison_results import differences
from module.get_variable import get_var, push_var
from module.get_msg_from_db import get_msg_from_db
from module.collage_string import CollageStr

"""
             ┏┓   ┏┓
            ┏┛┻━━━┛┻┓
            ┃   ☃   ┃
            ┃ ┳┛ ┗┳ ┃
            ┃   ┻   ┃
            ┗━┓   ┏━┛
              ┃      ┗━━━┓
              ┃  神兽保佑 ┣┓
              ┃　永无BUG！┏┛
              ┗┓┓┏━┳┓ ┏┛
               ┃┫┫  ┃┫┫
               ┗┻┛  ┗┻┛
"""

"""
   $：表示从配置文件中取值
   %：代表从全局变量中取值
   &：表示运行系统方法
   $&：表示从上一个接口中取数据
"""

TEMPORARY_VARIABLE = {}

cases_fp = '../3platformAPI.yaml'
cases = conf_load(cases_fp).read()

PHONE_WORD = 'platformCode'  # phone


@parameterized_class(cases)
class Test(unittest.TestCase, TestRunner):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_run(self):
        LOGGER.info('*************** No: {} {}'.format(self.case_no, self.case_name))
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
                    value = get_var(var, TEMPORARY_VARIABLE.get(PHONE_WORD))
                    result = eval(func)(value)
                    if result:
                        self.data[d] = result
                    else:
                        raise RuntimeException("{}({})方法运行时，未取到结果！".format(func, value))

            # 从全局变量中取值
            if '%' in str(self.data[d]):
                try:
                    self.data[d] = TEMPORARY_VARIABLE[d]
                except KeyError:
                    raise KeyError("全局变量中没有该字段，可能上次请求中没取出来该值！")

            # 从配置文件中取值
            if '$' in str(self.data[d]):
                k = self.data[d].split('$')[-1].replace(')', '')

                # get('phone') 需要改
                result = get_var(k, TEMPORARY_VARIABLE.get(PHONE_WORD))
                self.data[d] = result
                TEMPORARY_VARIABLE[d] = result

            # 如果请求参数中包含token字段，把它置成空字符串
            if d == 'token':
                if not self.data[d]:
                    self.data[d] = ''

            global request_data
            # 如果request data里面写死手机号，这里捕获后，直接传给参数排序
            if PHONE_WORD in TEMPORARY_VARIABLE.keys():
                phone = TEMPORARY_VARIABLE[PHONE_WORD]
                request_data = CollageStr(self.data).order_str(phone)
            else:
                if hasattr(self, 'limit'):
                    request_data = CollageStr(self.data).order_str(phone=self.data.get(PHONE_WORD),
                                                                   os=self.limit.get('os'))
                else:
                    request_data = CollageStr(self.data).order_str(phone=self.data.get(PHONE_WORD))

        LOGGER.info('\n*************************\n全局变量：{}\n*************************'.format(TEMPORARY_VARIABLE))
        LOGGER.info('$$$$$ path: {}'.format(self.path))
        LOGGER.info('***** request: \n{}\n *****'.format(request_data))
        if self.method == 'post':
            if hasattr(self, 'headers'):
                res = requests.post(self.path, request_data, headers=self.headers, verify=True)
                t = res.elapsed.total_seconds() * 1000
                LOGGER.info('***** response: \n{}\n *****, 响应时间: {:.2f} ms!'.format(res.text, t))
            else:
                res = requests.post(self.path, request_data, verify=True)
                t = res.elapsed.total_seconds() * 1000
                LOGGER.info('***** response: \n{}\n *****, 响应时间: {:.2f} ms!'.format(res.text, t))
        elif self.method == 'get':
            res = requests.get(self.path, request_data, headers=self.headers, verify=True)
            t = res.elapsed.total_seconds() * 1000
            LOGGER.info('***** response: {}, 响应时间: {:.2f} ms!'.format(res.text, t))
        else:
            raise NotImplementedError("还没实现！")

        dict_res = json.loads(res.text)
        if res.status_code == requests.codes.ok:
            if self.check_point:
                for po in self.check_point.keys():
                    for var in self.check_point[po].keys():
                        # 取后置参数所需变量, 这里可以扩展一个正则表达式提取器
                        if isinstance(dict_res, int):
                            self.assertEqual(self.check_point[po][var], dict_res, '预期不符～')
                            continue
                        if isinstance(dict_res['result'], list):
                            TEMPORARY_VARIABLE[var] = [po_word for po_word in dict_res['result'] if
                                                       '$&' in self.check_point[po][var]]
                            continue
                        if '$&' in str(self.check_point[po][var]):
                            # 这有个问题，如果conf.yaml中json层级发生变化，代码会报错
                            TEMPORARY_VARIABLE[var] = dict_res['result'][var]
                            # push_var(var, self.data[PHONE_WORD], dict_res['result'][var])
                            continue
                        if po == 'text':
                            if not isinstance(dict_res, dict):
                                self.assertEqual(self.check_point[po][var], dict_res, '预期不符～')
                            else:
                                self.assertIn(self.check_point[po][var], dict_res.values(), '预期不符～')
                        elif po == 'result':
                            self.assertIn(self.check_point[po][var], dict_res[po], '预期不符～')

            else:
                LOGGER.warning("[-]用例: {}, 请求地址: {}, 请求参数: {}, 响应body: {}"
                               .format(self.case_no, self.path, res.status_code, res.text))
        else:
            LOGGER.info("[+]用例: {}, 请求地址: {}, 参数: {} , 响应: {}".format(self.case_no, self.path, self.data, res.text))


if __name__ == '__main__':
    run = TestRunner(cases_fp, './', 'xxx接口测试', '测试环境', 'Medivh')
    run.debug()
