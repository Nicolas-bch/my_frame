# encoding: utf-8
'''
@author: libingchen
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: nicolas_bch@163.com
@software: garner
@file: saver.py
@time: 2019-11-13 16:03
@desc:
'''
import json
from public.task_obj import UrlInfo
from public.basic_class import DBClass
# from conf.settings import MYSQL_TEST
from conf.settings import EXTRACTOR2SAVER_QUEUE, SAVER2SELECTOR_QUEUE
import logging

logger = logging.getLogger(__name__)


class Saver(DBClass):
    count = 5
    def __init__(self, send_queue=SAVER2SELECTOR_QUEUE, recv_queue=EXTRACTOR2SAVER_QUEUE):
        super(Saver, self).__init__(send_queue=send_queue, recv_queue=recv_queue)

    def report_crawl_state(self, data):
        status_code = data.statue_code
        page_source = data.source_page
        extractor_data = data.data
        freq = int(data.crawl_freq)
        if status_code==200 and extractor_data:
            if data.retry_times<3:
                data.retry_times = 3
                data.crawl_freq = 30
        else:
            data.crawl_freq = 1.5*freq
            data.proxy_keep = 0
            data.retry_times -= 1

    def insert_to_db(self, task):
        # 存入mongo
        mongo_tb = self.mongo_db['wangyi']
        mongo_tb.insert(json.loads(task.get_attr('data')))

    def save_item(self, task):
        # 状态码判断
        self.report_crawl_state(data=task)
        # 数据入库
        self.insert_to_db(task)
        # 将抓取情况反馈给selector
        # for url in urls:
        logger.info('*'*100)
        logger.info(task.__dict__)
        self.send_to_queue(task=task)

    def deal_queue_info(self, ch, method, properties, body):
        task_str = body.decode(encoding='utf-8')
        data = UrlInfo(task_str)
        self.save_item(task=data)

    def run(self):
        self.get_from_queue(callback=self.deal_queue_info)


if __name__ == '__main__':
    s = Saver()
    s.run()