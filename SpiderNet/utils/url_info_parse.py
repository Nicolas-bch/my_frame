# encoding: utf-8
'''
@author: libingchen
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: nicolas_bch@163.com
@software: garner
@file: url_info_parse.py
@time: 2019-11-20 15:59
@desc:
'''
from urllib.parse import urlparse, parse_qs, urljoin


class UrlInfoParse:
    def __init__(self, url):
        url_parse_result = urlparse(url)
        self.scheme = url_parse_result.scheme
        self.domain = url_parse_result.netloc
        self.path = url_parse_result.path
        self.params = url_parse_result.query
        params = parse_qs(self.params)
        self.params_dict = {key: params[key][0] for key in params}

    def format_url(self, domain_url):
        perfect_url = urljoin()
        pass


if __name__ == "__main__":
    url = "https://tianchi.aliyun.com/notebook-ai/detail?spm=5176.12282042.0.0.77532042ZBtyl3&postId=6471"
    u = UrlInfoParse(url)
    print(u.__dict__)