#!/usr/bin/env python3

from config_element.yaml_manager import ConfYaml
from base.logger import logged, LOGGER


@logged
def get_var(key, value=None):
    if key == 'phone':
        if value:
            return ConfYaml('user.yaml').read()[value]
        for phone in ConfYaml('user.yaml').read():
            yield phone
    if key == 'user_id' or key == 'token' or key == 'order_id' or key == 'pay_password':
        if value:
            return ConfYaml('user.yaml').read()[value][key]
        else:
            raise ValueError("取 {} 必须传手机号！".format(key))

    globals_var = ConfYaml('global_variable.yaml').read()
    if globals_var:
        if key in globals_var:
            return globals_var[key]
    else:
        return

    LOGGER.info('key :{}, value: {}'.format(key, value))
    raise KeyError("没找到变量！")


@logged
def push_var(var, phone, value=None) -> bool:
    if var == 'phone':
        return ConfYaml('user.yaml').update({phone: None})
    if var == 'user_id' or var == 'token' or var == 'order_id' or var == 'pay_password':
        if value:
            return ConfYaml('user.yaml').update({phone: {var: value}})
        else:
            raise ValueError("取 {} 必须传手机号！".format(var))

    return ConfYaml('global_variable.yaml').update({var: phone})
