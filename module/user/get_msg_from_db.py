# !/uer/bin/env python3
# coding=utf-8
import re
from base.db_manager import mysql
from base.runner import logged, LOGGER


@logged
def get_msg_from_db(phone) -> int:
    with mysql() as cur:
        cur.execute('select msg from czb_message.sms_log where mobile=%s group by send_time DESC limit 1', (phone,))
        result = cur.fetchall()
        re_r = re.compile("\d{4}", re.S)
        try:
            code = re.findall(re_r, result[0].get('msg'))
            if len(code):
                return code[0]
        except TypeError as e:
            LOGGER.error("运行失败，查询结果不能正常匹配！异常：{}".format(e))
            return False
