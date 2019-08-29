#!/usr/bin/env python3

import re
from base.my_exception import *


def post_processing(unit_test_subclass, res, TEMPORARY_VARIABLE):
    """
        $：表示从配置文件中取值
        %：代表从全局变量中取值
        &：表示运行系统方法
        $&：表示从上一个接口中取数据
    :param unit_test_subclass:
    :param res:
    :param TEMPORARY_VARIABLE:
    :return:
    """
    if unit_test_subclass.check_point:
        for k, v in unit_test_subclass.check_point.items():
            if v:
                if isinstance(v, dict):
                    for k1, v1 in v.items():
                        if v1:
                            if '$&' in v1:
                                var = v1.split('$&')[-1]
                                try:
                                    result = re.findall('"{}":"(.+?)"'.format(var), res.text)
                                    TEMPORARY_VARIABLE[var] = result[0]
                                    continue
                                except IndexError:
                                    raise MatchException("未匹配到结果！")
                        else:
                            pass
                elif '$&' in str(v):
                    var = v.split('$&')[-1]
                    try:
                        result = re.findall('"{}":"(.+?)"'.format(var), res.text)
                        TEMPORARY_VARIABLE[var] = result[0]
                        continue
                    except IndexError:
                        raise MatchException("未匹配到结果！")
                elif '200' == res.text:
                    unit_test_subclass.assertEqual(str(v), res.text, "不通过")
                elif k in res.text:
                    if isinstance(v, int):
                        unit_test_subclass.assertIn('"{}":{}'.format(k, v), res.text, "不通过")
                    else:
                        unit_test_subclass.assertIn('"{}":"{}"'.format(k, v), res.text, "不通过")
                else:
                    raise KeyError("检查点错误，{}不在响应中！".format(k))
            else:
                pass
