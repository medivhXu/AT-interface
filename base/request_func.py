#!/usr/bin/env python3
import os
import json
import requests
from base.loger import LOGGER
from config_element import conf_load


def request_func(path, request_data, method='post', headers=None, verify=True):
    conf = conf_load('../__conf.yaml').read()['INTERFACE']
    time_out = conf['time_out']
    LOGGER.info('$$$$$ path: {}'.format(path))
    LOGGER.info('***** request: \n{}\n *****'.format(request_data))
    if method == 'post':
        if headers:
            res = requests.post(path, request_data, headers=headers, verify=verify, timeout=time_out)
        else:
            res = requests.post(path, request_data, verify=verify, timeout=time_out)
    elif method == 'get':
        if headers:
            res = requests.get(path, request_data, headers=headers, verify=verify, timeout=time_out)
        else:
            res = requests.get(path, request_data, verify=verify, timeout=time_out)
    else:
        raise NotImplementedError("还没实现！")
    t = res.elapsed.total_seconds() * 1000
    LOGGER.info('*********************************** response: \n{}\n ***********************************, ' \
                '响应时间: {:.2f} ms!'.format(res.text, t))
    if res.status_code != requests.codes.ok:
        LOGGER.warning("[-]请求地址: {}, 参数: {} , 响应: {}".format(path, request_data, res.text))
    return json.loads(res.text)
