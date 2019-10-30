#!/usr/bin/env python3

import json

from urllib import parse


class CharlesFileLoad:
    """
    批量读取charles文件，写入到yaml文件，以后优化到mysql
    """

    def __init__(self, fp):
        self.fp = fp

    def load(self):
        with open(self.fp, 'r', encoding='utf-8') as f:
            word = f.read()
            decode_word = parse.unquote(word)
            dict_socket = {i.split('=')[0]: i.split('=')[1] for i in decode_word.split('&')}

            return dict_socket

    def chlsj_load(self):
        with open(self.fp, 'r', encoding='utf-8') as f:
            word = f.read()
            list_word = json.loads(word)
            case_no = 1
            cases = []
            for case_dict in list_word:
                new_case_dict = {}
                for k, v in case_dict.items():
                    if k in ('method', 'scheme', 'host', 'port', 'path'):
                        if isinstance(v, str):
                            new_case_dict[k] = parse.unquote(v)
                    elif k == 'request':
                        new_case_dict['data'] = {
                            i.split('=')[0]: parse.unquote(i.split('=')[1]).encode('utf-8').decode('utf-8') for i in
                            v.get('body').get('text').split('&')}
                        new_case_dict['headers'] = {i.get("name"): i.get("value") for i in
                                                    v.get('header').get('headers')}
                    elif k == 'response':
                        new_case_dict['check_point'] = json.loads(v.get('body').get('text'))
                    else:
                        pass
                new_case_dict.update({'case_no': case_no})
                cases.append(new_case_dict)
                case_no += 1
            return cases
