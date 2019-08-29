# !/uer/bin/env python3

from base.my_exception import *
from module.globals.collage_string import CollageStr
from module.globals.get_variable import get_var
from module.user.get_msg_from_db import get_msg_from_db
from module.order.random_outer_order_no import get_random_outer_order_id


def pretreatment(unit_test_subclass, TEMPORARY_VARIABLE, PHONE_WORD='phone'):
    """
    前置数据处理
        接口请求 -> 如果需要用调用系统方法& -> 存入全局变量 -> 下一个请求从全局变量里取%
        接口请求请求数据从配置文件中取$ -> 如果需要用调用系统方法& -> 存入全局变量 -> 下一个请求从全局变量里取%

        $：表示从配置文件中取值
        %：代表从全局变量中取值
        &：表示运行系统方法
        $&：表示从上一个接口中取数据
    :param unit_test_subclass: 
    :param TEMPORARY_VARIABLE: 公共变量
    :param PHONE_WORD: 手机号字段名
    :return:
    """
    for d in unit_test_subclass.data:
        # 变量中有系统方法的
        if '&' in str(unit_test_subclass.data[d]):
            func_str = unit_test_subclass.data[d].replace('&', '')
            func = func_str.split('(')[0]
            result = []
            # 带参方法
            if '%' in func_str:
                var = func_str.split('%')[-1].replace(')', '')
                value = TEMPORARY_VARIABLE[var]
                try:
                    if eval(func)(value).__next__():
                        for i in eval(func)(value):
                            result.append(i)
                        # 待优化
                        unit_test_subclass.data[d] = result[0]
                except AttributeError:
                    unit_test_subclass.data[d] = eval(func)(value)
            # 从配置文件里加载系统方法参数
            elif '$' in func_str:
                var = func_str.split('$')[-1].replace(')', '')
                value = get_var(var, TEMPORARY_VARIABLE.get(PHONE_WORD))
                try:
                    if eval(func)(value).__next__():
                        for i in eval(func)(value):
                            result.append(i)
                        unit_test_subclass.data[d] = result[0]
                except AttributeError:
                    unit_test_subclass.data[d] = eval(func)(value)
            else:
                try:
                    if eval(func)().__next__():
                        for i in eval(func)():
                            result.append(i)
                        unit_test_subclass.data[d] = result[0]
                except AttributeError:
                    unit_test_subclass.data[d] = eval(func)()

        # 从全局变量中取值
        if '%' in str(unit_test_subclass.data[d]):
            try:
                unit_test_subclass.data[d] = TEMPORARY_VARIABLE[unit_test_subclass.data[d].split('%')[-1]]
            except KeyError:
                raise KeyError("全局变量中没有该字段，可能上次请求中没取出来该值！")

        # 从配置文件中取值
        if '$' in str(unit_test_subclass.data[d]):
            k = unit_test_subclass.data[d].split('$')[-1].replace(')', '')

            # get('phone') 需要改
            result = get_var(k, TEMPORARY_VARIABLE.get(PHONE_WORD))
            unit_test_subclass.data[d] = result
            TEMPORARY_VARIABLE[d] = result

        # 如果请求参数中包含token字段，把它置成空字符串
        if not unit_test_subclass.data[d] and d == 'token':
            unit_test_subclass.data[d] = ''

    global request_data
    # 如果request data里面写死手机号，这里捕获后，直接传给参数排序
    if PHONE_WORD in TEMPORARY_VARIABLE.keys():
        phone = TEMPORARY_VARIABLE[PHONE_WORD]
        try:
            if unit_test_subclass.limit.get('os'):
                request_data = CollageStr(unit_test_subclass.data).order_str(phone=phone,
                                                                             os=unit_test_subclass.limit.get('os'))
        except AttributeError:
            request_data = CollageStr(unit_test_subclass.data).order_str(phone=phone)
    else:
        try:
            request_data = CollageStr(unit_test_subclass.data).order_str(
                phone=unit_test_subclass.data.get(PHONE_WORD),
                os=unit_test_subclass.limit.get('os'))
        except AttributeError:
            request_data = CollageStr(unit_test_subclass.data).order_str(
                phone=unit_test_subclass.data.get(PHONE_WORD))
    return request_data
