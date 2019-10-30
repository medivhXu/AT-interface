# !/uer/bin/env python3

import unittest
from parameterized import parameterized_class

from base.logger import LOGGER
from base.runner import TestRunner
from config_element import conf_load, cases_load
from base.request_func import request_func

from module import *
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

# ===============这里需要根据自己需要修改=============== #
# 单独加载用例文件

# file = '../3platformAPI.yaml'
# cases = conf_load(file).read()

# -------------------------------------------------- #
# 批量加载用例文件，可以按照规定顺序执行

cases = cases_load()
PHONE_WORD = 'phone'

# =================================================== #


@parameterized_class(cases)
class Test(unittest.TestCase, TestRunner):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_run(self):
        LOGGER.info('\n*************** No: {} ***************\n'.format(self.case_no))

        # 取前置条件所需的变量
        request_data = pretreatment(unit_test_subclass=self, TEMPORARY_VARIABLE=TEMPORARY_VARIABLE, PHONE_WORD=PHONE_WORD)

        LOGGER.info('\n*************全局变量：************\n{}\n*********************************'.format(TEMPORARY_VARIABLE))
        res = request_func(path=''.join((self.scheme, '://', self.host, self.path)), method=self.method,
                           request_data=request_data, headers=self.headers, verify=True)

        # 后置处理，取相关参数
        post_processing(unit_test_subclass=self, res=res, TEMPORARY_VARIABLE=TEMPORARY_VARIABLE)


if __name__ == '__main__':
    run = TestRunner('./', 'Medivh接口测试', '测试环境', 'Medivh')
    run.debug()
