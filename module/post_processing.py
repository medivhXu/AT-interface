#!/usr/bin/env python3


def post_processing(unit_test_subclass, dict_res, TEMPORARY_VARIABLE):
    """
        $：表示从配置文件中取值
        %：代表从全局变量中取值
        &：表示运行系统方法
        $&：表示从上一个接口中取数据
    :param unit_test_subclass:
    :param dict_res:
    :param TEMPORARY_VARIABLE:
    :return:
    """
    if unit_test_subclass.check_point:
        for po in unit_test_subclass.check_point.keys():
            for var in unit_test_subclass.check_point[po].keys():
                # 取后置参数所需变量, 这里可以扩展一个正则表达式提取器
                if isinstance(dict_res, int):
                    unit_test_subclass.assertEqual(unit_test_subclass.check_point[po][var], dict_res, '预期不符～')
                    continue
                if isinstance(dict_res['result'], list):
                    TEMPORARY_VARIABLE[var] = [po_word for po_word in dict_res['result'] if
                                               '$&' in unit_test_subclass.check_point[po][var]]
                    continue
                if '$&' in str(unit_test_subclass.check_point[po][var]):
                    # 这有个问题，如果conf.yaml中json层级发生变化，代码会报错
                    TEMPORARY_VARIABLE[var] = dict_res['result'][var]
                    # push_var(var, self.data[PHONE_WORD], dict_res['result'][var])
                    continue
                if po == 'text':
                    if not isinstance(dict_res, dict):
                        unit_test_subclass.assertEqual(unit_test_subclass.check_point[po][var], dict_res, '预期不符～')
                    else:
                        unit_test_subclass.assertIn(unit_test_subclass.check_point[po][var], dict_res.values(), '预期不符～')
                elif po == 'result':
                    unit_test_subclass.assertIn(unit_test_subclass.check_point[po][var], dict_res[po], '预期不符～')
