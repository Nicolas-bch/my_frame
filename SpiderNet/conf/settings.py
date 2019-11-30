#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019/11/6 11:23
# @Author  : RoryXiang (pingping19901121@gmail.com)
# @Link    : ""
# @Version : 1.0
from conf.models import DBConf


ENV = 1     # 1: 测试环境

if ENV == 1:
    # 代理IP获取地址
    ip_url = "http://116.196.124.10:1316/getIp"

    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/53"
                      "7.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/53"
                      "7.36"
    }

    download_timeoput = 5

    retry_times = 5

    # redis
    REDISHOST, REDISPORT, REDISPASSWORD = "127.0.0.1", 6379, ""

    # mongo
    MONGOHOST, MONGOPORT = "127.0.0.1", 27017
    MONGOUSER, MONGOPASSWORD, MONGODATABASE = "test", "123456", "test"

    # mysql
    MYSQL_TEST = DBConf(host="localhost", db="lvwan", user="root", passwd="")



    # queue
    # 选择器到检索器的消息队列
    SELECTOR2CRAWLER_QUEUE = 'selector2crawler_test'

    # 检索器到提取器的消息队列
    CRAWLER2EXTRACTOR_QUEUE = 'crawler2extractor_test'

    # 提取器到存储器的消息队列
    EXTRACTOR2SAVER_QUEUE = 'extractor2saver_test'

    # 存储器到选择器提供抓取反馈的队列
    SAVER2SELECTOR_QUEUE = 'saver2selector_test'

