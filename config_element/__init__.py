#!/usr/bin/env python3

import re
import os

from config_element.yaml_manager import ConfYaml
from config_element.xlsx_manager import ConfExcel
from config_element.charles_file_load import CharlesFileLoad
from base.loger import LOGGER

DP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')


def conf_load(file_name):
    """
    读取配置文件，如果文件名包含文件后缀，则自动找到最近修改的文件
    :param file_name:
        示例: 'cases.yaml' or file point
    :return: type(obj)
    """
    if '../' in file_name:
        fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
        file_type = file_name.split('/')[-1].split('.')[-1]
        if 'yaml' == file_type:
            return ConfYaml(fp)
        else:
            return ConfExcel(fp)

    fp = os.path.join(DP, file_name)
    if os.path.isfile(fp):
        file_type = file_name.split('.')[-1]
        if 'yaml' == file_type:
            return ConfYaml(fp)
        else:
            return ConfExcel(fp)
    else:
        # 取最新修改的文件
        files = os.listdir(DP)
        file_name_split = file_name.split('.')
        if len(file_name_split) > 1:
            files_dict = {f: os.stat(os.path.join(DP, f)).st_mtime for f in files if
                          re.search('{}.*.{}'.format(file_name_split[0], file_name_split[-1]), f)}
        else:
            files_dict = {f: os.stat(os.path.join(DP, f)).st_mtime for f in files if
                          re.search('{}.*'.format(file_name_split[0]), f)}
        try:
            new_modify = max(zip(files_dict.values(), files_dict.keys()))[1]
            file_type = new_modify.split('.')[-1]
            fp = os.path.join(DP, new_modify)
            if 'yaml' == file_type:
                return ConfYaml(fp)
            else:
                return ConfExcel(fp)
        except ValueError:
            raise NameError("文件名没匹配到，请确认是否存在该文件！")


def cases_load(dir_name='cases_files', case_sort=None):
    """
    分别加载用例文件夹中的用例文件内的所有用例数据，如果排序不为空，就按照排序的顺序加载用例到中间文件中，intermediate.yaml
    :param dir_name: 用例存储的文件夹
    :param case_sort: 用例排列的顺序， type(list)
    :return:
    """
    dp = os.path.join(DP, dir_name)
    intermediate = os.path.join(dp, '../intermediate.yaml')
    if ConfYaml(intermediate).read():
        ConfYaml(intermediate).delete()
    if os.path.isdir(dp):
        order_file_list = []
        file_list = os.listdir(dp)
        if '.DS_Store' in file_list:
            file_list.remove('.DS_Store')
        if case_sort:
            for i in case_sort:
                order_file_list.extend([y for y in file_list if i == int(y.split('_')[0])])
        else:
            order_file_list = sorted(file_list, key=lambda x: int(x.split('_')[0]))
        for file_name in order_file_list:
            fp = os.path.join(dp, file_name)
            if 'yaml' == file_name.split('.')[-1]:
                source_data = ConfYaml(fp).read()
                intermediate_data = ConfYaml(intermediate)
                intermediate_data.add(source_data)
            elif 'chlsj' == file_name.split('.')[-1]:
                # 支持多个chlsj文件，但不能去重
                source_data = CharlesFileLoad(fp).chlsj_load()
                intermediate_data = ConfYaml(intermediate)
                intermediate_data.add(source_data)
            else:
                LOGGER.warning("{}文件夹下存在其他类型文件，系统直接忽略！".format(dp))
        cases = ConfYaml(intermediate).read()
        return cases
    else:
        raise NotADirectoryError("{} 不存在该文件夹！",dir_name)


if __name__ == '__main__':
    cases_load()
