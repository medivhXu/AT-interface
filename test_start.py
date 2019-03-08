# !/uer/bin/env python3
# coding=utf-8
import unittest
import requests
from parameterized import parameterized
from base.collage_string import CollageStr
from base.loadcase import LoadCase
from base.runner import TestRunner
from base.my_exception import *
from base.log import LOGGER


class SendMsg(unittest.TestCase, TestRunner):
    @classmethod
    def setUpClass(cls, ):
        super(SendMsg, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    cases = LoadCase().get_all_data_list()

    # debug data
    par = [(1, '短信', 'https://test-acs.czb365.com', 'post', None, '/services/v3/begin/sendMsg', {'text': {'code': 200}},
            {'text': {'code': 200}})]

    @parameterized.expand(cases)
    def test_run(self, case_no, case_name, url, method, port, data, checkpoint):
        sign_str = CollageStr(data).sign_str()
        full_data = data.updata({'sign': sign_str})
        if method == 'get':
            res = requests.get(url, full_data, verify=True)
            if res.status_code != requests.codes.ok:
                LOGGER.warning("[-]用例: {}, 请求地址: {}, 请求参数: {}, 响应body: {}"
                               .format(case_no, url, res.status_code, res.text))
            else:
                LOGGER.info("[+]用例: {}, 请求地址: {}, 参数: {} , 响应: {}".format(case_no, url, data, res.text))
        elif method == 'post':
            res = requests.post(url, full_data)
            if res.status_code != requests.codes.ok:
                LOGGER.warning("[-]用例: {}, 请求地址: {}, 请求参数: {}, 响应body: {}"
                               .format(case_no, url, res.status_code, res.text))
            else:
                LOGGER.info("[+]用例: {}, 请求地址: {}, 参数: {} , 响应: {}".format(case_no, url, data, res.text))
        else:
            raise MethodException("方法错误，不支持{}方法!".format(method))


if __name__ == '__main__':
    run = TestRunner('./', 'xxx接口测试', '测试环境', 'Medivh')
    run.debug()
