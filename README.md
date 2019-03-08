# AT-interface
基于unittest框架，让工作更快捷方便

#### 安装说明：
* python3.5+ : http://www.python.org/
* requests : pip3 install requests

#### 栗子:
进入/case/test_start.py
```
# !/uer/bin/env python3
# coding=utf-8
import unittest
from base.test_runner import TestRunner
from base.request_func import RequestFunc
from parameterized import parameterized
from exception.myError import MyError
from base.collage_string import CollageStr


class SendMsg(unittest.TestCase, TestRunner):
    @classmethod
    def setUpClass(cls, ):
        super(SendMsg, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @parameterized.expand([('APP', 'services/v3/begin/sendMsg', 'post', {'phone': 13800138000},
                            {"code": 200, "message": "OK", "result": "null"}), ])   # 设置请求参数，与test_run方法参数名称对应
    @unittest.expectedFailure
    def test_run(self, platform, url, method, data, expected):
        md_data = CollageStr(data)
        sign_str = md_data.sign_str(platform=platform, device="android")
        req = RequestFunc(platform=platform, url=url)
        if method == 'post':
            req.post_func = sign_str
            res = req.post_func
            self.assertEqual(res.items(), expected, "不相等～")
        elif method == 'get':
            res = req.get_func = sign_str
            self.assertEqual(res.items(), expected, "不相等～")
        else:
            raise MyError("不支持该请求方法！")


if __name__ == '__main__':
    run = TestRunner('./', 'xxx接口测试', '测试环境：android', 'Medivh')
    run.debug()
```

配置完成后直接运行即可

未完，待续～
