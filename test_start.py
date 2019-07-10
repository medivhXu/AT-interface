# !/uer/bin/env python3

import unittest
from parameterized import parameterized_class

from base.loger import LOGGER
from base.runner import TestRunner
from config_element import conf_load, cases_load
from base.request_func import request_func
from module.pretreatment import pretreatment
from module.post_processing import post_processing

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


TEMPORARY_VARIABLE = {}

cases = cases_load()
PHONE_WORD = 'phone'


@parameterized_class(cases)
class Test(unittest.TestCase, TestRunner):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_run(self):
        LOGGER.info('*************** No: {} {}'.format(self.case_no, self.case_name))
        # 取前置条件所需的变量

        request_data = pretreatment(unit_test_subclass=self, TEMPORARY_VARIABLE=TEMPORARY_VARIABLE, PHONE_WORD=PHONE_WORD)

        LOGGER.info('\n*************************\n全局变量：{}\n*************************'.format(TEMPORARY_VARIABLE))
        res = request_func(path=self.path, method=self.method, request_data=request_data, headers=self.headers,
                           verify=True)

        post_processing(unit_test_subclass=self, dict_res=res, TEMPORARY_VARIABLE=TEMPORARY_VARIABLE)


if __name__ == '__main__':
    run = TestRunner('./', 'xxx接口测试', '测试环境', 'Medivh')
    run.debug()
