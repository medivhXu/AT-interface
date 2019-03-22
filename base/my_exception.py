# !/uer/bin/env python3
# coding=utf-8


class MyException(Exception):
    def __init__(self, msg, data=None):
        self._msg = msg
        self._data = data

    def __str__(self):
        if self._data:
            return "{}, data:{}".format(self._msg, self._data)
        return self._msg

    def __repr__(self):
        return repr(self._msg)


class ReadConfException(MyException):
    pass


class MethodException(MyException):
    pass


class ConfigurationException(MyException):
    pass


class UpdateConfException(MyException):
    pass
