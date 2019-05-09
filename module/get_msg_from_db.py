# !/uer/bin/env python3
# coding=utf-8
import re
from base.db_manager import Mysql
from base.log import logged, LOGGER


@logged
def get_msg_from_db(phone) -> int:
    sql = "select msg from czb_message.sms_log where mobile={} group by send_time DESC limit 1".format(int(phone))
    result = Mysql().select(sql)
    re_r = re.compile("\d{4}", re.S)
    try:
        code = re.findall(re_r, result.get('msg'))
        if len(code):
            return code[0]
    except TypeError as e:
        LOGGER.error("运行失败，查询结果不能正常匹配！异常：{}".format(e))
        return False
