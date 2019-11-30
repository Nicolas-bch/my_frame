#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019/11/7 10:54
# @Author  : RoryXiang (pingping19901121@gmail.com)
# @Link    : ""
# @Version : 1.0

from utils.GeneralNewsExtractor import GeneralNewsExtractor


def extract_news(source_page):
    extractor = GeneralNewsExtractor()
    news = extractor.extract(source_page)
    return news


