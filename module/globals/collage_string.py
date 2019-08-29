# !/uer/bin/env python3

import time
from base.loger import logged, LOGGER
from base.encrypt import Encryption
from config_element import conf_load


class CollageStr:
    """核心加密算法，对请求参数进行拼接"""

    def __init__(self, data: dict, conf_yaml_filename='__conf.yaml', user_yaml_filename='user.yaml',
                 global_variable_filename='global_variable.yaml'):
        self._data = dict(data)
        self._conf_data = conf_load(conf_yaml_filename).read()
        self._user_data = conf_load(user_yaml_filename).read()
        self._global_var = conf_load(global_variable_filename).read()

    def order_str(self, phone=None, platform='APP', os='ios') -> dict:
        if 'sign' in self._data:
            self._data.pop('sign')
        for k, v in self._conf_data[platform][os].items():
            if k == 'app_secret':
                continue
            self._data[k] = v or ''

        self._data['timestamp'] = str(round(time.time() * 1000))

        if phone and len(str(phone)) == 11:
            if self._user_data.get(phone):
                for k, v in self._user_data.get(phone).items():
                    try:
                        if k == 'token':
                            if self._data[k]:
                                if v:
                                    self._data[k] = v
                                    continue
                        if k == 'payPassword':
                            if self._data[k]:
                                if isinstance(self._data[k], int):
                                    self._data[k] = Encryption.md5(str(self._data[k]))
                                    continue
                            elif v:
                                if isinstance(v, int):
                                    self._data[k] = Encryption.md5(str(self._user_data[phone][k]))
                                    continue
                                else:
                                    self._data[k] = v
                            else:
                                LOGGER.error("支付密码不能为空！")
                    except KeyError:
                        LOGGER.warning('用户文件中没有{}的对应关系，默认设置为空!'.format(phone))
                        pass

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
