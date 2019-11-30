#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-08-27 10:18:56
# @Author  : RoryXiang (pingping19901121@gmail.com)
# @Link    : ${link}
# @Version : $1.0$
import requests
from conf import settings
import time
import logging

logger = logging.getLogger(__name__)


class Downloader(object):
    """docstring for Downloader"""
    ip_url = settings.ip_url
    headers = settings.default_headers
    cookies = {}

    @classmethod
    def get_proxies(cls):
        """
        get ip from clear url and format useable proxeis of requests
        :return: proxies  type: dict
        """
        while True:
            try:
                ip_res = requests.get(Downloader.ip_url)
                break
            except Exception as e:
                logger.debug("get ip error: {}".format(e))
                time.sleep(0.5)
        ip_port = ip_res.text
        proxies = {
            "http": f"http://{ip_port}",
            "https": f"https://{ip_port}"
        }
        return proxies

    @classmethod
    def get_info(cls, url, headers, proxies=None):
        """
        send a get request
        :param url: destination url of that get request
        :param headers: request headers
        :param proxies: request proxies
        :return: response
        """
        if proxies:
            response = requests.get(url,
                                    headers=headers,
                                    proxies=proxies,
                                    timeout=settings.download_timeoput)
        else:
            response = requests.get(url,
                                    headers=headers,
                                    timeout=settings.download_timeoput)
        response.encoding = response.apparent_encoding
        return response

    @classmethod
    def post_info(cls, url, headers, proxies=None, json=None, data=None):
        """
        send a post request
        :param data:
        :param json:
        :param url: destination url of that request
        :param headers: request headers
        :param proxies: request proxies
        :return: response
        """
        if proxies:
            if json:
                response = requests.post(url,
                                         json=json,
                                         headers=headers,
                                         proxies=proxies,
                                         timeout=settings.download_timeoput)
            else:
                response = requests.post(url,
                                         data=data,
                                         headers=headers,
                                         proxies=proxies,
                                         timeout=settings.download_timeoput)
        else:
            if json:
                response = requests.post(url,
                                         json=json,
                                         headers=headers,
                                         timeout=settings.download_timeoput)
            else:
                response = requests.post(url,
                                         data=data,
                                         headers=headers,
                                         timeout=settings.download_timeoput)
        response.encoding = response.apparent_encoding
        return response

    @classmethod
    def update_headers(cls, key, value):
        """
        updata one headers key value or set a new key value
        :param key: dict headers key, type: string
        :param value: the value of key set to headers, type: string
        :return:
        """
        if not isinstance(key, str):
            raise TypeError("the key of request header must be string")
        Downloader.headers[key] = value

    @classmethod
    def dowload(cls, url, methods, headers=headers, json=None, data=None):
        """
        send a get or a post request. use default headers or you can affrenten
        a Self-defined headers
        :param data:
        :param json:
        :param url:  destination url
        :param methods: request method
        :param headers: request headers
        :return: response
        """
        retry_number = 1
        while retry_number <= settings.retry_times:
            if Downloader.ip_url:
                proxies = Downloader.get_proxies()
            else:
                proxies = None
            try:
                if methods == "get":
                    response = Downloader.get_info(url,
                                                   headers,
                                                   proxies=proxies)
                else:
                    if not json and not data:
                        raise Exception(
                            "post requests needs post data but not given")
                    response = Downloader.post_info(url,
                                                    headers,
                                                    json=json,
                                                    data=data,
                                                    proxies=proxies)
                return response
            except (requests.ConnectionError,
                    requests.HTTPError,
                    requests.exceptions.ReadTimeout) as e:
                logger.debug(f"download retry {retry_number} times")
                retry_number += 1
        logger.info("Retry too much time of the target: ", url)
        return None


class MySession(requests.Session):
    """
    Encapsulate request. Session, add automatic replacement proxies and update
    cookie function

    """

    def __init__(self, out_wall=0):
        super().__init__()
        self.headers = settings.default_headers
        self.change_ip(out_wall)

    def change_ip(self, out_wall=0):
        """
        get a new ip
        :return: formated proxies
        """
        if out_wall==0:
            self.proxies = Downloader.get_proxies() if settings.ip_url else {}

    def s_get(self, url, **kwargs):
        """
        send a get request and update cookie, automatic replacement proxies if
        it's useless
        :param url: URL for the new :class:`Request` object.
        :rtype: requests.Response
        """
        try_number = 0
        while try_number < settings.retry_times:
            try:
                response = self.get(url, **kwargs)
                self.cookies.update(response.cookies)
                return response
            except (requests.ConnectionError,
                    requests.HTTPError,
                    requests.exceptions.ReadTimeout) as e:
                self.change_ip()
                try_number += 1

    def s_post(self, url, data=None, json=None, **kwargs):
        """
        send a post request and update cookie, automatic replacement proxies if
        it's useless
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:
            `Request`.
        :rtype: requests.Response
        """
        try_number = 0
        while try_number < settings.retry_times:
            try:
                response = self.post(url, data=data, json=json, **kwargs)
                self.cookies.update(response.cookies)
                return response
            except (requests.ConnectionError,
                    requests.HTTPError,
                    requests.exceptions.ReadTimeout) as e:
                self.change_ip()
                try_number += 1
