# !/uer/bin/env python3

import os
import configparser

from base.super_kit.db_super import DB
from base.log import LOGGER, logged


class Mysql(DB):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Mysql, cls).__new__(cls)
        return cls.instance

    def __init__(self, **kwargs):
        try:
            import pymysql
        except ImportError:
            os.system('pip3 install pymysql')
        import pymysql

        if not kwargs:
            db_name = "SERVER"
            try:
                _conf = configparser.ConfigParser()
                _conf.read('../__conf.ini')
                _server_conf = {'host': _conf.get(db_name, "host"),
                                'user': _conf.get(db_name, "username"),
                                'passwd': _conf.get(db_name, "password"),
                                'port': int(_conf.get(db_name, "port")),
                                'charset': _conf.get(db_name, "charset")}

                self._db = pymysql.connect(**_server_conf)
                self._cursor = self._db.cursor()
                LOGGER.info("数据库连接成功!")
            except ConnectionError as ex:
                LOGGER.error(str(ex))
        else:
            try:
                self._db = pymysql.connect(**kwargs)
                self._cursor = self._db.cursor()
                LOGGER.info("数据库连接成功!")
            except ConnectionError as ex:
                LOGGER.error(str(ex))

    @logged
    def select(self, sql):
        """

        :param sql:
        :return: type(tuple)
        """
        try:

            if hasattr(sql, '__iter__'):
                for sq in sql:
                    self._cursor.execute(sq)
            else:
                self._cursor.execute(sql)
                self._db.commit()
                result = self._cursor.fetchone()
                yield result
        except Exception as e:
            self._db.rollback()
            LOGGER.error("执行语句出错了。错误信息：{}".format(e))
        finally:
            self._db.close()
            LOGGER.info("数据库连接关闭!")

    @logged
    def select_all(self, sql):
        try:
            if iter(sql):
                for sq in sql:
                    self._cursor.execute(sq)
                    self._db.commit()
                    result = self._cursor.fetchall()
                    yield result
            else:
                self._cursor.execute(sql)
                self._db.commit()
                result = self._cursor.fetchall()
                yield result
        except Exception as e:
            self._db.rollback()
            LOGGER.error("执行语句出错了。错误信息：{}".format(e))
        finally:
            self._db.close()
            LOGGER.info("数据库连接关闭!")

    @logged
    def insert(self, sql):
        pass

    @logged
    def update(self, sql):
        pass

    @logged
    def delete(self, sql):
        pass


class Oracle(DB):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Oracle, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super(Oracle, self).__init__()
        pass

    def insert(self, sql):
        pass

    def select(self, sql):
        pass

    def update(self, sql):
        pass

    def delete(self, sql):
        pass


if __name__ == '__main__':
    run = Mysql()
    c1 = run.select(
        "select count(user_id) from yfq_user where register_dt "
        "between str_to_date('%s', '%%Y-%%m-%%d') and str_to_date('%s', '%%Y-%%m-%%d')" % ('2018-11-01', '2018-12-01'))
    print(c1)
