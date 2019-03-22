# !/uer/bin/env python3
# coding=utf-8
import re
from base.db_manager import Mysql
from base.log import logged


@logged
def get_msg_from_db(phone) -> int:
    sql = "select msg from czb_message.sms_log where mobile={} group by send_time DESC limit 1".format(phone)
    result = Mysql().select(sql)
    re_r = re.compile("\d{4}", re.S)
    code = re.findall(re_r, result[0])
    return code[0]

