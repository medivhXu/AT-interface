# !/uer/bin/env python3

import pymysql
import contextlib
from base.loger import LOGGER
from config_element import conf_load


@contextlib.contextmanager
def mysql(db_conf=None):
    """
    mysql连接方法
        examples:

                with mysql() as cur:
                    cur.execute('select * from czb_message.sms_log where mobile=18515966636 group by send_time DESC limit 1;')
                    result = cur.fetchall()
                    print(result)
    :return: 游标
    """
    if not db_conf:
        conf = conf_load('../__conf.yaml').read()['MYSQL']
    else:
        conf = db_conf
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
