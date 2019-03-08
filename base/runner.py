# !/uer/bin/env python3
# coding=utf-8
import datetime
import os
from base import HTMLTestReportCN
import unittest
from analysis.send_email import SendEmail


class TestRunner(object):
    def __init__(self, cases="./", title="czb Test Report", description="Test case execution", tester="system"):
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
        file_path = "./report/" + now + "result.html"
        fp = open(file_path, 'wb')
        tests = unittest.defaultTestLoader.discover(self.cases, pattern='test*.py', top_level_dir=None)
        runner = HTMLTestReportCN.HTMLTestRunner(stream=fp, title=self.title, description=self.des, tester=self.tester)
        runner.run(tests)
        fp.close()
        email_obj = SendEmail()
        email_obj.send_html_to_email(file_path)

    def debug(self):
        tests = unittest.defaultTestLoader.discover(self.cases, pattern='test*.py', top_level_dir=None)
        runner = unittest.TextTestRunner(verbosity=2)
        print("test start:")
        runner.run(tests)
        print("test end!!!")


if __name__ == '__main__':
    test = TestRunner()
    test.run()