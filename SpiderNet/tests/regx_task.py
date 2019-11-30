# encoding: utf-8
'''
@author: libingchen
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: nicolas_bch@163.com
@software: garner
@file: regx_task.py
@time: 2019-11-21 10:54
@desc:
'''

import re

url = 'https://www.baidu.com/s?ie=UTF-8&wd=url_parse_obj%20=%20UrlInfoParse(url=url)'
pattern = 'https://(.*?)\?'



url1 = 'https://news.163.com/19/1122/09/EUIV7D16000189FH.html'
url2 = 'https://news.163.com/19/1106/17/ETAJUCLJ000189FH.html'
url3 = 'http://news.163.com/16/0616/04/BPLET51000011229.html#f=slist'
pattern1 = 'news.163.com/(\d+\/\d+\/\d+\/[\s\S]+.html)'


def tests(url, pattern):
    print(re.search(pattern, url).group(1))


if __name__ == '__main__':
    tests(url3, pattern1)