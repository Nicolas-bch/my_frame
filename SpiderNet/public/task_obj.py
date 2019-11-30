# encoding: utf-8
'''
@author: libingchen
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: nicolas_bch@163.com
@software: garner
@file: task_obj.py
@time: 2019-11-07 14:55
@desc:
'''
import json, time
import logging
from public.logger import add_logger_handler

logger = logging.getLogger(__name__)
add_logger_handler(logger, __name__)


# """
# create table source_page(
#     id bigint(20) NOT NULL AUTO_INCREMENT,
#     sid varchar(40) not null comment "域名id",
#     gid varchar(40) not null comment "站点id",
#     url varchar(255) not null comment "网址",
#     last_crawl_time varchar(16) default null comment "上次调度时间",
#     next_crawl_time varchar(16) default null comment "下次调度时间",
#     proxy_keep int default 0 comment "代理保持",
#     retry_times int default 3 comment "重试次数",
#     url_hash varchar(40) NOT NULL,
#     PRIMARY KEY(`id`),
#     UNIQUE KEY(`sid`, `gid`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#
# create table site_group_conf(
#     id bigint(20) NOT NULL AUTO_INCREMENT,
#     sid varchar(40) not null comment "域名id",
#     gid varchar(40) default "0" comment "站点id",
#     url varchar(255) not null comment "网址",
#     site_name varchar(255) default null comment "站点名字",
#     status int default 0 comment "抓取状态 0：不参与抓取、1：参与抓取"
#     PRIMARY KEY(`id`),
#     UNIQUE KEY(`sid`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#
# create table crawl_conf(
#     id bigint(20) NOT NULL AUTO_INCREMENT,
#     sid varchar(40) not null comment "域名id",
#     gid varchar(40) not null comment "站点id",
#     crawl_type varchar(240) default "html" comment "抓取类型",
#     crawl_freq tinyint default 30 comment "抓取频率",
#     out_wall tinyint default 0 comment "0表示国内代理， 1表示国外代理 ",
#     extractor_info varchar(240) default null comment "解析方法",
#     proxy_keey int default 3 comment "代理保持",
#     PRIMARY KEY(`id`),
#     UNIQUE KEY(`sid`, `gid`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
#
# """

class UrlInfo:
    def __init__(self, data_str=None):
        self.set_init_attr()
        self.source_page_attr = ['sid', 'gid', 'url', 'status', 'site_name', 'crawl_freq', 'next_crawl_time', 'last_crawl_time', 'retry_times', 'proxy_keep']
        self.crawl_conf_attr = ['sid', 'gid', 'extractor_info', 'crawl_type', 'page_type', 'type', 'out_wall', 'url_regx']
        if data_str:
            self.update_str_to_attr(data_str)

    def set_init_attr(self):
        """

        :return:
        """
        self.sid = -1               # 域名id  all
        self.gid = -1               # 站点id  all
        self.url = ''               # url    source_page
        self.site_name = ''         # 站点名字  site_group_conf
        self.sub_url_regxs = []     # 子页面   extractor生成
        self.status = -1            # 抓取状态码：是否参与抓取     site_group_conf
        self.crawl_type = 'html'    # 抓取类型，用来帮助分配抓取器    crawl_conf
        self.crawl_freq = 30        # 抓取频率, 决定抓取频率         crawl_conf
        self.last_crawl_time = int(time.time())     # 上次调度时间        source_page
        self.next_crawl_time = self.last_crawl_time + self.crawl_freq   # 下次调度时间        source_page
        self.source_page = ''       # 源页面，crawler模块生成属性
        self.data = ''              # 解析结果，extractor模块生成属性
        self.statue_code = -1       # 抓取状态，crawler模块生成属性
        self.page_type = 'news'         # 页面类型，决定解析方式，extractor模块生成属性
        self.allow_domain = []      # 适用域名
        self.out_wall = 0           # 0表示国内代理， 1表示国外代理      crawl_conf
        self.extractor_info = ''    # 解析方法      crawl_conf
        self.proxy_keey = 0         # 代理保持  0为不保持，每次抓取切换， 1为保持      source_page crawl_conf
        self.retry_times = 3        # 重试次数，避免破解失效网站占用系统资源           source_page
        self.table_name = ''        # 数据库表名     crawl_conf
        self.type = '1'             # 页面类型  【2：detail、1：list、0：index】
        self.url_regx = ''      # 正则，用来识别url

    def update_sourcepage_attr(self, data_str):
        data_str = self.str_loads_to_json(data_str) if isinstance(data_str, str) else data_str
        for attr in self.source_page_attr:
            self.set_attr(key=attr, value=data_str.get(attr))

    def update_crawlconf_attr(self, data_str):
        data_str = self.str_loads_to_json(data_str) if isinstance(data_str, str) else data_str
        for attr in self.crawl_conf_attr:
            self.set_attr(key=attr, value=data_str.get(attr))

    def json_dumps_to_str(self):
        return json.dumps(self.__dict__)

    def str_loads_to_json(self, data_str):
        return json.loads(data_str)

    def get_attr(self, key):
        if key in self.__dict__:
            value = self.__dict__[key]
            return value

    def set_attr(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value

    def update_str_to_attr(self, data_str):
        data_json = self.str_loads_to_json(data_str) if isinstance(data_str, str) else data_str
        for key in data_json:
            if key in self.__dict__:
                # print(key, data_json[key])
                self.set_attr(key=key, value=data_json[key])
        # logger.info('urlinfo_obj value is: {}'.format(self.__dict__))

#
# class TaskEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, TaskObj):
#             return o.dump_to_str()
#         return json.JSONEncoder.default(self, o)


if __name__ == '__main__':
    row = {
        "sid": 12121212,
        "gid": 1,
        "crawl_type": 'html',
        'freq': 30,
        'last_crawl_time': 1573716617027,
        'next_crawl_time': None
    }
    url_info = UrlInfo(data_str=row)
    logger.info(url_info.__dict__)
    url_info_str = url_info.json_dumps_to_str()
    logger.info(url_info_str)
    # print(url_info_str, type(url_info_str), url_info_str.__class__)
    url_info_new = UrlInfo(url_info_str)
    logger.info(url_info_new)
    # url_info_new.update_str_to_attr(url_info_str)
    # print(url_info_new.__dict__, url_info_new.__class__)
    # import pickle
    # url_info_b = pickle.dumps(url_info)
    # print(url_info, url_info_b)
    # url_info_r = pickle.loads(url_info_b)
    # print(url_info_r, url_info_r.__doc__)


