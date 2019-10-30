#!/usr/bin/env python3

import os
import logging
import traceback
import inspect
import datetime
import functools

logs_dir_name = 'logs'
__dir__ = os.path.dirname(os.path.abspath(__file__))

if logs_dir_name not in os.listdir(os.path.join(__dir__, '../')):
    os.mkdir(''.join((os.path.join(__dir__, '../'), logs_dir_name)))

_now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
_logs_dir_path = os.path.join(__dir__, ''.join(('../', logs_dir_name, '/')))
log_fp = ''.join((_logs_dir_path, _now, ".log"))

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=log_fp,
                    filemode='w')

_console = logging.StreamHandler()
_console.setLevel(logging.INFO)
_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
_console.setFormatter(_formatter)
LOGGER = logging.getLogger('czb test')
LOGGER.addHandler(_console)


def logged(func):
    """创建一个日志装饰器，它会记录所装饰函数的入参和
    """
    result = None

    @functools.wraps(func)
    def inner(*args, **kwargs):

        try:
            nonlocal result
            result = func(*args, **kwargs)
            LOGGER.info('模块:{}\n 调用函数 {} 传入参数: {},{}\n 返回结果: {}'
                        .format(inspect.getmodule(func), func.__name__,
                                args, kwargs, result))
            return result
        except Exception as Ex:
            LOGGER.error("{}方法入参:{},{}".format(func.__name__, args, kwargs))
            e = traceback.format_exc()
            LOGGER.error('Exception：{}'.format(e))
            raise Ex

    return inner
