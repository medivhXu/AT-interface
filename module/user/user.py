#!/usr/bin/env python3


import datetime

from base.db_manager import mysql
from base.encrypt import Encryption
from base.my_exception import *


class User:
    info = {'uuid': None,
            'activity_id': 1,
            'vip_first_order': 1,
            'is_enabled': 1,
            'user_name': 'python',
            'vip': 1010,
            'platform_type': 10066001,
            'ref_user_id': -1,
            'create_dt': None,
            'authen_dt': None,
            'authen_status': 3,
            'authen_type': 2,
            'final_authen_type': 2,
            'user_source_type': 5,
            'user_source_value': 1201,
            'register_dt': None,
            'disabled': 1,
            'update_time': None}

    user_prefer = {'energy_type': 1,
                   'current_flag': 1,
                   'scope': 20,
                   'oil_type': 1,
                   'oil_no': 92,
                   'oil_name': '92#',
                   'oil_brand_ids': '1,2,3,4',
                   'oil_brand_names': '中国石油,中国石化,壳牌,其他',
                   'oil_habit': 0,
                   'yn': 1}

    def __init__(self, **user_info):
        """
        用户类
        :param user_info:所有用户相关信息
        """
        t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.info['uuid'] = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        self.info['authen_dt'] = t
        self.info['register_dt'] = t
        self.info['update_time'] = t
        self.info['create_dt'] = t
        if 'id' in user_info:
            user_info.pop('id')
        self.info.update(user_info)

    def add_user_info(self, phone) -> dict:
        """
        插入新用户信息到yfq_user表
        :param phone:
        :return:
        """
        self.info['phone'] = str(phone)
        self.info['nickname'] = str(phone)
        self.info['platform_code'] = str(phone)

        keys_str = ''
        for k, v in self.info.items():
            keys_str += ','.__add__(k)
        sql = 'insert into chezhubangapppp.yfq_user({}) values {}'.format(keys_str[1:],
                                                                          tuple(self.info.values()))
        with mysql() as cur:
            cur.execute(sql)
            return cur.lastrowid

    def update_user_info(self, phone=None) -> bool:
        """
        更新用户信息
        :param phone:
        :return:
        """
        if 'phone' in self.info.keys():
            phone = self.get_user_info_by_phone(self.info.get('phone'))
            self.info.pop('phone')
            keys_str = ''
            for k, v in self.info.items():
                keys_str += ','.__add__('{}={}'.format(k, v))
            sql = 'update chezhubangapppp.yfq_user set {} where phone={}'.format(keys_str[1:], str(phone))
            with mysql() as cur:
                cur.execute(sql)
                return True
        elif 'user_id' in self.info.keys():
            user_id = self.info.get('user_id')
            self.info.pop('user_id')
            self.info.pop('phone')
            keys_str = ''
            for k, v in self.info.items():
                keys_str += ','.__add__('{}={}'.format(k, v))
            sql = 'update chezhubangapppp.yfq_user set {} where user_id={}'.format(keys_str[1:], str(user_id))
            with mysql() as cur:
                cur.execute(sql)
                return True
        else:
            if phone:
                keys_str = ''
                for k, v in self.info.items():
                    keys_str += ','.__add__('{}={}'.format(k, v))
                sql = 'update chezhubangapppp.yfq_user set {} where phone={}'.format(keys_str[1:], str(phone))
                with mysql() as cur:
                    cur.execute(sql)
                    return True
            else:
                raise Parameter("缺少必要参数！")

    @staticmethod
    def delete_user_info_by_phone(phone) -> bool:
        """
        删除指定用户
        :param phone:
        :return:
        """
        sql = 'DELETE FROM `chezhubangapppp`.`yfq_user` WHERE `phone` = {}'.format(phone)
        with mysql() as cur:
            cur.execute(sql)
            return True

    @staticmethod
    def get_user_info_by_phone(phone) -> dict:
        """
        根据手机号获取用户信息
        :param phone:
        :return:
        """
        sql = 'select * from chezhubangapppp.yfq_user where phone={}'.format(phone)
        with mysql() as cur:
            cur.execute(sql)
            data = cur.fetchall()
            return data

    @staticmethod
    def set_level_3_funrun(phone) -> bool:
        """
        根据手机号设置三级分润用户
        :param phone:
        :return:
        """
        del_sql = 'delete from chezhubangapppp.yfq_user where user_id=1000'
        sql = 'update chezhubangapppp.yfq_user set user_id=1000 where phone={}'.format(phone)
        with mysql() as cur:
            cur.execute(del_sql)
            cur.execute(sql)
            return True

    @staticmethod
    def set_vip(phone) -> bool:
        """
        设置优享会员
        :param phone:
        :return:
        """
        sql = 'update chezhubangapppp.yfq_user set vip=1012 where phone={}'.format(phone)
        with mysql() as cur:
            cur.execute(sql)
            return True

    def add_preferences(self, prefer) -> dict:
        """
        设置用户偏好
        :param prefer:
        :return:
        """
        self.user_prefer.update(prefer)
        keys_str = ''
        for k, v in self.user_prefer.items():
            keys_str += ','.__add__(k)

        sql = 'insert into chezhubangapppp.czb_user_prefer({}) values {}'.format(keys_str[1:],
                                                                                 tuple(prefer.values()))
        with mysql() as cur:
            cur.execute(sql)
            return cur.lastrowid

    def update_preferences(self, user_id, prefer=None) -> bool:
        """
        更新用户偏好
        :param user_id:
        :param prefer:
        :return:
        """
        kwargs_str = ''
        if prefer:
            self.user_prefer.update(prefer)
            for k, v in self.user_prefer.items():
                kwargs_str += ','.__add__('{}=\'{}\''.format(k, v))
        else:
            for k, v in self.user_prefer.items():
                kwargs_str += ','.__add__('{}=\'{}\''.format(k, v))
        sql = 'update chezhubangapppp.czb_user_prefer set {} where user_id={}'.format(kwargs_str[1:], user_id)
        with mysql() as cur:
            cur.execute(sql)
            return True

    def get_preferences_by_phone(self, phone=None) -> dict:
        """
        查询用户偏好
        :param phone:
        :return:
        """
        user_id = self.get_user_info_by_phone(phone).get('user_id')
        if phone:
            sql = 'select * from chezhubangapppp.czb_user_prefer where user_id={}'.format(user_id)
            with mysql() as cur:
                cur.execute(sql)
                data = cur.fetchall()
                return data
        else:
            user_id = self.get_user_info_by_phone(self.info.get('phone'))
            sql = 'select * from chezhubangapppp.czb_user_prefer where user_id={}'.format(user_id)
            with mysql() as cur:
                cur.execute(sql)
                data = cur.fetchall()
                return data

    @staticmethod
    def set_certification(phone, authen_type=1, platform_type=10066001, first_after_auth=1) -> dict:
        """
        设置用户认证类型
        :param phone:
        :param authen_type: 认证类型，1:物流车,2:专快车,3:出租车,4:私家车,999:默认私家车
        :param platform_type: 设置认证来源
        :param first_after_auth: 是否首次认证
        :return:
        """
        if platform_type == 10066001:
            sql = 'insert into chezhubangapppp.czb_user_authentication(user_id,phone,platform_type,default_flag,' \
                  'group_id,authen_status,authen_type,first_after_auth,yn) values {}'.format(phone, platform_type, 0, 0,
                                                                                             3, authen_type,
                                                                                             first_after_auth, 1
                                                                                             )
        else:
            sql = 'insert into chezhubangapppp.czb_user_authentication(user_id,phone,platform_type,default_flag,' \
                  'group_id,authen_status,authen_type,first_after_auth,yn) values {}'.format(phone, platform_type, 1,
                                                                                             1003, 3, authen_type,
                                                                                             first_after_auth, 1
                                                                                             )
        with mysql() as cur:
            cur.execute(sql)
            return cur.lastrowid

    @staticmethod
    def get_certification_info(phone) -> dict:
        """
        获取用户认证信息
        :param phone:
        :return:
        """
        sql = 'select * from chezhubangapppp.czb_user_authentication where phone={}'.format(phone)
        with mysql() as cur:
            cur.execute(sql)
            data = cur.fetchall()
            return data

    @staticmethod
    def set_pay_password(phone, pwd) -> bool:
        """
        设置用户支付密码
        :param phone:
        :param pwd:
        :return:
        """
        pwd_md5 = Encryption.md5(pwd)
        sql = 'update chezhubangapppp.yfq_user set pay_password={} where phone={}'.format(pwd_md5, phone)
        with mysql() as cur:
            cur.execute(sql)
            return True

    @staticmethod
    def set_auth(user_id, phone, user_type=11) -> dict:
        """
        设置用户授权渠道
        :param user_id:
        :param phone:
        :param user_type: 11手机号,12微信,13小程序
        :return:
        """
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "insert into chezhubangapppp.czb_user_auth(user_id,user_type,identifier,create_time,create_user,yn) " \
              "values {}".format(user_id, user_type, phone, time, 'python', 1)
        with mysql() as cur:
            cur.execute(sql)
            return cur.lastrowid
