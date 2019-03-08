# !/uer/bin/env python3
# coding=utf-8
import time
from base.log import logged
from base.md5 import Encryption
from base.conf_manager import ConfYaml


class CollageStr(object):
    """核心加密算法，对请求参数进行拼接"""
    @logged
    def __init__(self, string):
        self._interface_data = ConfYaml('interface.yaml')
        self._string = string
        self._conf_data = ConfYaml('__conf.yaml')
        self._user_data = ConfYaml('user.yaml')

    @logged
    def sign_str(self, phone, platform='APP', os='ios'):
        sort_str = ''
        self._string['app_key'] = self._interface_data.read()[platform][os]['app_key']
        self._string['timestamp'] = str(round(time.time() * 1000))
        self._string['token'] = self._user_data.read()[phone]['token']
        self._string['app_version'] = self._conf_data.read()[platform][os]['app_version']
        app_secret = self._conf_data.read()[platform][os]['app_secret']
        s_list = sorted(self._string, key=str.lower)
        for i in s_list:
            sort_str += ''.__add__(i + str(self._string.get(i)))
        string = app_secret + sort_str + app_secret
        md = Encryption.md5(string)
        self._string['sign'] = str(md).lower()
        return self._string
