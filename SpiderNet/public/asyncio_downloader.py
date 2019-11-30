#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019/11/15 17:28
# @Author  : RoryXiang (pingping19901121@gmail.com)
# @Link    : ""
# @Version : 1.0

import asyncio
from aiohttp import ClientSession
import requests_async as requests
from conf import settings
import time


class Downloader(object):
    ip_url = settings.ip_url
    headers = settings.default_headers
    cookie = {}

    @classmethod
    async def get_proxies(cls):
        while True:
            try:
                ip = await requests.get(Downloader.ip_url, timeout=2)
                ip = ip.decode()
                proxies = {
                    "http": f"http://{ip}",
                    "https:": f"https://{ip}"
                }
                return proxies
            except Exception as e:
                time.sleep(1)


if __name__ == "__main__":
    pp = Downloader.get_proxies()
    print(pp)
