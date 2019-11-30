# encoding: utf-8
'''
@author: libingchen
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: nicolas_bch@163.com
@software: garner
@file: selector.py
@time: 2019-11-08 20:41
@desc:
'''

import time, json
from public.basic_class import DBClass
from conf.settings import MYSQL_TEST, SELECTOR2CRAWLER_QUEUE, SAVER2SELECTOR_QUEUE
from public.task_obj import UrlInfo
from urlinfo_cache import UrlInfoCache
from logging import getLogger

logger = getLogger(__name__)


class Selector(DBClass):
    """
    选择器，从数据库中抽取抓取源，及配置数据
    """
    def __init__(self, mysql_info=MYSQL_TEST, send_queue=SELECTOR2CRAWLER_QUEUE, recv_queue=SAVER2SELECTOR_QUEUE):
        super(Selector, self).__init__(mysql_info=mysql_info, send_queue=send_queue, recv_queue=recv_queue)
        self.url_info_cache = UrlInfoCache()

    def send_info(self):
        task_infos = self.url_info_cache.read_cache()
        for task_info in task_infos:
            logger.info(task_info.__dict__)
            self.send_to_queue(task=task_info)

    def urlinfo_cache(self, new_task):
        """将urlinfo读入缓存，用来后期的更新和去重"""
        self.url_info_cache.insert_newtask(new_task)

    def urlconf_cache(self, new_task):
        self.url_info_cache.insert_confcache(new_task)

    def expand_sub_urls(self, task):
        sub_urls = task.sub_urls
        for sub_url in sub_urls:
            new_task = UrlInfo()
            new_task.url = sub_url
            new_task.sid = task.sid
            self.urlinfo_cache(new_task=new_task)

    def get_domain_info(self, table_name='site_group_conf'):
        self.mysql_db.set_table_name(table_name=table_name)
        sql = 'select * from {table_name}'.format(table_name=table_name)
        status, domain_rows = self.mysql_db.select_by_sql(sql)
        return domain_rows

    def get_crawl_conf(self, domain_rows, table_name='crawl_conf'):
        for row in domain_rows:
            if row:
                sid = row.get('sid')
                sql = 'select * from {table_name} where sid={sid}'.format(table_name=table_name, sid=sid)
                task_rows = self.mysql_db.select_by_sql(sql=sql)
                if not task_rows:
                    continue
                for task_row in task_rows[1]:
                    logger.info(task_row)
                    task_row['base_url'] = row.get('url')
                    self.urlconf_cache(task_row)

    def get_source_page(self, domain_rows, table_name='source_page'):
        for row in domain_rows:
            if row:
                sql = 'select * from {table_name} where sid="{sid}"'.format(table_name=table_name, sid=row.get('sid'))
                task_rows = self.mysql_db.select_by_sql(sql=sql)
                if not task_rows:
                    continue
                for task_row in task_rows[1]:
                    logger.info(task_row)
                    task_row['status'] = row.get('status')
                    task_row['site_name'] = row.get('site_name')
                    self.urlinfo_cache(task_row)

    def cache_init(self):
        # 域名与抓取逻辑绑定
        domain_rows = self.get_domain_info()
        # 拉取抓取配置
        self.get_crawl_conf(domain_rows=domain_rows)
        # 根据域名信息获取, 并存入缓存 thread-1
        self.get_source_page(domain_rows=domain_rows)

    def run(self):
        self.cache_init()
        clock = 1
        while 1:
            logger.info(clock)
            # 从缓存中读取数据存入队列
            self.send_info()
            # 根据saver反馈调整缓存结构

            time.sleep(10)
            clock+=1


if __name__ == '__main__':
    s = Selector()
    s.run()