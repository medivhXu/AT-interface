#!/usr/bin/env python3

import datetime


def get_random_outer_order_id(order_length=20, orders_num=1):
    suffix = 1
    while orders_num > 0:
        prefix = 'TEST'
        middle = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        order_no = ('0' * (order_length - len(str(suffix)) - len(prefix) - len(middle))).join(
            (prefix, middle, str(suffix)))
        yield order_no
        suffix += 1
        orders_num = orders_num - 1
