#!/usr/bin/env python3


def compare_json_data(exp, resp, xpath='.'):
    if isinstance(exp, list) and isinstance(resp, list):
        for i in range(len(exp)):
            try:
                compare_json_data(exp[i], resp[i], xpath + '[%s]' % str(i))
            except:
                print('▇▇▇▇▇ A中的%s[%s]未在B中找到' % (xpath, i))
    if isinstance(exp, dict) and isinstance(resp, dict):
        for i in exp:
            try:
                resp[i]
            except:
                print('▇▇▇▇▇ A中的%s/%s 未在B中找到' % (xpath, i))
                continue
            if not (isinstance(exp.get(i), (list, dict)) or isinstance(resp.get(i), (list, dict))):
                if type(exp.get(i)) != type(resp.get(i)):
                    print('▇▇▇▇▇ 类型不同参数在[A]中的绝对路径:  %s/%s  ►►► A is %s, B is %s ' % (
                        xpath, i, type(exp.get(i)), type(resp.get(i))))
                elif exp.get(i) != resp.get(i):
                    print(
                        '▇▇▇▇▇ 仅内容不同参数在[A]中的绝对路径:  %s/%s  ►►► A is %s, B is %s ' % (xpath, i, exp.get(i), resp.get(i)))
                continue
            compare_json_data(exp.get(i), resp.get(i), xpath + '/' + str(i))
        return
    if type(exp) != type(resp):
        print('▇▇▇▇▇ 类型不同参数在[A]中的绝对路径:  %s  ►►► A is %s, B is %s ' % (xpath, type(exp), type(resp)))
    elif exp != resp and type(exp) is not list:
        print('▇▇▇▇▇ 仅内容不同参数在[A]中的绝对路径:  %s  ►►► A is %s, B is %s ' % (xpath, exp, resp))
