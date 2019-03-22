# !/uer/bin/env python3
# coding=utf-8
from base.log import logged


@logged
def differences(exp: dict, resp: dict) -> set or bool:
    """
    :parameter exp是期望
    :parameter resp是返回值
    :return diff (差异值, type(dict))
    """
    if exp == resp:
        return True
    diff = {}
    for key, value in exp.items():
        try:
            if resp[key] == value:
                resp.pop(key)
            if isinstance(exp[key], list):
                for ad in exp[key]:
                    for bd in resp[key]:
                        differences(ad, bd)
        except KeyError:
            diff[key] = value
    diff.update(resp)
    return diff
