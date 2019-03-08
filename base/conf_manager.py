# !/uer/bin/env python3
# coding=utf-8
import os
import yaml
from base.log import logged


class ConfYaml(object):
    """读写配置文件类"""

    @logged
    def __init__(self, conf_file_name='__conf.yaml'):
        self._conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../{}'.format(conf_file_name))

    @logged
    def read(self):
        """
        读取conf文件
        :return: type(dict)
        """
        with open(self._conf_path, 'r', encoding='utf-8') as f:
            text = yaml.load(f, Loader=yaml.Loader)
            return text

    @logged
    def update(self, doc):
        """
        host:
          port:

        case:
          1:
            name: 短信
            request:
              path: /services/v3/begin/sendMsg
              data:
                phone: 13800138000
              checkpoint:
                text:
                  code: 200
            response:
          2:
            name: 登录
            request:
              path: /services/v3/begin/loginAppV4
        """
        text = self.read()
        text.update(doc)
        with open(self._conf_path, 'w') as nf:
            yaml.dump(text, nf, default_flow_style=False)
        return True

    @logged
    def _reset(self, doc):
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
