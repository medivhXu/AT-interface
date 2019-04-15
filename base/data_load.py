#!/usr/bin/env python3

import os

from configElement.yaml_manager import ConfYaml
from configElement.xlsx_manager import ReadData
from base.my_exception import *


def file_load(file_name):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
    if file_name in os.listdir(path):
        file_name_cut_list = str(file_name).split('.')
        suffix = file_name_cut_list[-1]
        prefix = file_name_cut_list[0]
        if suffix == 'yaml':
            conf = ConfYaml(os.path.join(path, file_name)).read()
            return conf
        elif suffix == 'xlsx':
            xlsx_obj = ReadData(os.path.join(path, file_name))
            if prefix == 'cases':
                conf = xlsx_obj.get_cases_data()
                return conf
            elif prefix == 'global_variable':
                conf = xlsx_obj.get_global_variable()
                return conf
            elif prefix == 'user':
                conf = xlsx_obj.get_user_data()
                return conf
            else:
                raise MyException("未知异常！")
        else:
            raise UnsupportedFile("不支持 {} 类型文件！".format(suffix))
    else:
        raise FileNotFoundError("没找到文件，请将文件放到 {} 文件夹下！".format(path))



