#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019/11/11 15:30
# @Author  : RoryXiang (pingping19901121@gmail.com)
# @Link    : ""
# @Version : 1.0

from news_extractor import extract_news
from lxml import etree
from public.basic_class import DBClass
import re, json
from public.dequeue import Dequeue
from public.task_obj import UrlInfo
from utils.url_info_parse import UrlInfoParse
from logging import getLogger
from public.logger import add_logger_handler
from conf.settings import CRAWLER2EXTRACTOR_QUEUE, EXTRACTOR2SAVER_QUEUE, MYSQL_TEST

logger = getLogger(__name__)
add_logger_handler(logger, "extractor.log")


class Extractor(DBClass):

    def __init__(self):
        self.domain_url = ""
        self.queue_recv_name = CRAWLER2EXTRACTOR_QUEUE
        self.queue_send_name = EXTRACTOR2SAVER_QUEUE
        super(Extractor, self).__init__(mysql_info=MYSQL_TEST, send_queue=self.queue_send_name, recv_queue=self.queue_recv_name)

    def extract_xpath(self, html, xpath):
        text_list = html.xpath(xpath)
        text = "".join(text_list)
        return text

    def extract_info(self, html, xpath_condition):
        data = {}
        for key, xpath in xpath_condition.items():
            text = self.extract_xpath(html, xpath)
            data[key] = text
        return data

    def check_perfect_url(self, urls):
        perfect_urls = []
        for url in urls:
            urlp = UrlInfoParse(url)
            perfect_urls.append(urlp.format_url(domain_url=self.domain_url))
        return perfect_urls

    def extract_href(self, source_page, re_rule):
        results = re.findall(re_rule, source_page)
        results = self.check_perfect_url(urls=results)
        return results

    def get_sub_urls(self, sub_url_regxs, source_page):
        # task.sub_url_regx = '//a/@href'
        urls = []
        if sub_url_regxs:
            for re_condition in sub_url_regxs:
                # 获取提取阔连的正则
                sub_urls = self.extract_href(source_page, re_condition)
                urls.extend(sub_urls)
        return urls

    def callback(self, ch, method, properties, body):
        task = UrlInfo(body.decode(encoding='utf-8'))
        data = {}
        gid = task.gid
        self.domain_url = task.url
        source_page = task.source_page  # 获取网页源码
        statue_code = task.statue_code
        sub_url_regxs = task.sub_url_regxs

        if task.page_type == "news":  # 如果是新闻类的提取
            if statue_code == '200':
                data = extract_news(source_page)
                task.data = json.dumps(data)
                logger.info('extractor_to_saver: {}'.format(task.__dict__))
        else:
            extractor_info = task.extractor_info
            if extractor_info:
                extractor_info_dict = extractor_info if isinstance(extractor_info, dict) else json.loads(extractor_info)
                extractor_type = extractor_info_dict.get('extractor_type')
                if extractor_type in ['xpath']:
                    xpath_info = extractor_info_dict.get('xpath')
                    html = etree.HTML(source_page)
                    # 获取xpath信息
                    if xpath_info:
                        print(xpath_info)
                        data = self.extract_info(html, xpath_info)  # 获取详情信息
                        task.set_attr("data", data)
        if sub_url_regxs:
            task.sub_urls = self.get_sub_urls(sub_url_regxs=sub_url_regxs, source_page=source_page)
        self.send_to_queue(task=task)



    def run(self):
        queue_name = CRAWLER2EXTRACTOR_QUEUE
        self.get_from_queue(callback=self.callback)
        pass


if __name__ == '__main__':
    e = Extractor()
    e.run()