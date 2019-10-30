# !/uer/bin/env python3
# coding=utf-8
import datetime
import os
import unittest

from base import HTMLTestReportCN
from base.send_email import smtp_email
from config_element import conf_load
from base.logger import log_fp


class TestRunner(object):
    def __init__(self, cases="./", title="CZB Test Report", description="Test case execution",
                 tester="system"):
        self.cases = cases
        self.title = title
        self.des = description
        self.tester = tester

    def run(self):

        for filename in os.listdir(self.cases):
            if filename == "report":
                break
        else:
            os.mkdir(self.cases + '/report')

        now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
        report = os.path.join(os.path.dirname(os.path.abspath(__file__)), now.join(("../report/", ".html")))
        with open(report, 'wb') as fp:
            tests = unittest.defaultTestLoader.discover(self.cases, pattern='test*.py', top_level_dir=None)
            runner = HTMLTestReportCN.HTMLTestRunner(stream=fp, title=self.title, description=self.des,
                                                     tester=self.tester)
            runner.run(tests)

        email_dict = conf_load('../__conf.yaml').read()['EMAIL']
        smtp_email(sender=email_dict['sender'], receivers=email_dict['receivers'], password=email_dict['password'],
                   smtp_server=email_dict['smtp_server'], port=email_dict['port'],
                   attachment=[report, log_fp])

    def debug(self):
        tests = unittest.defaultTestLoader.discover(self.cases, pattern='test*.py', top_level_dir=None)
        runner = unittest.TextTestRunner(verbosity=2)
        print("test start:")
        runner.run(tests)
        print("test end!!!")
