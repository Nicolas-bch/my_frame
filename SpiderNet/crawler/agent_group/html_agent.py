# encoding: utf-8
'''
@author: libingchen
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: nicolas_bch@163.com
@software: garner
@file: html_agent.py
@time: 2019-11-07 20:27
@desc:
'''
from public.downloader import Downloader, MySession

class HtmlAgent:
    def __init__(self):
        pass

    def download(self, task):
        status_code = 600
        content = ''
        proxy_keey = task.proxy_keey
        out_wall = task.out_wall
        session = MySession(out_wall)
        if not proxy_keey:
            session.change_ip(out_wall)
        response = session.s_get(url=task.url)
        status_code = response.status_code
        content = response.text
        session.close()
        return status_code, content


html_agent = HtmlAgent()