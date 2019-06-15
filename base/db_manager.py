# !/uer/bin/env python3

import os

from configElement import conf_load
from base.super_kit.db_super import DB
from base.runner import LOGGER, logged
from base.my_exception import *

try:
    import pymysql
except ImportError:
    os.system('pip3 install pymysql')
import pymysql


class Mysql(DB):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Mysql, cls).__new__(cls)
        return cls.instance

    def __init__(self, **kwargs):

        if not kwargs:
            try:
                conf = conf_load('__conf.yaml').read()
                _server_conf = {'host': conf['MYSQL']['host'],
                                'user': conf['MYSQL']['username'],
                                'passwd': conf['MYSQL']['password'],
                                'port': conf['MYSQL']['port'],
                                'charset': conf['MYSQL']['charset'],
                                'database': conf['MYSQL']['database']}

                self._db = pymysql.connect(**_server_conf)
                self._cursor = self._db.cursor()
                LOGGER.info("数据库连接成功!")
            except ConnectionError as ex:
                LOGGER.error(str(ex))
        else:
            try:
                self._db = pymysql.connect(kwargs)
                self._cursor = self._db.cursor()
                LOGGER.info("数据库连接成功!")
            except ConnectionError as ex:
                LOGGER.error(str(ex))

    @logged
    def select(self, sql):
        if sql[:6] == 'select':
            try:
                with self._db.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                    self._db.ping(reconnect=True)
                    cursor.execute(sql)
                    LOGGER.info("自增id:{}".format(cursor.lastrowid))
                    self._db.commit()
                    result = cursor.fetchone()
                    return result
            except Exception as e:
                self._db.rollback()
                LOGGER.error("执行语句出错了。错误信息：{}".format(e))
            finally:
                self._db.close()
                LOGGER.info("数据库连接关闭!")
        else:
            raise SyntaxException("sql格式错误～")

    @logged
    def select_all(self, sql: str):
        if sql[:6] == 'select':
            try:
                with self._db.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                    self._db.ping(reconnect=True)
                    cursor.execute(sql)
                    LOGGER.info("自增id:{}".format(cursor.lastrowid))
                    self._db.commit()
                    result = cursor.fetchall()
                    return result
            except Exception as e:
                self._db.rollback()
                LOGGER.error("执行语句出错了。错误信息：{}".format(e))
                return False
            finally:
                self._db.close()
                LOGGER.info("数据库连接关闭!")
        else:
            raise SyntaxException("sql格式错误～")

    @logged
    def insert(self, sql):
        if sql[:6] == 'insert':
            try:
                with self._db.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                    self._db.ping(reconnect=True)
                    cursor.execute(sql)
                    LOGGER.info("自增id:{}".format(cursor.lastrowid))
                    self._db.commit()
                    return cursor.lastrowid
            except Exception as e:
                self._db.rollback()
                LOGGER.error("执行语句出错了。错误信息：{}".format(e))
                return False
            finally:
                self._db.close()
                LOGGER.info("数据库连接关闭!")
        else:
            raise SyntaxException("sql格式错误～")

    @logged
    def update(self, sql):
        if sql[:6] == 'update':
            try:
                with self._db.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                    self._db.ping(reconnect=True)
                    cursor.execute(sql)
                    LOGGER.info("自增id:{}".format(cursor.lastrowid))
                    self._db.commit()
                return True
            except Exception as e:
                self._db.rollback()
                LOGGER.error("执行语句出错了。错误信息：{}".format(e))
                return False
            finally:
                self._db.close()
                LOGGER.info("数据库连接关闭!")
        else:
            raise SyntaxException("sql格式错误～")

    @logged
    def delete(self, sql):
        raise NotImplementedError


class Oracle(DB):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Oracle, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super(Oracle, self).__init__()
        pass

    def insert(self, sql):
        raise NotImplementedError

    def select(self, sql):
        raise NotImplementedError

    def select_all(self, sql: str):
        pass

    def update(self, sql):
        raise NotImplementedError


if __name__ == '__main__':
    run = Mysql()
    c1 = run.select(
        "select count(user_id) from yfq_user where register_dt "
        "between str_to_date('%s', '%%Y-%%m-%%d') and str_to_date('%s', '%%Y-%%m-%%d')" % ('2018-11-01', '2018-12-01'))
    print(c1)
