# encoding: utf-8
'''
@author: libingchen
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: nicolas_bch@163.com
@software: garner
@file: urlinfo_cache.py
@time: 2019-11-12 10:02
@desc:
'''
import time, re, logging
from public.task_obj import UrlInfo
from utils.common_utils import md
from utils.bloom_filter import BloomFilter


logger = logging.getLogger(__name__)



class UrlInfoCache:
    def __init__(self):
        # self.server = connection()
        self.dumplicate_filter = BloomFilter(key='task')
        self.cache = dict()
        self.re_cache = dict()

    def check_cache(self, task, url_hash):
        """
        type 0表示首页，1表示列表页，2表示正文; status_code 200 表示检索完成， 根据正文页不变性，不需要再检索
        :param task:
        :param url_hash:
        :return:
        """
        type = task.type
        # cache_name = self.get_cache_name(salt)
        if type=='2':   # 详情页
            if task.statue_code==200:
                self.dumplicate_filter.insert(value=url_hash)
            if self.dumplicate_filter.is_exist(url_hash):
                return False
        return True

    def check_task(self, task):
        """
        检查task完整性
        :param task:
        :return:
        """
        # 检测关键属性，sid, gid, url, status, statue_code, retry_time
        # task.source_page_attr = ['sid', 'gid', 'url', 'status', 'crawl_freq', 'next_crawl_time', 'last_crawl_time', 'retry_times', 'proxy_keep']
        logger.info(task.__dict__)
        if task.sid and int(task.sid)<0:
            return False
        if not task.url:
            return False
        if task.status<0:
            return False
        if task.retry_times<0:
            return False
        return True

    def insert_cache(self, task, url_hash):
        if url_hash in self.cache:
            next_crawl_time = task.last_crawl_time+task.crawl_freq
            # self.cache[url_hash] = next_crawl_time
        else:
            self.cache[url_hash] = dict()
            next_crawl_time = task.next_crawl_time
            if not next_crawl_time:
                next_crawl_time = int(time.time())
                # crawl_freq = task.crawl_freq
        task.next_crawl_time = next_crawl_time
        if self.check_task(task):
            self.cache[url_hash] = task.__dict__

    def insert_newtask(self, new_task):
        # 1 检查是否已在缓存中，如果没有，检查是否不需要进一步检索（正文页唯一性）
        task = UrlInfo()
        task.update_sourcepage_attr(new_task)
        if task.url:
            url_hash = md(task.url)
            flag = self.check_cache(task=task, url_hash=url_hash)
            logger.info('check_cache result: {}'.format(flag))
            if flag:
                self.insert_cache(task=task, url_hash=url_hash)

    def insert_confcache(self, new_task):
        sid = new_task.get('sid')
        regx = new_task.get('url_regx')
        task = UrlInfo()
        task.update_crawlconf_attr(new_task)
        self.re_cache[sid] = dict()
        self.re_cache[sid][regx] = task.__dict__

    def add_crawl_conf(self, task):
        crawl_conf_attr = task.crawl_conf_attr
        url = task.url
        sid = task.sid
        resp = ''
        sub_url_regxs = []
        for regx in self.re_cache[sid]:
            sub_url_regxs.append(regx)
            try:
                print(regx)
                resp = re.search(regx, url).group(1)
                if resp:
                    conf = self.re_cache[sid][regx]
                    for attr in crawl_conf_attr:
                        task.set_attr(key=attr, value=conf[attr])
                    break
                else:
                    continue
            except Exception as e:
                logger.error(e)
                continue
        task.sub_url_regxs = sub_url_regxs
        return resp

    def read_cache(self):
        need_crawl = []
        for url_hash in self.cache:
            task_info = self.cache[url_hash]
            next_crawl_time = task_info.get('next_crawl_time')
            if int(next_crawl_time)<=int(time.time()) and int(task_info.get('retry_times'))>0:
                print(1)
                task = UrlInfo(task_info)
                flag = self.add_crawl_conf(task=task)
                if flag:
                    print(3)
                    need_crawl.append(task)
        logger.info('read_cache: {}'.format(need_crawl))
        return need_crawl

