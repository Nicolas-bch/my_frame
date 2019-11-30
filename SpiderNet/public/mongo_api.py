#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-08-08 14:01:51
# @Author  : RoryXiang (xiangshangping@lvwan.com)
# @Link    : ${link}
# @Version : $Id$

from pymongo import MongoClient
from conf.settings import (MONGOHOST, MONGOPORT, MONGOPASSWORD, MONGODATABASE,
                           MONGOUSER)


def get_mongo_db():
    """
    获取mongo数据库连接对象
    :return:
    """
    mongo_client = MongoClient(host=MONGOHOST, port=MONGOPORT, connect=False)
    db = mongo_client[MONGODATABASE]
    db.authenticate(MONGOUSER, MONGOPASSWORD)
    return db
