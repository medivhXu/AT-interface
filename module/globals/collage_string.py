# !/uer/bin/env python3

import time
from base.loger import logged, LOGGER
from base.encrypt import Encryption
from config_element import conf_load


class CollageStr(object):
    """核心加密算法，对请求参数进行拼接"""

    def __init__(self, data: dict, conf_yaml_filename='__conf.yaml', user_yaml_filename='user.yaml',
                 global_variable_filename='global_variable.yaml'):
        """
        加载变量
        :param data:
        :param conf_yaml_filename:
        :param user_yaml_filename:
        :param global_variable_filename:
        """
        self._data = dict(data)
        self._conf_data = conf_load(conf_yaml_filename).read()
        self._user_data = conf_load(user_yaml_filename).read()
        self._global_var = conf_load(global_variable_filename).read()

    def order_str(self, phone=None, platform='APP', os='ios') -> dict:
        """
        加密串拼接
        :param phone: 用户参数化取值
        :param platform: 请求平台参数
        :param os: 请求平台系统
        :return: type(dict)
        """
        for k, v in self._conf_data[platform][os].items():
            if k == 'app_secret':
                continue
            self._data[k] = v or ''

        self._data['timestamp'] = str(round(time.time() * 1000))

        if phone:
            try:
                self._data['token'] = self._user_data[phone]['token'] or ''
            except KeyError:
                LOGGER.warn('用户文件中没有{}的对应关系，默认设置为空!'.format(phone))
                self._data['token'] = ''

        if self._global_var:
            self._data.update(self._global_var)

        app_secret = self._conf_data[platform][os]['app_secret']

        s_list = sorted(self._data, key=str.lower)
        sort_str = ''
        for i in s_list:
            sort_str += ''.__add__(i + str(self._data.get(i)))
        string = sort_str.join((app_secret, app_secret))
        md5_str = Encryption.md5(string)
        self._data['sign'] = str(md5_str).lower()
        return self._data
