#!/usr/bin/env python3

import json
import requests
from base.logger import LOGGER
from config_element import conf_load


def request_func(path, request_data, method='post', headers=None, verify=True):
    conf = conf_load('../__conf.yaml').read()['INTERFACE']
    time_out = conf['time_out']
    LOGGER.info('$$$$$ path: {}'.format(path))
    LOGGER.info('\n**************** request ******************* \n{}\n********************************************\n'
                .format(request_data))
    if method.lower() == 'post':
        if headers:
            res = requests.post(path, request_data, headers=headers, verify=verify, timeout=time_out)
        else:
            res = requests.post(path, request_data, verify=verify, timeout=time_out)
    elif method.lower() == 'get':
        if headers:
            res = requests.get(path, request_data, headers=headers, verify=verify, timeout=time_out)
        else:
            res = requests.get(path, request_data, verify=verify, timeout=time_out)
    else:
        raise NotImplementedError("还没实现！")
    t = res.elapsed.total_seconds() * 1000
    LOGGER.info('\n***************** response ****************** \n{}\n*********************************************\n' \
                '响应时间: {:.2f} ms!'.format(res.text, t))
    if res.status_code != requests.codes.ok:
        LOGGER.warning("[-]请求地址: {}, 参数: {} , 响应: {}".format(path, request_data, res.text))
    return res
