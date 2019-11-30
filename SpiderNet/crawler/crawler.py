# encoding: utf-8
'''
@author: libingchen
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: nicolas_bch@163.com
@software: garner
@file: crawler.py
@time: 2019-11-07 11:27
@desc:
'''
from agent_group import html_agent
from functools import partial
from public.basic_class import DBClass
from public.task_obj import UrlInfo
import gevent, time
from conf.settings import SELECTOR2CRAWLER_QUEUE, CRAWLER2EXTRACTOR_QUEUE
import logging
logger = logging.getLogger(__name__)



class Dispatcher:
    def __init__(self):
        self.agent_cache = {
            'html': 'html_agent.HtmlAgent()',
            'facebook': 'facebook_agent.FacebookAgent()',
            'js': 'js_agent.JsAgent()',
            'scrapy': 'scrapy_agent.ScrapyAgent()',
            'selenium': 'selenium_agent.SeleniumAgent()',
            'splash': 'splash_agent.SplashAgent()',
            'twitter': 'twitter_agent.TwitterAgent()'
        }

    def get_agent(self, task):
        task_type = task.crawl_type
        if not task_type:
            task_type = 'html'
        crawl_agent = eval(self.agent_cache[task_type])
        return crawl_agent


class Crawler(DBClass):
    count = 5
    def __init__(self, send_queue=CRAWLER2EXTRACTOR_QUEUE, recv_queue=SELECTOR2CRAWLER_QUEUE):
        super(Crawler, self).__init__(send_queue=send_queue, recv_queue=recv_queue)
        self.tasks = []
        self.dispatcher = Dispatcher()

    def queue_info(self, ch, method, properties, body):
        try:
            data_str = body.decode(encoding='utf-8')
            task = UrlInfo(data_str)
            # self.tasks.append(task)
            status_code, content = self.download(task=task)
            task.source_page = content
            task.statue_code = status_code
            last_crawl_time = int(time.time())
            next_crawl_time = last_crawl_time+int(task.crawl_freq)
            task.set_attr(key='last_crawl_time', value=last_crawl_time)
            task.set_attr(key='next_crawl_time', value=next_crawl_time)
            self.send_info(task=task)
        except Exception as e:
            logger.error(e)

    def send_info(self, task):
        logger.info('send to queue! \n {}'.format(task.__dict__))
        self.send_to_queue(task=task)

    def _run(self):
        while 1:
            try:
                self.get_from_queue(callback=self.queue_info)
            except Exception as e:
                time.sleep(20)
                logger.error('downloader broken!!! error info:{}'.format(e))
                continue

    def download(self, task):
        agent = self.dispatcher.get_agent(task)
        status_code, content = agent.download(task)
        return status_code, content

    def run(self):
        self._run()
        # tasks = self.tasks[:5]
        # resps = [gevent.spawn(self.download, dispatcher=self.dispatcher, task=task) for task in tasks]
        # map = dict(zip(resps, tasks))
        # [resp.link_value(partial(self.send_to_queue, map[resp])) for resp in resps]
        # gevent.joinall(resps)
        #
        # if len(self.tasks)<5:
        #     logger.info('task length not enough! {}'.format(len(self.tasks)))
        #     time.sleep(2)




if __name__ == '__main__':
    c = Crawler()
    c.run()
