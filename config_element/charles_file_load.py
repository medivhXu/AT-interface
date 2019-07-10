#!/usr/bin/env python3

from urllib import parse
from config_element.yaml_manager import ConfYaml


class CharlesFileLoad:
    """
    批量读取charles文件，写入到yaml文件，以后优化到mysql
    """
    def __init__(self, fp):
        self.fp = fp
        self.conf = ConfYaml('../__conf.yaml')

    def load(self):
        with open(self.fp, 'r', encoding='utf-8') as f:
            word = f.read()
            decode_word = parse.unquote(word)
            dict_socket = {i.split('=')[0]: i.split('=')[1] for i in decode_word.split('&')}

            return dict_socket


if __name__ == '__main__':
    r = CharlesFileLoad('/Users/medivhxu/Desktop/interface/sendMsg')
    res = r.load()
    print(res)
