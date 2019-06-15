# !/uer/bin/env python3
# coding=utf-8
import datetime
import logging
import os
import traceback
import inspect
import functools
import unittest

from base import HTMLTestReportCN
from base.send_email import smtp_email
from configElement import ConfYaml

logs_dir_name = 'logs'
__dir__ = os.path.dirname(os.path.abspath(__file__))

if logs_dir_name not in os.listdir(os.path.join(__dir__, '../')):
    os.mkdir(''.join((os.path.join(__dir__, '../'), logs_dir_name)))

_now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
_logs_dir_path = os.path.join(__dir__, ''.join(('../', logs_dir_name, '/')))
log_fp = ''.join((_logs_dir_path, _now, ".log"))

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=log_fp,
                    filemode='w')

_console = logging.StreamHandler()
_console.setLevel(logging.INFO)
_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
_console.setFormatter(_formatter)
LOGGER = logging.getLogger('czb test')
LOGGER.addHandler(_console)


def logged(func):
    """创建一个日志装饰器，它会记录所装饰函数的入参和
    """
    result = None

    @functools.wraps(func)
    def inner(*args, **kwargs):

        try:
            nonlocal result
            result = func(*args, **kwargs)
            LOGGER.info('模块:{}\n 调用函数 {} 传入参数: {},{}\n 返回结果: {}'
                        .format(inspect.getmodule(func), func.__name__,
                                args, kwargs, result))
            return result
        except Exception as Ex:
            LOGGER.error("{}方法入参:{},{}".format(func.__name__, args, kwargs))
            e = traceback.format_exc()
            LOGGER.error('Exception：{}'.format(e))
            raise Ex

    return inner


class TestRunner(object):
    def __init__(self, cases_fp, cases="./", title="CZB Test Report", description="Test case execution",
                 tester="system"):
        self.cases = cases
        self.title = title
        self.des = description
        self.tester = tester
        self.cases_fp = cases_fp

    def run(self):

        for filename in os.listdir(self.cases):
            if filename == "report":
                break
        else:
            os.mkdir(self.cases + '/report')

        now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        report = os.path.join(os.path.dirname(os.path.abspath(__file__)), now.join(("'../report/'", ".html")))
        with open(report, 'wb') as fp:
            tests = unittest.defaultTestLoader.discover(self.cases, pattern='test*.py', top_level_dir=None)
            runner = HTMLTestReportCN.HTMLTestRunner(stream=fp, title=self.title, description=self.des,
                                                     tester=self.tester)
            runner.run(tests)

        email_dict = ConfYaml('../__conf.yaml').read()['EMAIL']
        smtp_email(sender=email_dict['sender'], receivers=email_dict['receivers'], password=email_dict['password'],
                   smtp_server=email_dict['smtp_server'], port=email_dict['port'],
                   attachment=[self.cases_fp, report, log_fp])

    def debug(self):
        tests = unittest.defaultTestLoader.discover(self.cases, pattern='test*.py', top_level_dir=None)
        runner = unittest.TextTestRunner(verbosity=2)
        print("test start:")
        runner.run(tests)
        print("test end!!!")
