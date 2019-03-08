# !/uer/bin/env python3
# coding=utf-8
import unittest
import requests
from parameterized import parameterized
from base.collage_string import CollageStr
from base.comparison_results import diff_str
from base.conf_manager import ConfYaml
from base.runner import TestRunner
from base.my_exception import *
from base.log import LOGGER, logged


class SendMsg(unittest.TestCase, TestRunner):
    @classmethod
    def setUpClass(cls, ):
        super(SendMsg, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    cases = ConfYaml('interface.yaml').read()

    # debug data
    par = [(1, 'https://test-acs.czb365.com', 'post', None, '/services/v3/begin/sendMsg', {'text': {'code': 200}},
            {'text': {'code': 200}})]

    tes = {{1: {'request': {'https://test-acs.czb365.com', 'post', None, '/services/v3/begin/sendMsg', {'text': {'code': 200}},
            {'text': {'code': 200}}}}}}

    @parameterized.expand(par)
    def test_run(self, case_no, url, method, header, path, data, expected, result):
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

        self.assertEqual(res.items(), expected, "不相等～")


if __name__ == '__main__':
    run = TestRunner('./', 'xxx接口测试', '测试环境', 'Medivh')
    run.debug()
