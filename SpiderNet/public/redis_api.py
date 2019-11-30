#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-29 10:46:56
# @Author  : RoryXiang (pingping19901121@gmail.com)
# @Link    : ${link}
# @Version : $Id$

from redis import ConnectionPool, Redis
from conf.settings import REDISHOST, REDISPORT, REDISPASSWORD
import redis


class RedisPool(object):
    """
    redis连接池单例
    """
    _contener = {}

    def __new__(cls, *args, **kwargs):
        if not RedisPool._contener:
            obj = super().__new__(cls)
            RedisPool._contener["cls"] = obj
        return RedisPool._contener["cls"]

    def __init__(self):
        if REDISPASSWORD:
            self.pool = ConnectionPool(host=REDISHOST,
                                       port=REDISPORT,
                                       password=REDISPASSWORD)
        else:
            self.pool = ConnectionPool(host=REDISHOST,
                                       port=REDISPORT)

# 连接池
# 把他做成单例，写在一个文件里面，import它

# 拿到一个redis的连接池
pool = redis.ConnectionPool(host=REDISHOST, port=REDISPORT, password=REDISPASSWORD)


# print(conn.get('name').decode('utf-8'))


# 如果想要并发操作，就需要写成单列,以模块导入就是一个单例,把他做成单例，写在一个文件里面，import它,就是一个单例


def connection(db=0):
    """
    获取redis数据库连接对象
    :param db: number, db name
    :return:
    """
    # pool = RedisPool()
    # conn = Redis(connection_pool=pool, db=db)
    # 从池子中拿一个链接
    conn = redis.Redis(connection_pool=pool, decode_responses=True, db=db)
    return conn

