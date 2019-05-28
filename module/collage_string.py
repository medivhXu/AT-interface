# !/uer/bin/env python3
# coding=utf-8
import time
from base.log import logged
from base.encrypt import Encryption
from configElement.yaml_manager import ConfYaml


class CollageStr(object):
    """核心加密算法，对请求参数进行拼接"""

    @logged
    def __init__(self, data: dict, interface_yaml_filename='cases.yaml', conf_yaml_filename='__conf.yaml',
                 user_yaml_filename='user.yaml', global_variable_filename='global_variable.yaml'):
        """
        加载变量
        :param data:
        :param interface_yaml_filename:
        :param conf_yaml_filename:
        :param user_yaml_filename:
        :param global_variable_filename:
        """
        self._interface_data = ConfYaml(interface_yaml_filename).read()
        self._data = dict(data)
        self._conf_data = ConfYaml(conf_yaml_filename).read()
        self._user_data = ConfYaml(user_yaml_filename).read()
        self._global_var = ConfYaml(global_variable_filename).read()

    @logged
    def order_str(self, phone=None, platform='APP', os='ios') -> dict:
        """
        加密串拼接
        :param phone: 用户参数化取值
        :param platform: 请求平台参数
        :param os: 请求平台系统
        :return: type(dict)
        """
        sort_str = ''
        self._data['app_key'] = self._conf_data[platform][os]['app_key']
        self._data['timestamp'] = str(round(time.time() * 1000))
        if phone:
            self._data['token'] = self._user_data[phone]['token'] or ''
        if self._conf_data[platform][os]['app_version']:
            self._data['app_version'] = self._conf_data[platform][os]['app_version']
        self._data['os'] = self._conf_data[platform][os]['app_key'].split('_')[-1]
        if self._global_var:
            self._data.update(self._global_var)
        app_secret = self._conf_data[platform][os]['app_secret']
        s_list = sorted(self._data, key=str.lower)
        for i in s_list:
            sort_str += ''.__add__(i + str(self._data.get(i)))
        string = app_secret + sort_str + app_secret
        md5_str = Encryption.md5(string)
        self._data['sign'] = str(md5_str).lower()
        return self._data
