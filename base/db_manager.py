# !/uer/bin/env python3

import pymysql
import contextlib
from base.runner import LOGGER
from configElement.yaml_manager import ConfYaml


@contextlib.contextmanager
def mysql():
    """
    mysql连接方法
        examples:

                with mysql() as cur:
                    cur.execute('select * from czb_message.sms_log where mobile=18515966636 group by send_time DESC limit 1;')
                    result = cur.fetchall()
                    print(result)
    :return: 游标
    """
    conf = ConfYaml('../__conf.yaml').read()['MYSQL']
    conn = pymysql.connect(**conf)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    except Exception as e:
        LOGGER.error(e)
    finally:
        conn.commit()
        cur.close()
        conn.close()
