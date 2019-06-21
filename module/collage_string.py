# !/uer/bin/env python3

import time
from base.runner import logged, LOGGER
from base.encrypt import Encryption
from configElement import conf_load


class CollageStr(object):
    """核心加密算法，对请求参数进行拼接"""

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
        self._interface_data = conf_load(interface_yaml_filename).read()
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
            except KeyError as e:
                LOGGER.warn('获取数据时，没有这条数据，报错已自动修正: {}'.format(e))
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

    def test(self):
        app_secret = '156cd1010214343cd0830330117580bd'
        self._data['timestamp'] = str(round(time.time() * 1000))
        s_list = sorted(self._data, key=str.lower)
        sort_str = ''
        for i in s_list:
            sort_str += ''.__add__(i + str(self._data.get(i)))
        string = sort_str.join((app_secret, app_secret))
        md5_str = Encryption.md5(string)
        self._data['sign'] = str(md5_str).lower()
        return self._data


if __name__ == '__main__':
    a = {'gasIds': 'SD000011427', 'platformType': 92650965, 'phone': 18515966636, 'app_key': 'ectzhushou1.0'}
    r = CollageStr(a)
    print(r.test())
