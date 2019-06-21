# !/uer/bin/env python3

import yaml


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
        """
        17500123456:
          order_id: 3333
          pay_password: 123456
          token: null
          user_id: 12345
        13800138000:
          order_id: 5555
          pay_password: 123456
          token: null
          user_id: 12345
        :param dict_var: type(dict)
        :return:
        """
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

    def _reset(self, doc: dict):
        """
        case:
          1:
            name: "发送短信"
            request:
              checkpoint:
                text:
                  code: 200
              data:
                phone: $phone
                token: $token_data
              path: /services/v3/begin/sendMsg
            response:
          2:
            name: "登录"
            request:
              path: /services/v3/begin/loginAppV42
              data:
                phone: $phone
                code: $$get_db_msg($phone)
                token:
            response:
              text:
                token: $token

        host:
          port: null
        """
        with open(self._conf_path, 'w', encoding='utf-8') as nf:
            yaml.dump(yaml.load(doc), nf, default_flow_style=False)
