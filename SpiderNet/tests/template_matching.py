# encoding: utf-8
'''
@author: libingchen
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: nicolas_bch@163.com
@software: garner
@file: template_matching.py
@time: 2019-11-20 11:12
@desc:
'''

import re, json
from urllib.parse import urlsplit, urlparse, parse_qs

url1 = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=%E5%AD%97%E5%85%B8%E7%9A%84key%E9%9C%80%E8%A6%81%E5%8A%A0%E5%AF%86%E5%8E%8B%E7%BC%A9%E5%90%97&oq=%25E5%25AD%2597%25E5%2585%25B8%25E7%259A%2584key%25E9%259C%2580%25E8%25A6%2581%25E5%258A%25A0%25E5%25AF%2586%25E5%258E%258B%25E7%25BC%25A9%25E7%25A0%2581&rsv_pq=89f28c520000c4bd&rsv_t=6e3dJhdT2kxoOVgbal9y8isfJPrxffU%2BaYFcM5FvKdQZNDWmCRp9EpXcUgM&rqlang=cn&rsv_enter=1&rsv_dl=tb&inputT=1388&rsv_sug3=41&rsv_sug1=14&rsv_sug7=000&rsv_sug2=0&rsv_sug4=2672&rsv_sug=1'

url2 = 'https://www.baidu.com/s?wd=%E5%AD%97%E5%85%B8%E7%9A%84key%E9%9C%80%E8%A6%81%E5%8A%A0%E5%AF%86%E5%8E%8B%E7%BC%A9%E5%90%97&pn=10&oq=%E5%AD%97%E5%85%B8%E7%9A%84key%E9%9C%80%E8%A6%81%E5%8A%A0%E5%AF%86%E5%8E%8B%E7%BC%A9%E5%90%97&ie=utf-8&rsv_pq=9095d10000009568&rsv_t=7748sS%2Bxii%2F1%2FgOAiCfguxdwxPNphBDxn%2FIn2Vpb%2FnfLTmpg96p8NpP5je4&rsv_page=1'

url3 = 'https://www.baidu.com/s?wd=%E5%AD%97%E5%85%B8%E7%9A%84key%E9%9C%80%E8%A6%81%E5%8A%A0%E5%AF%86%E5%8E%8B%E7%BC%A9%E5%90%97&pn=20&oq=%E5%AD%97%E5%85%B8%E7%9A%84key%E9%9C%80%E8%A6%81%E5%8A%A0%E5%AF%86%E5%8E%8B%E7%BC%A9%E5%90%97&ie=utf-8&rsv_pq=a1b24297000647f6&rsv_t=4ffdDrlqHDFoQd9WXo9pfq61tJbA%2BG9TtQ5%2FfL6YNShQW8qBBkN9naRBtPA&rsv_page=1'

url = 'http://ent.people.com.cn/n1/2019/1120/c1012-31464178.html'

print(urlparse(url))

url1_split = urlsplit(url1)
url2_split = urlsplit(url2)
url3_split = urlsplit(url3)

url1_query = parse_qs(url1_split.query)
url2_query = parse_qs(url2_split.query)
url3_query = parse_qs(url3_split.query)
# print(url1_query, url2_query, url3_query, sep='\n')

url1_query_params = {key: url1_query[key][0] for key in url1_query}
url2_query_params = {key: url2_query[key][0] for key in url2_query}
url3_query_params = {key: url3_query[key][0] for key in url3_query}
# print(json.dumps(url1_query_params, indent=1), json.dumps(url2_query_params, indent=1), json.dumps(url3_query_params, indent=1), sep='\n')


a = {'a':1, 'b':2, 'c':3}
print(a.__str__())
a.__delitem__('a')
print(a)
