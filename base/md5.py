# !/uer/bin/env python3
# coding=utf-8
import hashlib
import base64
import os
import json
from base.log import logged
try:
    from pyDes import *
except ImportError as e:
    os.system('pip install -U pyDes --allow-external pyDes --allow-unverified pyDes')
    from pyDes import *


class Encryption(object):
    """对参数进行md5加密"""
    @staticmethod
    @logged
    def md5(string):
        md = hashlib.md5()
        md.update(string.encode(encoding='utf-8'))
        _md5_msg = str(md.hexdigest())
        return _md5_msg

    @staticmethod
    @logged
    def des(string, secret_key):
        _key = des(secret_key, padmode=PAD_PKCS5)
        _des_str = base64.b64encode(_key.encrypt(json.dumps(string)))
        return _des_str
