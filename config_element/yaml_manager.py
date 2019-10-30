# !/uer/bin/env python3

import yaml
# from ruamel import yaml


class ConfYaml(object):
    """读写配置文件类"""

    def __init__(self, fp):
        self._conf_path = fp

    def new(self, data):
        with open(self._conf_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)

    def read(self):
        """
        读取conf文件
        :return: type(dict)
        """
        with open(self._conf_path, 'r', encoding='utf-8') as f:
            text = yaml.load(f, Loader=yaml.Loader)
            return text

    def update(self, dict_var: dict) -> bool:
        text = self.read()
        for d1 in dict_var:
            if isinstance(dict_var[d1], dict):
                if d1 in text:
                    for k in dict_var[d1]:
                        text[d1][k] = dict_var[d1][k]
                else:
                    text[d1] = dict_var[d1]
            else:
                text.update(dict_var)

        with open(self._conf_path, 'w', encoding='utf-8') as nf:
            yaml.dump(text, nf, default_flow_style=False)
        return True

    def add(self, text):
        new_text = []
        if isinstance(self.read(), list):
            new_text.extend(self.read())
            new_text.extend(text)
            with open(self._conf_path, 'w', encoding='utf-8') as nf:
                yaml.dump(new_text, nf, default_flow_style=False)
        elif not self.read():
            with open(self._conf_path, 'w', encoding='utf-8') as nf:
                yaml.dump(text, nf, default_flow_style=False)
        else:
            raise NotImplementedError

    def delete(self):
        with open(self._conf_path, 'w', encoding='utf-8') as nf:
            yaml.dump(None, nf, default_flow_style=False)
