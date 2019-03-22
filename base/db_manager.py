# !/uer/bin/env python3

import os

from configElement.yaml_data import ConfYaml
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
            try:
                conf = ConfYaml('__conf.yaml').read()
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
    def select(self, sql: str) -> tuple:
        """

        :param sql:
        :return: type(tuple)
        """
        try:
            if 'select' == sql[:6]:
                self._cursor.execute(sql)
                self._db.commit()
                result = self._cursor.fetchone()
                return result
            else:
                raise ValueError("查询sql不能执行!")
        except Exception as e:
            self._db.rollback()
            LOGGER.error("执行语句出错了。错误信息：{}".format(e))
        finally:
            self._db.close()
            LOGGER.info("数据库连接关闭!")

    @logged
    def select_all(self, sql: str) -> tuple:
        try:
            if 'select' == sql[:6]:
                self._cursor.execute(sql)
                self._db.commit()
                result = self._cursor.fetchall()
                return result
            else:
                raise ValueError("查询sql不能执行!")
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
