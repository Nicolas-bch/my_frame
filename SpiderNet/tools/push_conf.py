# encoding: utf-8
'''
@author: libingchen
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: nicolas_bch@163.com
@software: garner
@file: push_conf.py
@time: 2019-11-21 20:37
@desc:
'''
import time
from utils.common_utils import md
from public.mysql_api import Dbconn
from conf.settings import MYSQL_TEST
from logging import getLogger

logger = getLogger(__name__)


site_group_conf = {
    'sid': 123457,
    'gid': 0,
    'url': 'https://news.163.com/',
    'site_name': '网易新闻',
    'allow_domain': '',
    'status': 1
}


source_page = {
    'sid': 123457,
    'gid': 0,
    'url': 'http://news.163.com/19/0530/18/EGEPFFCR000189DG.html',
    'last_crawl_time': int(time.time()),
    'next_crawl_time': int(time.time())+30,
    'crawl_freq': 30,
    'proxy_keep': 1,
    'retry_times': 3,
    'url_hash': md('http://news.163.com/19/0530/18/EGEPFFCR000189DG.html')
}


crawl_conf = {
    'sid': 123457,
    'gid': 1,
    'crawl_type': 'html',
    'crawl_freq': 3600,
    'out_wall': 0,
    'extractor_info': {},
    'proxy_keep': 0,
    'url_regx': 'news.163.com/(\d+\/\d+\/\d+\/[\s\S]+.html)',
    'type': '2',
    'page_type': 'news'
}


def push2line():
    db_conn = Dbconn(db_name=MYSQL_TEST.db, host=MYSQL_TEST.host, user=MYSQL_TEST.user, passwd=MYSQL_TEST.passwd)
    table_list = ['site_group_conf', 'source_page', 'crawl_conf']
    import json
    for table_name in table_list:
        logger.info(json.dumps(eval(table_name)))
        # for key in eval(table_name):
        #     print(key, eval(table_name)[key])
        db_conn.set_table_name(table_name=table_name)
        db_conn.insert(values=eval(table_name))



if __name__ == '__main__':
    push2line()